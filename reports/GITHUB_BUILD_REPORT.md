# GitHub build and Python foundations completion

This is the snapshot at Python-module completion. For the subsequent mathematics batch, see [MATHEMATICS_ON_RAMP_REPORT.md](MATHEMATICS_ON_RAMP_REPORT.md) and the current [progress ledger](../PROGRESS.md).

This continuation authored and verified **six new notebooks**, completing all **21 Python foundation lessons**. The academy now has **26 created and reviewed lessons** out of **427 planned**; **401 remain unwritten**. Modules 00 and 02 are still in progress at 3/15 and 2/47; modules 03–23 remain planned. Completing Python is not completion of the entire academy.

## New learning files

| ID | Clean notebook | Editable source |
|---|---|---|
| 01-14 | [Indexing, slicing, and shapes](../01_Python_Foundations/14_indexing_slicing_and_shapes.ipynb) | [01-14.lesson](../lesson_sources/01-14.lesson) |
| 01-15 | [Vectorization and broadcasting](../01_Python_Foundations/15_vectorization_and_broadcasting.ipynb) | [01-15.lesson](../lesson_sources/01-15.lesson) |
| 01-17 | [Filtering, grouping, and merging](../01_Python_Foundations/17_filtering_grouping_and_merging.ipynb) | [01-17.lesson](../lesson_sources/01-17.lesson) |
| 01-19 | [Matplotlib](../01_Python_Foundations/19_matplotlib.ipynb) | [01-19.lesson](../lesson_sources/01-19.lesson) |
| 01-20 | [Seaborn](../01_Python_Foundations/20_seaborn.ipynb) | [01-20.lesson](../lesson_sources/01-20.lesson) |
| 01-21 | [Exploratory analysis](../01_Python_Foundations/21_exploratory_analysis.ipynb) | [01-21.lesson](../lesson_sources/01-21.lesson) |

Each lesson contains 21 substantive sections, a hand calculation, executable examples, plots, six exercises with worked solutions, and five answered questions in each knowledge/interview section. Their saved executed copies are under `reports/executed/01_Python_Foundations/`. The [array/table](python_array_tables_review.png) and [plotting/EDA](python_plotting_eda_review.png) contact sheets preserve inspected figures. No planned notebook was generated as an empty placeholder.

## GitHub and learning support

The repository was initialized on `main` and published to [didar-ali-deed/machine_learning_guide](https://github.com/didar-ali-deed/machine_learning_guide) using the user's explicit remote and push instruction. Separate commits preserve the initial 20 verified lessons, GitHub preparation, the array/table batch, and a Windows runner fix; subsequent curriculum/status work is committed separately. No remote history was overwritten.

Added `.github/workflows/validate.yml`, a PR template, `.gitattributes`, [contribution instructions](../CONTRIBUTING.md), [GitHub setup](../GITHUB_SETUP.md), and [an active-study guide](../STUDENT_GUIDE.md). Virtual environments, caches, environment artifacts, and personal notes are ignored. Added [render_review.py](../scripts/render_review.py), a headless renderer for actual saved notebook plots. A public redistribution license has not been selected.

## Verification and limitations

All six new notebooks passed isolated `.venv` execution; 01-14 was repeated after plot-margin review and 01-17 after navigation changes. Their current evidence adds **47 code cells and nine figures**, including display-setup cells. The whole authored collection covers **190 code cells and 32 figures**. Counts come from execution results, not the planned inventory.

All **17 tests** pass locally: 12 infrastructure tests and five shared-helper tests. Structural, source-consistency, prerequisite, syntax, and local-link checks pass for the authored sources and their saved executed copies. Package consistency passes. Existing dependency pins were sufficient; no optional software was installed. Manual review is recorded in [CONTENT_REVIEW.md](CONTENT_REVIEW.md) and hash records.

The [first GitHub run](https://github.com/didar-ali-deed/machine_learning_guide/actions/runs/37877214137) installed dependencies and passed structural checks, then failed a relative-link test because a Windows short-name TEMP alias was resolved on only one side. Both path parents are now resolved consistently and a regression test simulates the alias. Inspect the [workflow page](https://github.com/didar-ali-deed/machine_learning_guide/actions/workflows/validate.yml) for current remote run results; a successful push alone is not a CI pass.

The complete 427-lesson academy, classical algorithms, advanced reference material, and capstone projects remain unfinished. Continue incrementally with actual lessons and execution evidence. The [progress ledger](../PROGRESS.md) lists every outstanding notebook.

## Exact continuation prompt

> Continue the academy in E:\machine_learning_basic_to_advance. Read AGENTS.md, PROGRESS.md, and reports/GITHUB_BUILD_REPORT.md. Implement 02-01 Fractions percentages and exponents, 02-02 Variables and equations, and 02-04 Functions and graphs as substantial beginner lessons with manual calculations, code, plots, exercises, and complete solutions. Regenerate notebooks, execute them in fresh .venv kernels, inspect all outputs and figures, run structural/link checks and tests, update source-matched review hashes and progress, then commit and push each reviewed batch to origin/main without force. Check actual GitHub CI results and fix failures. Preserve all 427 inventory entries and clearly distinguish planned advanced work from delivered lessons. Continue further batches while resources permit.
