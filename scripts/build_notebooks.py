"""Convert authored .lesson documents into reproducible, clean notebooks."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import re
import nbformat
from build_catalog import render

ROOT = Path(__file__).resolve().parents[1]

def build():
    inventory = json.loads((ROOT / 'reference_materials/notebook_inventory.json').read_text())
    draft_path = ROOT / 'reference_materials/draft_lessons.json'
    drafts = json.loads(draft_path.read_text(encoding='utf-8')) if draft_path.exists() else {}
    lookup = {entry['id']: entry for entry in inventory}
    count = 0
    for source in sorted((ROOT / 'lesson_sources').glob('*.lesson')):
        ident = source.stem
        record = lookup[ident]
        parts = re.split(r'^```python\s*\n(.*?)^```\s*$', source.read_text(encoding='utf-8'), flags=re.M | re.S)
        setup = nbformat.v4.new_code_cell("# Enable embedded figures in this fresh notebook kernel.\nfrom IPython import get_ipython\nget_ipython().run_line_magic('matplotlib', 'inline')")
        setup['id'] = f'{ident}-display-setup'
        cells = []
        for index, part in enumerate(parts):
            if not part.strip(): continue
            factory = nbformat.v4.new_code_cell if index % 2 else nbformat.v4.new_markdown_cell
            cell = factory(part.strip())
            cell['id'] = hashlib.sha256(f'{ident}:{index}:{part}'.encode()).hexdigest()[:12]
            cells.append(cell)
        cells.insert(1, setup)
        notebook = nbformat.v4.new_notebook(cells=cells, metadata={
            'kernelspec': {'name': 'ml-academy', 'language': 'python', 'display_name': 'Python (ML Academy .venv)'},
            'language_info': {'name': 'python'},
            'academy': {'id': ident, 'source': str(source.relative_to(ROOT)).replace('\\', '/'),
                        'prerequisites': record['prerequisites'], 'cpu': True, 'seed': 42},
        })
        if record.get('dependencies'):
            notebook.metadata.academy['dependencies'] = record['dependencies']
        if ident in drafts:
            notebook.metadata.academy['authoring_status'] = 'draft'
            notebook.metadata.academy['validation_policy'] = 'static-only'
        nbformat.validate(notebook)
        nbformat.write(notebook, ROOT / record['path'])
        count += 1
    render(inventory)
    print(f'Built {count} populated notebooks: {count-len(drafts)} authored lessons and {len(drafts)} explicit drafts. No cells executed.')

if __name__ == '__main__': build()
