# Contributing to the academy

Read [AGENTS.md](AGENTS.md) for the educational contract and [PROGRESS.md](PROGRESS.md) before selecting work. Preserve the inventory; implement a small coherent batch. A notebook title or filled generic template is not a delivered lesson.

Edit `lesson_sources/<id>.lesson`. Fenced Python blocks become executable cells. Define symbols, units, shapes, assumptions, and manual examples. Include six reasoning exercises with worked solutions. Use synthetic or built-in data, CPU execution, deterministic seeds where randomness is used, and no mandatory downloads.

From PowerShell in the repository:

```powershell
.\.venv\Scripts\python.exe scripts/build_notebooks.py
.\.venv\Scripts\python.exe scripts/check_academy.py
.\.venv\Scripts\python.exe scripts/execute_notebooks.py --ids 01-14
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

Replace the selected ID with the lessons you changed. Inspect their printed outputs, formulas, plots, exercises, and answers. Record that specific review in `reports/CONTENT_REVIEW.md` and `reports/content_review.json`, using the current execution source hash. Then run `scripts/update_progress.py` and the structural check again. An unchanged old passing execution cannot verify a newly edited lesson.

Keep source notebooks free of outputs. Keep executed evidence in `reports/`. Do not commit `.venv`, runtime caches, credentials, or personal study notes. Commit each reviewed lesson or coherent tested batch with a message describing the actual work. Do not amend or rewrite another contributor's history to disguise untested changes.

The [GitHub workflow](https://github.com/didar-ali-deed/machine_learning_guide/actions/workflows/validate.yml) runs the checks and authored notebooks on Windows with Python 3.11.9. Inspect its actual result for the commit under review. Automated success does not replace educational review. Public licensing has not been selected; do not assume an open-source license merely because a repository is hosted on GitHub.
