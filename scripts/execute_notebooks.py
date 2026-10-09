"""Execute each created curriculum notebook in a new project-only kernel."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
from importlib.metadata import version
import json
from pathlib import Path
import subprocess
import sys
import time
from academy_tools import ROOT, configure_local_runtime, inventory, source_hash, relocate_markdown_links, local_dependency_hashes

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ids', nargs='*', help='Inventory IDs; default: every created notebook')
    parser.add_argument('--authored-only', action='store_true', help='Exclude generated drafts from explicit execution')
    args = parser.parse_args()
    expected = ROOT / '.venv' / ('Scripts/python.exe' if sys.platform == 'win32' else 'bin/python')
    if Path(sys.executable).resolve() != expected.resolve():
        raise SystemExit('Use the project .venv interpreter.')
    configure_local_runtime()
    import nbformat
    from nbclient import NotebookClient
    from jupyter_client import KernelManager
    from jupyter_client.kernelspec import KernelSpecManager
    subprocess.run([sys.executable, '-m', 'pip', 'check'], check=True)
    subprocess.run([sys.executable, '-m', 'ipykernel', 'install', '--prefix', sys.prefix,
                    '--name', 'ml-academy', '--display-name', 'Python (ML Academy .venv)'], check=True)
    entries = inventory()
    known = {r['id'] for r in entries}
    if args.ids and set(args.ids) - known:
        raise SystemExit(f'Unknown IDs: {set(args.ids) - known}')
    report_path = ROOT / 'reports/execution_results.json'
    report = json.loads(report_path.read_text()) if report_path.exists() else {'notebooks': {}}
    report['environment'] = {name:version(name) for name in ['numpy','pandas','matplotlib','seaborn','scikit-learn','nbclient','ipykernel']}
    report['python'] = sys.version.split()[0]
    report['checked_at_utc'] = datetime.now(timezone.utc).isoformat()
    failures = 0
    selected = [r for r in entries if (args.ids is None and (ROOT / r['path']).exists()) or (args.ids and r['id'] in args.ids)]
    if args.authored_only:
        selected = [r for r in selected if nbformat.read(ROOT/r['path'], as_version=4).metadata.get('academy', {}).get('authoring_status') != 'draft']
    if not selected: raise SystemExit('No authored notebooks selected.')
    for record in selected:
        ident = record['id']
        started = time.monotonic()
        result = {'status':'running', 'path':record['path'], 'checked_at_utc':datetime.now(timezone.utc).isoformat()}
        report['notebooks'][ident] = result
        report_path.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
        try:
            notebook = nbformat.read(ROOT / record['path'], as_version=4)
            nbformat.validate(notebook)
            result['source_sha256'] = source_hash(notebook)
            result['dependencies_sha256'] = local_dependency_hashes(notebook)
            specs = KernelSpecManager(kernel_dirs=[str(Path(sys.prefix) / 'share/jupyter/kernels')], ensure_native_kernel=False)
            spec = specs.get_kernel_spec('ml-academy')
            if Path(spec.argv[0]).resolve() != expected.resolve(): raise RuntimeError('Wrong kernel interpreter')
            km = KernelManager(kernel_name='ml-academy', kernel_spec_manager=specs)
            client = NotebookClient(notebook, km=km, timeout=90, startup_timeout=60, allow_errors=False,
                                    resources={'metadata':{'path':str((ROOT / record['path']).parent)}})
            executed = client.execute(cleanup_kc=True)
            cells = [c for c in executed.cells if c.cell_type == 'code']
            if not cells or any(c.execution_count is None for c in cells): raise RuntimeError('Unexecuted cells')
            errors = [o for c in cells for o in c.outputs if o.output_type == 'error']
            if errors: raise RuntimeError(str(errors))
            figures = sum('image/png' in o.get('data', {}) for c in cells for o in c.outputs)
            # Every first-batch lesson includes a meaningful plot.
            if not figures: raise RuntimeError('No rendered plot in lesson outputs')
            destination = ROOT / 'reports/executed' / record['path']
            destination.parent.mkdir(parents=True, exist_ok=True)
            for cell in executed.cells:
                if cell.cell_type == 'markdown':
                    cell.source = relocate_markdown_links(cell.source, ROOT / record['path'], destination)
            nbformat.write(executed, destination)
            result.update(status='passed', code_cells=len(cells), figures=figures,
                          output=str(destination.relative_to(ROOT)).replace('\\','/'))
            print(f'PASS {ident}: {len(cells)} code cells, {figures} plots', flush=True)
        except Exception as exc:
            result.update(status='failed', error=f'{type(exc).__name__}: {exc}')
            failures += 1
            print(f'FAIL {ident}: {exc}', flush=True)
        result['seconds'] = round(time.monotonic() - started, 3)
        report_path.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    raise SystemExit(1 if failures else 0)

if __name__ == '__main__': main()
