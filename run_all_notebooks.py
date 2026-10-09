"""Run the academy inventory with live progress and durable per-run results.

PowerShell: .\.venv\Scripts\python.exe run_all_notebooks.py
This is an explicit manual execution command. Importing it or using --list
does not start kernels. Curriculum sources and historical evidence stay intact.
"""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import html
import io
import json
from pathlib import Path
import subprocess
import sys
import threading
import time
import uuid

import nbformat
from nbclient import NotebookClient
from nbconvert import HTMLExporter
from jupyter_client import KernelManager
from jupyter_client.kernelspec import KernelSpecManager

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
from academy_tools import (configure_local_runtime, inventory, source_hash,
                           local_dependency_hashes, relocate_markdown_links)


def utc_now():
    return datetime.now(timezone.utc).isoformat()


def atomic_text(path, content):
    """Replace a closed temporary file so interruption leaves the last report."""
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + '.tmp')
    temporary.write_text(content, encoding='utf-8')
    temporary.replace(path)


class LiveProgress:
    """A lightweight console heartbeat, plus a durable chronological log."""
    def __init__(self, total, directory, interval=5):
        self.total = total
        self.directory = Path(directory)
        self.started = time.monotonic()
        self.state = {'finished': 0, 'passed': 0, 'failed': 0, 'current': 'preparing',
                      'cell': 0, 'cells': 0}
        self.lock = threading.Lock()
        self.stop = threading.Event()
        self.interval = interval
        self.thread = None

    def update(self, **values):
        with self.lock:
            self.state.update(values)

    def emit(self, event):
        with self.lock:
            state = self.state.copy()
            fraction = state['finished'] / self.total if self.total else 1
            filled = int(20*fraction)
            bar = '#' * filled + '-' * (20-filled)
            elapsed = time.monotonic() - self.started
            line = (f"[{bar}] {state['finished']}/{self.total} ({100*fraction:5.1f}%) "
                    f"PASS {state['passed']} FAIL {state['failed']} | {state['current']} "
                    f"cell {state['cell']}/{state['cells']} | {elapsed:.0f}s | {event}")
            print(line, flush=True)
            with (self.directory/'progress.log').open('a', encoding='utf-8') as log:
                log.write(utc_now() + ' ' + line + '\n')

    def start(self):
        def heartbeat():
            while not self.stop.wait(self.interval):
                self.emit('still running')
        self.thread = threading.Thread(target=heartbeat, name='academy-progress', daemon=True)
        self.thread.start()

    def close(self):
        self.stop.set()
        if self.thread:
            self.thread.join(timeout=2)


