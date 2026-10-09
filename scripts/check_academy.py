"""Check inventory, prerequisites, notebook substance, and local documentation links."""
from __future__ import annotations
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
import nbformat
from academy_tools import ROOT, inventory, source_hash

def validate_graph(records):
    lookup = {r['id']:r for r in records}
    if len(lookup) != len(records): raise ValueError('Duplicate inventory IDs')
    if len({r['path'] for r in records}) != len(records): raise ValueError('Duplicate notebook paths')
    active, done = set(), set()
    def visit(ident):
        if ident in active: raise ValueError(f'Prerequisite cycle at {ident}')
        if ident in done: return
        if ident not in lookup: raise ValueError(f'Unknown prerequisite {ident}')
        active.add(ident)
        for previous in lookup[ident]['prerequisites']: visit(previous)
        active.remove(ident)
        done.add(ident)
    for ident in lookup: visit(ident)

def markdown_text(path):
    if path.suffix == '.ipynb':
        return '\n\n'.join(c.source for c in nbformat.read(path, as_version=4).cells if c.cell_type == 'markdown')
    return path.read_text(encoding='utf-8')

def anchors(text):
    result = set(re.findall(r'<a\s+id=["\']([^"\']+)', text))
    for title in re.findall(r'^#{1,6}\s+(.+)$', text, flags=re.M):
        # The authored documents use simple GitHub-style heading anchors.
        result.add(re.sub(r'[^\w\- ]', '', title.lower()).replace(' ', '-'))
    return result

def broken_links(path, text=None):
    text = markdown_text(path) if text is None else text
    text = re.sub(r'```.*?```', '', text, flags=re.S)
    errors = []
    for destination in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
        url = urlsplit(destination.strip('<>'))
        if url.scheme or url.netloc: continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path.resolve()
        if not target.exists():
            errors.append(f'{path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}: missing {destination}')
        elif url.fragment and target.is_file():
            if unquote(url.fragment) not in anchors(markdown_text(target)):
                errors.append(f'{path.name}: missing anchor {destination}')
    return errors

def main():
    (ROOT/'reports/structural_checks.json').write_text('{"status": "running"}\n', encoding='utf-8')
    records = inventory()
    errors = []
    validate_graph(records)
    created = []
    details = {}
    for record in records:
        path = ROOT / record['path']
        if not path.exists(): continue
        created.append(path)
        try:
            notebook = nbformat.read(path, as_version=4)
            nbformat.validate(notebook)
            if notebook.metadata.get('academy', {}).get('id') != record['id']:
                errors.append(f'{record["id"]}: incorrect notebook identity')
            if notebook.metadata.get('academy', {}).get('dependencies', []) != record.get('dependencies', []):
                errors.append(f'{record["id"]}: declared local dependencies differ from the inventory')
            markdown = '\n\n'.join(c.source for c in notebook.cells if c.cell_type == 'markdown')
            source_file = ROOT/'lesson_sources'/f'{record["id"]}.lesson'
            if not source_file.exists():
                errors.append(f'{record["id"]}: editable lesson source is missing')
            else:
                parts = re.split(r'^```python\s*\n(.*?)^```\s*$', source_file.read_text(encoding='utf-8'), flags=re.M | re.S)
                expected_cells = [('code' if i % 2 else 'markdown', part.strip()) for i, part in enumerate(parts) if part.strip()]
                actual_cells = [(c.cell_type, c.source) for c in notebook.cells if c.id != f'{record["id"]}-display-setup']
                if actual_cells != expected_cells:
                    errors.append(f'{record["id"]}: notebook differs from its editable source; regenerate it')
            headings = [int(n) for n in re.findall(r'^#{1,2}\s+(\d+)\.', markdown, flags=re.M)]
            if headings != list(range(1,22)): errors.append(f'{record["id"]}: expected all 21 ordered educational sections')
            words = len(re.findall(r'\b[\w-]+\b', markdown))
            if words < 1000: errors.append(f'{record["id"]}: only {words} prose words; review depth')
            codes = [c for c in notebook.cells if c.cell_type == 'code']
            if len(codes) < 4: errors.append(f'{record["id"]}: insufficient executable demonstrations')
            for index, cell in enumerate(codes):
                compile(cell.source, f'{record["id"]}:cell{index}', 'exec')
                if cell.outputs or cell.execution_count is not None:
                    errors.append(f'{record["id"]}: source notebook contains execution state')
            if '**Challenge:**' not in markdown or markdown.count('**Beginner:**') < 3 or markdown.count('**Intermediate:**') < 2:
                errors.append(f'{record["id"]}: exercise levels missing')
            for number in [19,20]:
                section = re.split(rf'^## {number}\. .+\n', markdown, flags=re.M)[1].split('\n## ')[0]
                if len(re.findall(r'\*\*[^*]+\?\*\*', section)) < 5:
                    errors.append(f'{record["id"]}: section {number} needs five answered questions')
            errors.extend(broken_links(path, markdown))
            details[record['id']] = {'words':words, 'code_cells':len(codes), 'source_sha256':source_hash(notebook)}
        except Exception as exc:
            errors.append(f'{record["id"]}: {type(exc).__name__}: {exc}')
    docs = list(ROOT.glob('*.md'))
    for directory in [*sorted(ROOT.glob('[0-9][0-9]_*')), ROOT/'datasets', ROOT/'exercises', ROOT/'solutions',
                      ROOT/'assessments', ROOT/'diagrams', ROOT/'reference_materials', ROOT/'reports']:
        docs.extend(directory.glob('*.md'))
    for path in docs: errors.extend(broken_links(path))
    archived = list((ROOT/'reports/executed').rglob('*.ipynb'))
    for path in archived: errors.extend(broken_links(path))
    actual = {str(p.relative_to(ROOT)).replace('\\','/') for d in ROOT.glob('[0-9][0-9]_*') for p in d.glob('*.ipynb')}
    if actual != {r['path'] for r in records if (ROOT/r['path']).exists()}:
        errors.append('A curriculum notebook is missing from the inventory')
    report = {'status':'failed' if errors else 'passed', 'planned':len(records), 'created':len(created),
              'documents_checked':len(docs), 'executed_copies_link_checked':len(archived), 'notebooks':details, 'errors':errors,
              'limitation':'Structural checks do not prove pedagogical correctness; see content review.'}
    (ROOT/'reports/structural_checks.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k != 'notebooks'}, indent=2))
    raise SystemExit(bool(errors))

if __name__ == '__main__': main()
