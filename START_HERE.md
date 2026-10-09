# Start here

Read the first lesson without trying to understand every library call immediately. Predict the hand calculation, execute the code, inspect the result, and then alter one input. Attempt the exercises before opening section 18. The introductory route is a preview of useful ideas; the full Python and mathematics sequences supply further practice before algorithm study.

## Environment actually checked

| Tool | System result | Project result |
|---|---|---|
| Python | 3.11.9, Windows x64; meets 3.11+ | Isolated `.venv`, same interpreter version |
| pip | 26.2.1 available | 24.0 in `.venv`; dependencies installed successfully |
| Git | 2.55.0.windows.5 available | `main` tracks the user's GitHub repository; commits published |
| Jupyter Notebook | 7.6.2 available globally | 7.6.3 installed locally |

No required system tool is missing; no system-level installation is needed. The `py` launcher exists but `py --list-paths` reported no installed Pythons. Use the working `python` command or the explicit `.venv` interpreter below. The environment smoke notebook actually executed four code cells successfully; its local generated report is `artifacts/environment-check.json`. Run the environment verifier below to recreate that ignored artifact in a fresh checkout.

## Open the academy on this Windows machine

```powershell
Set-Location 'E:\machine_learning_basic_to_advance'
.\.venv\Scripts\python.exe -m notebook
```

Open a numbered lesson and select **Python (ML Academy .venv)** as its kernel. Shift+Enter executes a cell. Restart the kernel and run all cells to check independence from previous sessions. Stop the notebook server in its terminal with Ctrl+C when finished. Authentication remains enabled; use the local URL the server prints.

## Reproduce the environment in a fresh checkout

Run these commands from the repository directory with a working 64-bit Python 3.11 installation. The pinned lock was tested with Python 3.11.9 on Windows; other platforms or Python minor versions are not claimed as verified.

```powershell
python --version
python -m venv .venv
.\.venv\Scripts\python.exe -m pip --isolated install --index-url https://pypi.org/simple --only-binary=:all: --no-cache-dir -r requirements.txt
.\.venv\Scripts\python.exe scripts\verify_environment.py
.\.venv\Scripts\python.exe scripts\check_academy.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts\execute_notebooks.py
```

Stop and read an error if any command fails. `verify_environment.py` registers the kernel inside `.venv`, verifies package consistency, executes the smoke notebook, and records the actual kernel executable. It does not register a system-wide or user-wide kernel. The verification scripts keep runtime caches inside ignored project directories.

Activation is optional when using the interpreter path directly, as explained in the [Python venv documentation](https://docs.python.org/3.11/library/venv.html). No PowerShell execution-policy change is needed for these commands. Package installation follows the [Jupyter installation documentation](https://jupyter.org/install).

## Work through a lesson

1. Read objectives and prerequisites. Follow the [eight-lesson route](README.md) before returning to the complete numbered syllabus.
2. Calculate the tiny example without running the code. Write units beside each answer.
3. Run from a clean kernel. For each output, explain why it follows from the input.
4. Change one setting and predict the effect first. Restore the original values afterward.
5. Complete all six exercises. Record reasoning, not just final numbers.
6. Use the [assessment rubric](assessments/README.md) to decide whether to revisit a prerequisite.

Do not equate reading a notebook with mastering it. The [progress file](PROGRESS.md) tracks repository construction, not your personal learning completion. Keep personal notes separately so those meanings stay distinct.
