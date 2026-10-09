"""Exercise runner reporting and failures without starting notebook kernels."""
import contextlib
import io
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

import nbformat
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import run_all_notebooks as runner


class FakeProgress:
    def __init__(self):
        self.events=[]
        self.values={}
    def update(self,**values):
        self.values.update(values)
    def emit(self,event):
        self.events.append(event)


def simulated_client(mode):
    class Client:
        def __init__(self,notebook,**options):
            self.notebook=notebook
            self.options=options
        def execute(self,**kwargs):
            number=0
            for index,cell in enumerate(self.notebook.cells):
                if cell.cell_type!='code':
                    continue
                number+=1
                self.options['on_cell_start'](cell=cell,cell_index=index)
                cell.execution_count=number
                cell.outputs=[nbformat.v4.new_output('stream',name='stdout',text=f'Simulated output {number}\n')]
                if number==2 and mode=='fail':
                    cell.outputs=[nbformat.v4.new_output('error',ename='AssertionError',evalue='simulated failure',traceback=[])]
                self.options['on_cell_executed'](cell=cell,cell_index=index)
                if number==2 and mode=='fail':
                    raise RuntimeError('simulated failure')
                if number==1 and mode=='interrupt':
                    raise KeyboardInterrupt()
            return self.notebook
    return Client


class BatchRunnerTests(unittest.TestCase):
    def run_simulation(self,root,mode,export_html=False):
        source=root/'00_Lessons/lesson.ipynb'
        source.parent.mkdir()
        notebook=nbformat.v4.new_notebook(cells=[
            nbformat.v4.new_markdown_cell('[Reference](../reference.md)'),
            nbformat.v4.new_code_cell("raise RuntimeError('This source must never really execute')"),
            nbformat.v4.new_code_cell('answer = 42')],
            metadata={'academy':{'authoring_status':'draft'}})
        nbformat.write(notebook,source)
        (root/'reference.md').write_text('Reference',encoding='utf-8')
        original=source.read_bytes()
        directory=root/'reports/runs/test'
        directory.mkdir(parents=True)
        record={'id':'00-01','title':'Example','path':'00_Lessons/lesson.ipynb'}
        checkpoints=[]
        progress=FakeProgress()
        with patch.object(runner,'ROOT',root):
            result=runner.execute_one(record,directory,15,progress,
                lambda item:checkpoints.append(item.copy()),object(),
                make_client=simulated_client(mode),export_html=export_html)
        self.assertEqual(original,source.read_bytes())
        self.assertEqual(result['authoring_status'],'draft')
        self.assertTrue((directory/result['output']).exists())
        self.assertTrue((directory/result['log']).exists())
        return result,checkpoints,progress,directory

    def test_pass_saves_outputs_without_requiring_figures(self):
        with tempfile.TemporaryDirectory() as location:
            result,checkpoints,progress,directory=self.run_simulation(Path(location),'pass')
            self.assertEqual(result['status'],'passed')
            self.assertEqual(result['executed_cells'],2)
            self.assertEqual(result['figures'],0)
            self.assertEqual(progress.values['cell'],2)
            self.assertTrue(any(c.get('executed_cells')==1 for c in checkpoints))

    def test_failure_preserves_partial_notebook_and_error_log(self):
        with tempfile.TemporaryDirectory() as location:
            result,_,_,directory=self.run_simulation(Path(location),'fail')
            self.assertEqual(result['status'],'failed')
            saved=nbformat.read(directory/result['output'],as_version=4)
            self.assertIn('Simulated output',saved.cells[1].outputs[0].text)
            self.assertEqual(saved.cells[2].outputs[0].output_type,'error')
            self.assertIn('simulated failure',(directory/result['log']).read_text(encoding='utf-8'))

    def test_interrupt_preserves_first_cell_output(self):
        with tempfile.TemporaryDirectory() as location:
            result,_,_,_=self.run_simulation(Path(location),'interrupt')
            self.assertEqual(result['status'],'interrupted')
            self.assertEqual(result['executed_cells'],1)

    def test_export_failure_does_not_turn_runtime_pass_into_failure(self):
        with tempfile.TemporaryDirectory() as location, patch.object(runner,'HTMLExporter',side_effect=ValueError('export unavailable')):
            result,_,_,_=self.run_simulation(Path(location),'pass',export_html=True)
            self.assertEqual(result['status'],'passed')
            self.assertIn('export unavailable',result['html_warning'])

    def test_report_preserves_pending_lessons_and_escapes_html(self):
        with tempfile.TemporaryDirectory() as location:
            report={'run_id':'test','status':'running','notebooks':{
                'a':{'id':'a','title':'<script>example</script>','status':'failed','error':'<bad>'},
                'b':{'id':'b','title':'Not started','status':'pending'}}}
            runner.save_reports(Path(location),report)
            saved=json.loads((Path(location)/'results.json').read_text(encoding='utf-8'))
            self.assertEqual(saved['notebooks']['b']['status'],'pending')
            html=(Path(location)/'index.html').read_text(encoding='utf-8')
            self.assertIn('&lt;script&gt;',html)
            self.assertNotIn('<script>example',html)
            self.assertIn('http-equiv="refresh"',html)

    def test_list_never_launches_subprocesses(self):
        with patch.object(runner.subprocess,'run',side_effect=AssertionError('must not launch')), contextlib.redirect_stdout(io.StringIO()) as output:
            self.assertEqual(runner.main(['--list','--ids','00-01']),0)
            self.assertIn('zero notebook cells executed',output.getvalue())

    def test_rejects_nonpositive_cell_timeout(self):
        import argparse
        with self.assertRaises(argparse.ArgumentTypeError):
            runner.positive_seconds('0')

    def test_batch_continues_after_one_notebook_fails(self):
        with tempfile.TemporaryDirectory() as location:
            root=Path(location)
            expected=root/'.venv'/('Scripts/python.exe' if sys.platform=='win32' else 'bin/python')
            records=[{'id':'a','title':'First','path':'first.ipynb'},
                     {'id':'b','title':'Second','path':'second.ipynb'}]
            visited=[]
            def fake_execute(record,directory,timeout,progress,checkpoint,km,**kwargs):
                visited.append(record['id'])
                result={'id':record['id'],'title':record['title'],
                        'status':'failed' if record['id']=='a' else 'passed'}
                checkpoint(result)
                return result
            spec=SimpleNamespace(argv=[str(expected)])
            with patch.object(runner,'ROOT',root), patch.object(runner,'inventory',return_value=records), \
                 patch.object(runner.sys,'executable',str(expected)), patch.object(runner,'configure_local_runtime'), \
                 patch.object(runner.subprocess,'run'), patch.object(runner,'KernelSpecManager') as specs, \
                 patch.object(runner,'KernelManager'), patch.object(runner,'execute_one',side_effect=fake_execute), \
                 contextlib.redirect_stdout(io.StringIO()):
                specs.return_value.get_kernel_spec.return_value=spec
                self.assertEqual(runner.main(['--no-html']),1)
            self.assertEqual(visited,['a','b'])
            report_path=next((root/'reports/runs').glob('*/results.json'))
            report=json.loads(report_path.read_text(encoding='utf-8'))
            self.assertEqual(report['counts']['passed'],1)
            self.assertEqual(report['counts']['failed'],1)
            self.assertEqual(report['counts']['pending'],0)
