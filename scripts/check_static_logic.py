"""Conservative static checks; never run notebook cells or fit models.

Check global bindings, import/API availability, named constructor arguments,
and obvious fitting against explicitly named test arrays. This is not a proof
of algorithmic correctness, convergence, numerical accuracy, or teaching depth.
"""
from __future__ import annotations
import ast
import builtins
import importlib
import inspect
import json
import symtable
import nbformat
from academy_tools import ROOT, inventory


def unbound_globals(source):
    table = symtable.symtable(source, '<notebook-static>', 'exec')
    bound = set(dir(builtins)) | {'__name__', '__file__'}
    bound.update(s.get_name() for s in table.get_symbols()
                 if s.is_assigned() or s.is_imported() or s.is_namespace())
    missing = set()
    def inspect_scope(scope):
        for symbol in scope.get_symbols():
            if symbol.is_referenced() and symbol.is_global() and symbol.get_name() not in bound:
                missing.add(symbol.get_name())
        for child in scope.get_children():
            inspect_scope(child)
    inspect_scope(table)
    return sorted(missing)


def keyword_errors(call, callable_object):
    try:
        parameters = inspect.signature(callable_object).parameters
    except (ValueError, TypeError):
        return []
    if any(p.kind == inspect.Parameter.VAR_KEYWORD for p in parameters.values()):
        return []
    return sorted(k.arg for k in call.keywords if k.arg is not None and k.arg not in parameters)


def inspect_source(source):
    tree = ast.parse(source)
    errors = [f'Unbound global name: {name}' for name in unbound_globals(source)]
    imports = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            if node.module == '__future__':
                continue
            try:
                module = importlib.import_module(node.module)
                for alias in node.names:
                    if alias.name != '*':
                        imports[alias.asname or alias.name] = getattr(module, alias.name)
            except (ImportError, AttributeError) as exc:
                errors.append(f'Import unavailable: {node.module}: {exc}')
        elif isinstance(node, ast.Import):
            for alias in node.names:
                try:
                    importlib.import_module(alias.name)
                except ImportError as exc:
                    errors.append(f'Import unavailable: {alias.name}: {exc}')
    calls_checked = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        if isinstance(node.func, ast.Name) and node.func.id in imports:
            bad = keyword_errors(node, imports[node.func.id])
            calls_checked += 1
            if bad:
                errors.append(f'{node.func.id}: unsupported named arguments {bad}')
        if isinstance(node.func, ast.Attribute) and node.func.attr in {'fit', 'fit_transform', 'partial_fit'}:
            explicit_test = [argument.id for argument in node.args if isinstance(argument, ast.Name)
                             and argument.id in {'X_test', 'y_test', 'test_X', 'test_y'}]
            if explicit_test:
                errors.append(f'Obvious test-data fitting: {explicit_test}')
    return errors, calls_checked


def main():
    details = {}
    failures = []
    for record in inventory():
        path = ROOT/record['path']
        notebook = nbformat.read(path, as_version=4)
        if notebook.metadata.get('academy', {}).get('authoring_status') != 'draft':
            continue  # Existing reviewed lessons retain their separate evidence.
        source = '\n\n'.join(cell.source for cell in notebook.cells if cell.cell_type == 'code')
        errors, calls = inspect_source(source)
        details[record['id']] = {'status':'failed' if errors else 'passed',
                                'imported_calls_checked':calls, 'errors':errors}
        failures.extend(f'{record["id"]}: {error}' for error in errors)
    report = {'status':'failed' if failures else 'passed', 'drafts_checked':len(details),
              'cells_executed':0, 'models_fitted':0, 'errors':failures, 'notebooks':details,
              'limitations':['Global binding checks do not prove cell ordering or all control-flow paths.',
                             'API checks inspect installed imports and direct named calls only.',
                             'No numerical, convergence, plot, or full educational review was performed.',
                             'A static pass must never be recorded as a successful notebook execution.']}
    (ROOT/'reports/static_logic_checks.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k!='notebooks'},indent=2))
    raise SystemExit(bool(failures))


if __name__ == '__main__':
    main()
