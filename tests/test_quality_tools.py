"""Test evidence and validation behaviors that protect truthful curriculum status."""
import sys
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
import nbformat
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from academy_tools import source_hash, relocate_markdown_links
from check_academy import broken_links, validate_graph

class EvidenceTests(unittest.TestCase):
    def test_imported_module_edit_invalidates_execution_evidence(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            dependency = root / 'helper.py'
            dependency.write_text('value = 1\n', encoding='utf-8')
            notebook = nbformat.v4.new_notebook(metadata={'academy': {'dependencies': ['helper.py']}})
            with patch('academy_tools.ROOT', root):
                before = source_hash(notebook)
                dependency.write_text('value = 2\n', encoding='utf-8')
                self.assertNotEqual(before, source_hash(notebook))

    def test_dependency_cannot_escape_repository(self):
        with tempfile.TemporaryDirectory() as temporary:
            notebook = nbformat.v4.new_notebook(metadata={'academy': {'dependencies': ['../outside.py']}})
            with patch('academy_tools.ROOT', Path(temporary)), self.assertRaisesRegex(ValueError, 'within the repository'):
                source_hash(notebook)

    def test_code_edit_invalidates_execution_evidence(self):
        notebook = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell('x = 1')])
        before = source_hash(notebook)
        notebook.cells[0].source = 'x = 2'
        self.assertNotEqual(before, source_hash(notebook))

    def test_explanatory_edit_also_invalidates_evidence(self):
        notebook = nbformat.v4.new_notebook(cells=[nbformat.v4.new_markdown_cell('Two rows.')])
        before = source_hash(notebook)
        notebook.cells[0].source = 'Three rows.'
        self.assertNotEqual(before, source_hash(notebook))

    def test_execution_outputs_do_not_change_source_hash(self):
        notebook = nbformat.v4.new_notebook(cells=[nbformat.v4.new_code_cell('print(1)')])
        before = source_hash(notebook)
        notebook.cells[0].execution_count = 1
        notebook.cells[0].outputs = [nbformat.v4.new_output('stream', name='stdout', text='1\n')]
        self.assertEqual(before, source_hash(notebook))

class PrerequisiteTests(unittest.TestCase):
    def test_cycle_rejected(self):
        with self.assertRaisesRegex(ValueError, 'cycle'):
            validate_graph([{'id':'a','path':'a.ipynb','prerequisites':['b']}, {'id':'b','path':'b.ipynb','prerequisites':['a']}])

    def test_missing_prerequisite_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Unknown'):
            validate_graph([{'id':'a','path':'a.ipynb','prerequisites':['missing']}])

    def test_valid_prerequisite_chain(self):
        validate_graph([{'id':'a','path':'a.ipynb','prerequisites':[]}, {'id':'b','path':'b.ipynb','prerequisites':['a']}])

class LinkTests(unittest.TestCase):
    def test_archived_notebook_keeps_original_link_target(self):
        root = Path(tempfile.gettempdir()) / 'academy-link-test'
        source = root/'00_Module/lesson.ipynb'
        destination = root/'reports/executed/00_Module/lesson.ipynb'
        relocated = relocate_markdown_links('[next](../01_Module/next.ipynb#topic)', source, destination)
        self.assertEqual(relocated, '[next](../../../01_Module/next.ipynb#topic)')

    def test_missing_file_and_anchor_are_reported(self):
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary)/'lesson.md'
            path.write_text('# Real heading\n[missing](absent.md)\n[bad anchor](#absent)\n', encoding='utf-8')
            self.assertEqual(len(broken_links(path)), 2)

    def test_existing_relative_file_and_anchor_pass(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root/'target.md').write_text('<a id="00-01"></a>\n# Topic\n', encoding='utf-8')
            path = root/'source.md'
            path.write_text('[target](target.md#00-01)\n[heading](target.md#topic)\n', encoding='utf-8')
            self.assertEqual(broken_links(path), [])

if __name__ == '__main__': unittest.main()
