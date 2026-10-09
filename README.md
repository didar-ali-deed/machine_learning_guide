# Complete Machine Learning Academy

[![Validate academy](https://github.com/didar-ali-deed/machine_learning_guide/actions/workflows/validate.yml/badge.svg)](https://github.com/didar-ali-deed/machine_learning_guide/actions/workflows/validate.yml)

A permanent, incremental self-study repository that begins with datasets and basic Python and progresses toward classical ML, neural networks, deployment, and nine capstones. This existing workspace is the project root; a second nested copy is unnecessary.

**Start with [START_HERE.md](START_HERE.md).** The [syllabus](SYLLABUS.md) links to all **427 notebook files across 24 modules**: **41 reviewed lessons and 386 incomplete, unexecuted drafts**. The [progress ledger](PROGRESS.md) distinguishes actual lessons, passing executions, and unfinished work. Drafts contain topic briefs and code starting points; the full university-level curriculum remains incomplete.

Use the [student guide](STUDENT_GUIDE.md) to study actively, the [GitHub setup guide](GITHUB_SETUP.md) to clone or connect the repository, and [contribution instructions](CONTRIBUTING.md) to add tested lessons. The project is published at [machine_learning_guide](https://github.com/didar-ali-deed/machine_learning_guide). The badge links to actual GitHub validation results.

## Study the first route

1. [What is Machine Learning?](00_Getting_Started/01_what_is_machine_learning.ipynb)
2. [Types and terminology](00_Getting_Started/02_machine_learning_types_and_terminology.ipynb)
3. [Python and Jupyter](00_Getting_Started/03_python_and_jupyter_introduction.ipynb)
4. [NumPy basics](01_Python_Foundations/13_numpy_basics.ipynb)
5. [Pandas basics](01_Python_Foundations/16_pandas_basics.ipynb)
6. [Visualizing data](01_Python_Foundations/18_visualizing_data.ipynb)
7. [Scalars, vectors and matrices](02_Mathematics_for_ML/07_scalars_vectors_and_matrices.ipynb)
8. [Functions and derivatives](02_Mathematics_for_ML/03_functions_and_derivatives.ipynb)

Each lesson includes manual arithmetic, executable examples, plots, six exercises with worked solutions, and answered knowledge/interview questions. Source notebooks are clean; executed evidence is stored under `reports/executed/`.

## Continue Python foundations

All **21 Python foundation lessons** are authored and tested. Follow the [numbered Python index](01_Python_Foundations/README.md) from variables through NumPy, pandas, plotting, and exploratory analysis. Each lesson includes a small worked example and exercises with solutions.

The first **17 mathematics lessons** are authored and tested. Follow the [mathematics index](02_Mathematics_for_ML/README.md) through SVD and limits. Every remaining module now has populated draft notebooks. The [generation report](reports/GENERATION_ONLY_REPORT.md) documents the files, static checks, and educational limitations. New drafts were not executed; automatic GitHub checks are static-only. Consult [PROGRESS.md](PROGRESS.md) for exact status.

## Navigate

- [Roadmap](ROADMAP.md), [learning objectives](LEARNING_OBJECTIVES.md), [36-week plan](STUDY_PLAN_36_WEEKS.md), [12-week plan](STUDY_PLAN_12_WEEKS.md).
- [Glossary](ML_GLOSSARY.md), [mathematics reference](MATHEMATICS_CHEATSHEET.md), [algorithm comparison](ALGORITHM_CHEATSHEET.md), [interview practice](INTERVIEW_QUESTIONS.md).
- [Exercises](exercises/README.md), [solutions](solutions/README.md), [assessment rubric](assessments/README.md).
- [Dependency strategy](reference_materials/DEPENDENCIES.md), [data policy](datasets/README.md), [references](reference_materials/REFERENCES.md).
- [Contributor and continuation rules](AGENTS.md), [content review](reports/CONTENT_REVIEW.md).

## Verification

To manually execute every notebook with live progress and saved JSON/CSV/HTML results, use [the all-notebook runner](RUN_ALL_NOTEBOOKS.md): `.\.venv\Scripts\python.exe run_all_notebooks.py`. This explicitly includes drafts and is separate from automatic static validation.

From PowerShell in this directory:

```powershell
.\.venv\Scripts\python.exe scripts\check_academy.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts\check_static_logic.py
.\.venv\Scripts\python.exe scripts\update_progress.py
```

The last command records evidence; it does not turn an unreviewed lesson into a verified one. Execution reports include source hashes, runtimes, cell counts, and plot counts. Structural checks cannot replace mathematical and pedagogical review.

Notebook execution is a manual opt-in; use `scripts/execute_notebooks.py --authored-only` only when intentionally changing the current generation-only policy.

The current examples are small, synthetic, and CPU-friendly. They require no paid API, data account, GPU, or optional plugin. Advanced notebooks are incomplete drafts, and expanded reference guides remain unfinished where the progress ledger says so.