def save_reports(directory, report):
    """Persist JSON, CSV, and a browser-readable auto-refreshing summary."""
    directory = Path(directory)
    report['updated_at_utc'] = utc_now()
    atomic_text(directory/'results.json', json.dumps(report, indent=2) + '\n')
    output = io.StringIO(newline='')
    fields = ['id', 'title', 'status', 'authoring_status', 'code_cells',
              'executed_cells', 'figures', 'seconds', 'output', 'html', 'error']
    writer = csv.DictWriter(output, fieldnames=fields, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(report['notebooks'].values())
    atomic_text(directory/'results.csv', output.getvalue())
    rows = []
    counts = {}
    for item in report['notebooks'].values():
        status = item['status']
        counts[status] = counts.get(status, 0) + 1
        links = []
        for key, label in [('output','Notebook'), ('html','HTML'), ('log','Log')]:
            if item.get(key):
                links.append(f'<a href="{html.escape(item[key], quote=True)}">{label}</a>')
        values = [item['id'], item['title'], status, item.get('authoring_status',''),
                  f"{item.get('executed_cells',0)}/{item.get('code_cells',0)}",
                  str(item.get('seconds','')), item.get('error','')]
        rows.append('<tr>' + ''.join('<td>'+html.escape(str(v))+'</td>' for v in values)
                    + '<td>'+' · '.join(links)+'</td></tr>')
    refresh = '<meta http-equiv="refresh" content="5">' if report['status']=='running' else ''
    page = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">{refresh}
<title>Academy notebook run</title><style>
body{{font:15px system-ui;margin:24px}}table{{border-collapse:collapse;width:100%}}
td,th{{border:1px solid #ddd;padding:8px;text-align:left;vertical-align:top}}
th{{background:#eee}}td:nth-child(7){{max-width:420px;white-space:pre-wrap}}
</style></head><body><h1>Academy notebook execution</h1>
<p>Run {html.escape(report['run_id'])}: {html.escape(report['status'])}.
{html.escape(', '.join(f'{key}: {value}' for key,value in counts.items()))}</p>
<p>Updated {html.escape(report['updated_at_utc'])}. Running summaries refresh every five seconds.</p>
<p>A runtime pass does not establish full educational quality. Draft status remains unchanged.</p>
<p><a href="results.csv">CSV</a> · <a href="results.json">JSON</a> · <a href="progress.log">Live log</a></p>
<table><thead><tr><th>ID</th><th>Lesson</th><th>Runtime status</th><th>Authoring status</th>
<th>Executed cells</th><th>Seconds</th><th>Error</th><th>Saved results</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></body></html>"""
    atomic_text(directory/'index.html', page)


def output_log(notebook, error=''):
    lines = []
    for index, cell in enumerate(notebook.cells):
        if cell.cell_type != 'code':
            continue
        lines.append(f'\n--- Code cell at notebook index {index} ---\n')
        for output in cell.get('outputs', []):
            if output.output_type == 'stream':
                lines.append(output.text)
            elif output.output_type == 'error':
                lines.append(f"{output.ename}: {output.evalue}\n")
                lines.extend(str(line)+'\n' for line in output.get('traceback', []))
            elif 'text/plain' in output.get('data', {}):
                lines.append(output.data['text/plain']+'\n')
    if error:
        lines.append('\nRunner error: '+error+'\n')
    return ''.join(lines)


def execute_one(record, directory, timeout, progress, checkpoint,
                kernel_manager, make_client=NotebookClient, export_html=True):
    """Save successful or partial execution; errors never discard earlier output."""
    started = time.monotonic()
    result = {'id':record['id'], 'title':record['title'], 'path':record['path'],
              'status':'running', 'started_at_utc':utc_now(), 'executed_cells':0}
    notebook = None
    checkpoint(result)
    try:
        notebook = nbformat.read(ROOT/record['path'], as_version=4)
        nbformat.validate(notebook)
        result['source_sha256'] = source_hash(notebook)
        result['dependencies_sha256'] = local_dependency_hashes(notebook)
        result['authoring_status'] = notebook.metadata.get('academy', {}).get('authoring_status', 'authored')
        for cell in notebook.cells:
            if cell.cell_type == 'code':
                cell.outputs = []
                cell.execution_count = None
        indices = [i for i,c in enumerate(notebook.cells) if c.cell_type=='code' and c.source.strip()]
        result['code_cells'] = len(indices)
        if not indices:
            raise ValueError('No nonempty code cells to execute.')
        positions = {index: number for number,index in enumerate(indices,1)}
        progress.update(current=record['id'], cell=0, cells=len(indices))
        progress.emit('START '+record['title'])
        checkpoint(result)

        def cell_start(cell, cell_index, **kwargs):
            if cell_index in positions:
                progress.update(cell=positions[cell_index])
                progress.emit('executing cell')

        def cell_done(cell, cell_index, **kwargs):
            if cell_index in positions:
                result['executed_cells'] = sum(c.execution_count is not None for c in notebook.cells if c.cell_type=='code')
                result['seconds'] = round(time.monotonic()-started,2)
                checkpoint(result)

        client = make_client(notebook, km=kernel_manager, timeout=timeout,
                             startup_timeout=60, allow_errors=False,
                             resources={'metadata':{'path':str((ROOT/record['path']).parent)}},
                             on_cell_start=cell_start, on_cell_executed=cell_done)
        client.execute(cleanup_kc=True)
        cells = [notebook.cells[index] for index in indices]
        if any(c.execution_count is None for c in cells):
            raise RuntimeError('Some code cells did not execute.')
        if any(o.output_type=='error' for c in cells for o in c.outputs):
            raise RuntimeError('A cell returned an error output.')
        result['status'] = 'passed'
    except KeyboardInterrupt:
        result.update(status='interrupted', error='Stopped by Ctrl+C; partial outputs preserved.')
    except Exception as exc:
        result.update(status='failed', error=f'{type(exc).__name__}: {exc}')
    finally:
        if notebook is not None:
            destination = Path(directory)/'executed'/record['path']
            try:
                result['executed_cells'] = sum(c.execution_count is not None for c in notebook.cells if c.cell_type=='code')
                result['figures'] = sum('image/png' in o.get('data',{}) for c in notebook.cells if c.cell_type=='code' for o in c.outputs)
                for cell in notebook.cells:
                    if cell.cell_type=='markdown':
                        cell.source = relocate_markdown_links(cell.source, ROOT/record['path'], destination)
                atomic_text(destination, nbformat.writes(notebook))
                result['output'] = destination.relative_to(directory).as_posix()
                log_path = Path(directory)/'logs'/f'{record["id"]}.txt'
                atomic_text(log_path, output_log(notebook, result.get('error','')))
                result['log'] = log_path.relative_to(directory).as_posix()
                if export_html:
                    try:
                        body,_ = HTMLExporter().from_notebook_node(notebook)
                        html_path = destination.with_suffix('.html')
                        atomic_text(html_path, body)
                        result['html'] = html_path.relative_to(directory).as_posix()
                    except Exception as exc:
                        result['html_warning'] = f'{type(exc).__name__}: {exc}'
            except Exception as exc:
                result.update(status='failed', error=result.get('error','') + f' Saving outputs failed: {exc}')
        result['seconds'] = round(time.monotonic()-started,2)
        result['finished_at_utc'] = utc_now()
        checkpoint(result)
    return result


def positive_seconds(value):
    number = int(value)
    if number <= 0:
        raise argparse.ArgumentTypeError('Timeout must be a positive number of seconds.')
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--ids', nargs='+', help='Optional subset of inventory IDs; default: all notebooks, including drafts')
    parser.add_argument('--timeout', type=positive_seconds, default=120, help='Per-cell timeout in seconds (default: 120)')
    parser.add_argument('--no-html', action='store_true', help='Save notebooks, logs and summaries without individual HTML exports')
    parser.add_argument('--list', action='store_true', help='List the selected notebooks without running kernels or changing reports')
    args = parser.parse_args(argv)
    records = inventory()
    known = {r['id'] for r in records}
    if args.ids and set(args.ids)-known:
        parser.error(f'Unknown IDs: {sorted(set(args.ids)-known)}')
    selected = [r for r in records if not args.ids or r['id'] in args.ids]
    if args.list:
        for record in selected:
            print(record['id'], record['title'])
        print(f'{len(selected)} selected; zero notebook cells executed.')
        return 0
    expected = ROOT/'.venv'/('Scripts/python.exe' if sys.platform=='win32' else 'bin/python')
    if Path(sys.executable).resolve()!=expected.resolve():
        parser.error('Use the project interpreter: .\\.venv\\Scripts\\python.exe run_all_notebooks.py')
    configure_local_runtime()
    # This installs a kernel specification inside .venv, not system software.
    subprocess.run([sys.executable,'-m','pip','check'],check=True)
    subprocess.run([sys.executable,'-m','ipykernel','install','--prefix',sys.prefix,
                    '--name','ml-academy','--display-name','Python (ML Academy .venv)'],check=True)
    specs = KernelSpecManager(kernel_dirs=[str(Path(sys.prefix)/'share/jupyter/kernels')],ensure_native_kernel=False)
    if Path(specs.get_kernel_spec('ml-academy').argv[0]).resolve()!=expected.resolve():
        raise RuntimeError('Kernel specification points outside the project interpreter.')
    run_id = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')+'-'+uuid.uuid4().hex[:8]
    directory = ROOT/'reports/runs'/run_id
    directory.mkdir(parents=True,exist_ok=False)
    report = {'run_id':run_id,'status':'running','started_at_utc':utc_now(),
              'python':sys.version,'interpreter':sys.executable,'cell_timeout_seconds':args.timeout,
              'notebooks':{r['id']:{'id':r['id'],'title':r['title'],'status':'pending'} for r in selected},
              'limitation':'Runtime success does not establish full educational review. Source notebooks and historical reports are not overwritten.'}
    save_reports(directory,report)
    print(f'Results: {directory}\nLive browser summary: {directory / "index.html"}',flush=True)
    progress = LiveProgress(len(selected),directory)
    progress.start()
    interrupted = False
    passed = failed = 0

    def checkpoint(result):
        report['notebooks'][result['id']] = result.copy()
        save_reports(directory,report)

    try:
        for number,record in enumerate(selected,1):
            km = KernelManager(kernel_name='ml-academy',kernel_spec_manager=specs)
            result = execute_one(record,directory,args.timeout,progress,checkpoint,km,
                                 export_html=not args.no_html)
            if result['status']=='interrupted':
                interrupted = True
                break
            passed += result['status']=='passed'
            failed += result['status']=='failed'
            progress.update(finished=number,passed=passed,failed=failed)
            progress.emit(result['status'].upper())
    except KeyboardInterrupt:
        interrupted = True
    except Exception as exc:
        report['runner_error'] = f'{type(exc).__name__}: {exc}'
    finally:
        progress.close()
        report['status'] = 'interrupted' if interrupted else ('failed' if failed or report.get('runner_error') else 'completed')
        report['finished_at_utc'] = utc_now()
        report['counts'] = {status:sum(r['status']==status for r in report['notebooks'].values())
                            for status in ['passed','failed','interrupted','pending','running']}
        save_reports(directory,report)
        print(f"\nRun {report['status']}: {report['counts']}\nOpen {directory/'index.html'}",flush=True)
    return 130 if interrupted else (1 if report['status']=='failed' else 0)


if __name__ == '__main__':
    raise SystemExit(main())
