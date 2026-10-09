# Run every notebook and save the results

From PowerShell in `E:\machine_learning_basic_to_advance`, run:

```powershell
.\.venv\Scripts\python.exe run_all_notebooks.py
```

This single command selects **all 427 inventory notebooks, including drafts**, executes each in a fresh project kernel in syllabus order, and saves results. It continues after a notebook fails. Each notebook runs from its original module directory so relative data and helper paths retain their meaning. No optional package or system software is installed. Kernel setup is confined to the existing `.venv`.

The console shows overall completed count and percentage, pass/fail totals, current lesson, current code-cell position, and elapsed time. A five-second heartbeat shows that a long-running cell is still active. `progress.log` preserves the same progress messages. Individual cell outputs are saved in the notebooks and text logs; the console reports execution progress rather than streaming every output object.

## Saved results

Each invocation creates a separate directory such as:

```text
reports/runs/20261009T120000Z-a1b2c3d4/
├── index.html          # Auto-refreshing overview with links to saved results
├── results.json        # Status, source hashes, timings, errors and output paths
├── results.csv         # One row per notebook, convenient for Excel
├── progress.log        # Live progress history
├── logs/               # Text output and error details per notebook
└── executed/           # Module folders with executed .ipynb and .html copies
```

The script prints the actual directory. Open its `index.html` in a browser during or after the run. Running summaries refresh every five seconds. JSON, CSV, and summary files update as execution progresses. Each finished or failed notebook is saved immediately; failures and Ctrl+C preserve partial output where available. Not-yet-started notebooks remain explicitly pending. Source notebooks, historical `reports/executed/` copies, and the historical execution ledger are not overwritten. Runtime output folders are ignored by Git.

The per-cell timeout defaults to **120 seconds**; kernel startup has a separate 60-second timeout. Total run duration depends on notebook workloads. A missing optional package, an assertion failure, or a timeout is reported as a failure, with execution continuing to the next lesson. Individual HTML export problems are recorded as warnings while preserving the notebook and runtime result.

## Optional commands

Preview the complete selection without executing or modifying reports:

```powershell
.\.venv\Scripts\python.exe run_all_notebooks.py --list
```

Run a chosen subset:

```powershell
.\.venv\Scripts\python.exe run_all_notebooks.py --ids 00-01 02-18
```

Allow five minutes per cell or omit individual HTML exports:

```powershell
.\.venv\Scripts\python.exe run_all_notebooks.py --timeout 300
.\.venv\Scripts\python.exe run_all_notebooks.py --no-html
```

Press Ctrl+C to stop with partial reports. Starting the command again creates a new run; automatic resume is not implemented. The process exits with code 0 for a completed run without notebook failures, 1 for failures, and 130 for interruption.

## Meaning of a passing result

A runtime pass means selected nonempty code cells completed without reported errors. It does not establish mathematical correctness, full teaching depth, useful model performance, or production readiness. The **386 generated drafts remain incomplete drafts even if their code runs**. This runner records independent runtime evidence and does not promote lessons to educationally verified or alter `PROGRESS.md` automatically.

The runner was checked through syntax validation, dry-list selection, and infrastructure tests with simulated clients. Those tests exercise saving, partial failure, interruption, export warnings, and reporting without starting a real notebook kernel. The full 427-notebook run has **not** been started as part of creating this tool.
