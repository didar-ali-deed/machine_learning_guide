# Content review

The first eight lessons were reviewed against their prose, manual calculations, executable assertions, printed results, and all 11 rendered figures. This was a review by the authoring assistant, not an independent external academic review. Structural word counts alone were not treated as evidence of teaching quality.

| ID | Reviewed evidence and boundary |
|---|---|
| 00-01 | Mean 4, individual absolute errors 1 and 3, MAE 2; mean-versus-median distinction and train/test timing stated |
| 00-02 | Confusion matrix `[[2,0],[1,1]]`, accuracy 0.75, rare-class accuracy 0.99 with recall zero; supervised metrics distinguished from training |
| 00-03 | Revenue 12, remainder 7, new call 15 without changing stored 12; expected conversion/validation failures caught deliberately |
| 01-13 | Column means `[3,4]`, centered columns zero, copy independence, safe zero-row division; shape and mixed-unit caveats checked |
| 01-16 | Product revenue 50 and 100, total 150, many-to-one merge checks, one missing quantity and one duplicate diagnosed |
| 01-18 | Bin counts `[3,2,1]`; explicit boundary convention, seeded synthetic association, and coarse/fine histogram interpretation |
| 02-07 | Weighted sums `[11,13]`, fee totals `[13,15]`, unit conversion invariance, and weight sensitivity `[1,0.5]` |
| 02-03 | Difference quotient approaches six before floating-point cancellation; first update 0.6, loss 5.76, and rate 1.1 divergence match prose |

The first execution attempt exposed missing embedded plot output under the runner's backend. Explicit inline-display initialization corrected it; all eight were actually re-executed afterward. The original unsuccessful attempt was not counted as a passing batch.

Current source hashes associated with reviewed lessons are in [content_review.json](content_review.json). Fresh-kernel results are in [execution_results.json](execution_results.json). [The contact sheet](review_contact_sheet.png) shows the first batch's plots. A subsequent source change requires renewed review and execution.

Remaining limitations: the full course is unfinished; larger datasets, statistical inference, and production-equivalent implementations are not claimed by these introductory examples. Synthetic outputs establish arithmetic and mechanism behavior, not real-world predictive performance.

## Second batch and reviewed corrections

The next three lessons and their rendered figures were inspected before continuation. Their passing executions bring the available curriculum to 11 lessons and 14 rendered figures. The second batch's figures are in [second_batch_review.png](second_batch_review.png).

| ID | Reviewed evidence and boundary |
|---|---|
| 01-01 | Identifier `007` preserved; Celsius 20 maps to Fahrenheit 68; binary floating-point versus Decimal compared; shared-list and copy behavior demonstrated; ambiguous flags rejected |
| 01-02 | Residuals `[-1,2]` give MSE 2.5 rather than squared mean residual 0.25; precedence, negative powers, bounded array masks, and empty/exact/partial batch counts checked |
| 01-03 | Token counts red 2 and blue 1; original strings preserved; quoted CSV delimiter parsed; normalized region counts north 3 and south 2; unknown category rejected |
| 00-01 | Interview prompt now has explicit question form; mathematics and passing execution unchanged in meaning |
| 00-02 | Confusion-matrix annotation contrast improved and the changed lesson actually re-executed |

Review records were reconciled with the latest passing source hashes when resuming. The previous PROGRESS.md snapshot predated the second batch's final executions; regenerating status removes that stale snapshot without claiming new executions.

## Containers, control flow and functions

These three lessons passed fresh-kernel execution. The printed intermediate values, exercise solutions, and [rendered figures](python_control_flow_review.png) were inspected before marking them reviewed.

| ID | Reviewed evidence and boundary |
|---|---|
| 01-04 | Three observations versus two distinct products; sale-line counts A 2/B 1 versus item totals A 5/B 1; nested-copy independence; unknown product quarantined and accepted totals reconciled |
| 01-05 | Missing and negative readings excluded separately; valid zero retained; total 30/count 3/mean 10; batches `[4,4,2]` terminate with exact coverage; stronger validator rejects types and nonfinite values |
| 01-06 | Errors `[1,2]` yield MAE 1.5 and weighted MAE 1.75; library agreement, input preservation, shift/scale invariants, invalid inputs, and independent default histories checked |

The loops and metric functions are deliberately bounded teaching implementations with stated input-domain limits, rather than claims of production equivalence.

## Scope, comprehensions and modules

These lessons were executed in separate fresh kernels, and the intermediate outputs, mathematical examples, exercises, and figures were inspected. [The review contact sheet](python_scope_and_modules_review.png) records their figures. The scope figure's long category labels were wrapped after visual inspection and that changed notebook was re-executed before its final review record was saved.

