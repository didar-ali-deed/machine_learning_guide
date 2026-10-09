"""Validate the generation-only safeguards without executing notebook code."""
import ast
import sys
import unittest
import tempfile
import json
import contextlib
import io
from unittest.mock import patch
import nbformat
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from check_static_logic import unbound_globals, keyword_errors, inspect_source
import update_progress
from academy_tools import source_hash


class StaticLogicTests(unittest.TestCase):
    def test_detects_unbound_name_in_nested_function(self):
        self.assertEqual(unbound_globals('def f(x):\n    return x + missing\n'), ['missing'])

    def test_accepts_imports_builtins_and_comprehension_locals(self):
        self.assertEqual(unbound_globals('import math\nvalues = [math.sqrt(x) for x in range(3)]\n'), [])

    def test_rejects_unknown_constructor_keyword(self):
        def constructor(alpha=1):
            return alpha
        call=ast.parse('Constructor(aphla=2)').body[0].value
        self.assertEqual(keyword_errors(call,constructor), ['aphla'])

    def test_detects_obvious_test_data_fitting(self):
        errors,_=inspect_source('model = object()\nX_test = []\nmodel.fit(X_test)\n')
        self.assertTrue(any('test-data fitting' in error for error in errors))

    def test_does_not_execute_parsed_code(self):
        errors,_=inspect_source("raise RuntimeError('must never execute')\n")
        self.assertEqual(errors, [])

    def test_draft_cannot_be_promoted_by_execution_and_review_records(self):
        with tempfile.TemporaryDirectory() as temporary:
            root=Path(temporary)
            (root/'reports').mkdir()
            (root/'02_Math').mkdir()
            record={'id':'02-18','module':'02','path':'02_Math/draft.ipynb',
                    'title':'Derivatives','optional':False}
            notebook=nbformat.v4.new_notebook(metadata={'academy':{'authoring_status':'draft'}})
            nbformat.write(notebook,root/record['path'])
            digest=source_hash(notebook)
            (root/'reports/execution_results.json').write_text(json.dumps({'notebooks':{'02-18':{'status':'passed','source_sha256':digest}}}))
            (root/'reports/content_review.json').write_text(json.dumps({'02-18':{'source_sha256':digest}}))
            with patch.object(update_progress,'ROOT',root), patch.object(update_progress,'inventory',return_value=[record]), contextlib.redirect_stdout(io.StringIO()):
                update_progress.main()
            progress=(root/'PROGRESS.md').read_text(encoding='utf-8')
            self.assertIn('Executed and reviewed at the current source hash: **0**',progress)
            self.assertIn('Generated draft; unexecuted and incomplete (1)',progress)
