# Algebra, logarithms, and vector arithmetic

This batch adds three authored, executed, and reviewed mathematics lessons. There are now **32 verified curriculum notebooks** from the **427-notebook inventory**, leaving **395 unwritten**. Python remains complete at 21/21; Getting Started is 3/15 and Mathematics is 8/47. Modules 03–23 and advanced reference expansion remain planned.

| ID | New clean notebook | New editable source |
|---|---|---|
| 02-05 | [Linear and quadratic equations](../02_Mathematics_for_ML/05_linear_and_quadratic_equations.ipynb) | [02-05.lesson](../lesson_sources/02-05.lesson) |
| 02-06 | [Logarithms and exponentials](../02_Mathematics_for_ML/06_logarithms_and_exponentials.ipynb) | [02-06.lesson](../lesson_sources/02-06.lesson) |
| 02-08 | [Vector addition and multiplication](../02_Mathematics_for_ML/08_vector_addition_and_multiplication.ipynb) | [02-08.lesson](../lesson_sources/02-08.lesson) |

The executed copies are saved under `reports/executed/02_Mathematics_for_ML/`. This report and [the contact sheet](algebra_logs_vectors_review.png) are additional new files. Each lesson has 21 meaningful sections, manual calculations, scratch/library implementations, plots, experiments, evaluation, six worked exercises, and answered knowledge/interview questions. No planned placeholders were written.

## Actual checks

All three new lessons passed fresh-kernel `.venv` execution with **24 code cells and three figures**, including display setup. Lesson 02-04 also passed after its navigation changed. Total current execution evidence covers **237 code cells and 38 figures**. Manual review is recorded in [CONTENT_REVIEW.md](CONTENT_REVIEW.md), and review hashes match passing sources.

All **17 infrastructure/helper tests** pass. Structural, syntax, source consistency, prerequisite, and local-link checks pass for both source and saved executed copies. The existing environment was sufficient; no packages or optional software were installed.

## Boundaries and continuation

The quadratic formula implementation is a small teaching solver with numerical limitations, not a production polynomial package. Logarithm domains and numerical stability are taught explicitly. Vector operations retain coordinate order and units and distinguish scalar/elementwise multiplication from the forthcoming dot product. These are supplied mathematical rules rather than learned predictive models.

Git is on `main` with origin [machine_learning_guide](https://github.com/didar-ali-deed/machine_learning_guide). Tested batches are committed and pushed without force. Check the [actual GitHub workflow](https://github.com/didar-ali-deed/machine_learning_guide/actions/workflows/validate.yml) for each published commit; local checks and remote CI are distinct evidence.

> Continue from AGENTS.md and PROGRESS.md. Implement 02-09 Dot products, 02-10 Matrix multiplication, and 02-11 Matrix transpose as substantial beginner lessons. Include manual calculations, explicit shapes and units, scratch/library comparisons, plots, six exercises with solutions, and answered checks. Execute and review each lesson, validate all links and prerequisites, run tests, update hash-based progress, commit and push each reviewed batch to origin/main, and verify actual GitHub CI. Preserve the complete 427-notebook inventory and keep unfinished advanced work planned.
