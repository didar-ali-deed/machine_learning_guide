"""Small shared utilities for inventory checks and evidence-based status."""
import hashlib
import json
import os
import re
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parents[1]

def inventory():
    return json.loads((ROOT / 'reference_materials/notebook_inventory.json').read_text(encoding='utf-8'))

def source_hash(notebook):
    payload = [(c.cell_type, c.source) for c in notebook.cells]
    payload.append(('academy', json.dumps(notebook.metadata.get('academy', {}), sort_keys=True)))
    payload.extend((f'dependency:{relative}', digest) for relative, digest in local_dependency_hashes(notebook).items())
    return hashlib.sha256(json.dumps(payload, ensure_ascii=False).encode()).hexdigest()

def local_dependency_hashes(notebook):
    """Fingerprint explicitly declared local imports alongside notebook sources."""
    result = {}
    for relative in sorted(notebook.metadata.get('academy', {}).get('dependencies', [])):
        target = (ROOT / relative).resolve()
        if Path(relative).is_absolute() or not target.is_relative_to(ROOT.resolve()):
            raise ValueError(f'Local dependency must stay within the repository: {relative}')
        result[relative] = hashlib.sha256(target.read_bytes()).hexdigest()
    return result

def configure_local_runtime():
    for name, relative in {'JUPYTER_CONFIG_DIR':'.jupyter/config', 'JUPYTER_DATA_DIR':'.jupyter/data',
                          'JUPYTER_RUNTIME_DIR':'.jupyter/runtime', 'IPYTHONDIR':'.ipython',
                          'MPLCONFIGDIR':'.matplotlib'}.items():
        path = ROOT / relative
        path.mkdir(parents=True, exist_ok=True)
        os.environ[name] = str(path)
    os.environ['PYTHONNOUSERSITE'] = '1'
    os.environ['MPLBACKEND'] = 'Agg'
    os.environ['PYTHONHASHSEED'] = '42'
    os.environ['OMP_NUM_THREADS'] = '1'
    os.environ['OPENBLAS_NUM_THREADS'] = '1'

def relocate_markdown_links(text, source_path, destination_path):
    """Keep local lesson navigation working in the archived executed copy."""
    def replace(match):
        label, destination = match.groups()
        url = urlsplit(destination)
        if url.scheme or url.netloc or not url.path:
            return match.group(0)
        target = (source_path.parent / unquote(url.path)).resolve()
        # Resolve both sides: Windows TEMP may use a short-name alias while
        # resolve() expands the target to its long path on GitHub runners.
        relative = os.path.relpath(target, destination_path.parent.resolve()).replace('\\', '/')
        if url.fragment: relative += '#' + url.fragment
        return f'[{label}]({relative})'
    return re.sub(r'\[([^\]]*)\]\(([^)]+)\)', replace, text)
