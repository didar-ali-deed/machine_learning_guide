# Complete Machine Learning Academy

A permanent, incremental self-study repository that begins with datasets and basic Python and progresses toward classical ML, neural networks, deployment, and nine capstones. This existing workspace is the project root; a second nested copy is unnecessary.

**Start with [START_HERE.md](START_HERE.md).** The [syllabus](SYLLABUS.md) preserves all 427 planned notebooks across 24 modules. The [progress ledger](PROGRESS.md) distinguishes actual lessons, passing executions, and unfinished work. Module specification pages are plans, not completed tutorials.

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

The full Python sequence is available through [Classes and object-oriented programming](01_Python_Foundations/12_classes_and_object_oriented_programming.ipynb): [variables](01_Python_Foundations/01_variables_and_data_types.ipynb), [operators](01_Python_Foundations/02_operators.ipynb), [strings](01_Python_Foundations/03_strings.ipynb), [containers](01_Python_Foundations/04_lists_tuples_sets_and_dictionaries.ipynb), [conditions and loops](01_Python_Foundations/05_conditions_and_loops.ipynb), [functions](01_Python_Foundations/06_functions_and_parameters.ipynb), [scope](01_Python_Foundations/07_scope.ipynb), [comprehensions](01_Python_Foundations/08_list_comprehensions.ipynb), [modules](01_Python_Foundations/09_modules_and_packages.ipynb), [file handling](01_Python_Foundations/10_file_handling.ipynb), and [debugging](01_Python_Foundations/11_exceptions_and_debugging.ipynb). The next planned batch covers indexing/slicing/shapes, vectorization/broadcasting, and filtering/grouping/merging. See the [latest batch report](reports/PYTHON_FILES_DEBUGGING_CLASSES_REPORT.md).

## Navigate

- [Roadmap](ROADMAP.md), [learning objectives](LEARNING_OBJECTIVES.md), [36-week plan](STUDY_PLAN_36_WEEKS.md), [12-week plan](STUDY_PLAN_12_WEEKS.md).
- [Glossary](ML_GLOSSARY.md), [mathematics reference](MATHEMATICS_CHEATSHEET.md), [algorithm comparison](ALGORITHM_CHEATSHEET.md), [interview practice](INTERVIEW_QUESTIONS.md).
- [Exercises](exercises/README.md), [solutions](solutions/README.md), [assessment rubric](assessments/README.md).
- [Dependency strategy](reference_materials/DEPENDENCIES.md), [data policy](datasets/README.md), [references](reference_materials/REFERENCES.md).
- [Contributor and continuation rules](AGENTS.md), [content review](reports/CONTENT_REVIEW.md).

## Verification

From PowerShell in this directory:

```powershell
.\.venv\Scripts\python.exe scripts\check_academy.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
.\.venv\Scripts\python.exe scripts\execute_notebooks.py
.\.venv\Scripts\python.exe scripts\update_progress.py
```

The last command records evidence; it does not turn an unreviewed lesson into a verified one. Execution reports include source hashes, runtimes, cell counts, and plot counts. Structural checks cannot replace mathematical and pedagogical review.

The current examples are small, synthetic, and CPU-friendly. They require no paid API, data account, GPU, or optional plugin. Advanced modules and expanded reference guides remain planned where the progress ledger says so.