| ID | Reviewed evidence and boundary |
|---|---|
| 01-07 | Hidden global reference changes result 98 to 0; explicit reference remains 98; closure behavior and expected UnboundLocalError checked; configured training mean remains 3 after source-list mutation |
| 01-08 | Mapping length 4, filtering length 2, and conditional replacement length 4; correct selected IDs `[101,103]` retain targets A/C; rejected IDs `[102,104]` reconcile without overlap |
| 01-09 | Local source location verified; imported mean 4 agrees with manual and standard-library results; module cache identity, one-pass iterable, malformed inputs, and input preservation checked |

Earlier Strings and Functions notebooks were re-executed after replacing their next-lesson specification links with actual newly created notebook links. The local `measurements.py` dependency is now declared in the inventory and included in the modules lesson's evidence hash. Tests verify that editing a declared helper invalidates old evidence and that dependency paths cannot leave the repository.

## File handling, debugging, and classes

These three lessons passed execution in separate fresh kernels. Source explanations, hand calculations, exercise solutions, printed outputs, and [all three rendered figures](python_files_debugging_classes_review.png) were inspected. The debugging figure derives its counts from the audit result; that final edit was re-executed before recording review hashes.

| ID | Reviewed evidence and boundary |
|---|---|
| 01-10 | Loaded `[2,4,6]` mean 4 minutes; CSV quoted comma preserved; JSON metadata and UTF-8 café round trip; duplicate/missing fields diagnosed; exclusive creation preserves existing files; temporary files cleaned |
| 01-11 | Incorrect denominator produces 3 rather than 4; accepted IDs 101/104 have mean 3 minutes; four rejected rows retain reasons; conversion cause preserved; empty/all-invalid batches and row identity checked |
| 01-12 | Training mean 2 centers `[1,3]` to `[-1,1]`, held-out 100 to 98; independent instance mean 20; failed refit preserves state; scikit-learn agreement and distance invariants; challenge range scaler extrapolates to 2 and rejects constant data |

The previous modules lesson was re-executed after updating its next-step link to the new file-handling notebook. No dependency changed. The scratch classes intentionally support ordinary Python numeric values and one feature, without claiming production estimator compatibility. Synthetic examples support teaching checks, not population conclusions. A separate contact-sheet rendering attempt hit a Tk backend configuration error; using the noninteractive Agg backend resolved that review-tool issue without installing software. Notebook execution was unaffected.

## Array selection, broadcasting, and relational tables

Fresh-kernel execution passed for 01-14, 01-15, and 01-17. Manual calculations, code, printed outputs, exercise solutions, and [the three rendered figures](python_array_tables_review.png) were inspected. The indexing plot was given extra margins to keep identifiers clear of its border and re-executed after that adjustment.

| ID | Evidence and teaching boundary |
|---|---|
| 01-14 | IDs 102/103 retain targets 7/9; selected mean 8 hours; vector/column and row/table shapes differ; basic slice edits reach their source while advanced-index copies do not; paired versus rectangular indexing and empty selections checked |
| 01-15 | Column means 20/140 agree with loops; held-out row centers to 20/80; accidental 3x3 loss contrasts with zero corresponding error; finite/shape guards and checked-MSE exercise verified |
| 01-17 | Paid IDs 101/102/104 total 80 dollars; group counts 2/1 and means 20/40; weighted mean 80/3; duplicate reference keys rejected; unmatched order 104 retained; source table preserved |

These lessons teach transformations and table integrity, not predictive performance. The functions have deliberately restricted contracts, and neither shape agreement nor count conservation alone proves semantic correctness.

## Matplotlib, Seaborn, and exploratory analysis

Fresh-kernel execution passed for 01-19, 01-20, and 01-21. The source, manual arithmetic, printed outputs, exercise solutions, and [six rendered figures](python_plotting_eda_review.png) were inspected. The table-joins lesson was re-executed after updating its next-step links to these actual notebooks.

| ID | Reviewed evidence and boundary |
|---|---|
| 01-19 | Manual histogram counts `[1,3,1]`, mean 3.2 and median 2; alternate equal-width bins preserve observations; PNG decodes to `(360,600,4)`; labeled plotting helper rejects missing/negative/wrong-shape inputs |
| 01-20 | Site means 4/12 and counts 3/1; visit mean 6 differs from equally weighted site mean 8; plotted bar heights checked; individual instrument paths remain separate; added B visit changes mean to 8; no unsupported interval claims |
| 01-21 | Missing fraction 25% and observed mean 20 versus zero-filled 15; 21 raw rows become 20 unique records; split retains 15 training/5 test rows; 14 complete training pairs support the inspected association; conflicting repeated ID rejected |

The training Pearson correlation of approximately 0.990 follows the synthetic data generator and is not an empirical or causal claim. EDA leaves the test outcomes out of exploratory relationship analysis. All plots identify their quantities and units, and all new source notebooks remain free of execution outputs.
