# Complete Machine Learning Academy

[![Validate academy](https://github.com/didar-ali-deed/machine_learning_guide/actions/workflows/validate.yml/badge.svg)](https://github.com/didar-ali-deed/machine_learning_guide/actions/workflows/validate.yml)

A permanent, incremental self-study repository that begins with datasets and basic Python and progresses toward classical ML, neural networks, deployment, and nine capstones. This existing workspace is the project root; a second nested copy is unnecessary.

**Start with [START_HERE.md](START_HERE.md).** The [syllabus](SYLLABUS.md) preserves all 427 planned notebooks across 24 modules. The [progress ledger](PROGRESS.md) distinguishes actual lessons, passing executions, and unfinished work. Module specification pages are plans, not completed tutorials.

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

All **21 Python foundation lessons** are authored and tested. Follow the [numbered module index](01_Python_Foundations/README.md) from variables through NumPy, pandas, Matplotlib, Seaborn, and exploratory analysis. The newest lessons cover [indexing and shapes](01_Python_Foundations/14_indexing_slicing_and_shapes.ipynb), [broadcasting](01_Python_Foundations/15_vectorization_and_broadcasting.ipynb), [validated table joins](01_Python_Foundations/17_filtering_grouping_and_merging.ipynb), [Matplotlib](01_Python_Foundations/19_matplotlib.ipynb), [Seaborn](01_Python_Foundations/20_seaborn.ipynb), and [exploratory analysis](01_Python_Foundations/21_exploratory_analysis.ipynb). Mathematics and later modules remain in development; the [latest continuation report](reports/GITHUB_BUILD_REPORT.md) records what was actually delivered.

The mathematics sequence now begins with [fractions and percentages](02_Mathematics_for_ML/01_fractions_percentages_and_exponents.ipynb), [variables and equations](02_Mathematics_for_ML/02_variables_and_equations.ipynb), the existing derivative preview, and [functions and graphs](02_Mathematics_for_ML/04_functions_and_graphs.ipynb). See the [mathematics continuation report](reports/MATHEMATICS_ON_RAMP_REPORT.md) for the latest batch and next actions.

Continue through [linear and quadratic equations](02_Mathematics_for_ML/05_linear_and_quadratic_equations.ipynb), [logarithms and exponentials](02_Mathematics_for_ML/06_logarithms_and_exponentials.ipynb), and [vector arithmetic](02_Mathematics_for_ML/08_vector_addition_and_multiplication.ipynb). The [algebra/logarithm/vector report](reports/ALGEBRA_LOGS_VECTORS_REPORT.md) records that batch's evidence and limitations.

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
