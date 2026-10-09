# Interview practice — foundation and classical core edition

Explain assumptions before formulas. A strong answer connects a mechanism to a concrete example and acknowledges where it fails. Advanced specialized questions will expand alongside their notebooks; this file is not a claim that those modules are complete.

## Beginner

1. **What is ML?** A procedure estimates a rule's settings from examples. Averaging previous sales to predict the next day is already a learned model, though a simple one.
2. **Feature versus target?** A feature is available at prediction time; the target is the outcome being predicted. A column's role depends on the actual timing and question.
3. **Training versus inference?** Training estimates settings; inference applies the stored settings to inputs. A preprocessing mean is also a fitted setting.
4. **Classification versus regression?** Categories versus numerical outcomes. Integer category codes do not turn classification into meaningful numerical regression.
5. **Why split data?** To inspect whether learned behavior transfers to examples not used for fitting. Use validation for choices and an untouched test for final assessment.
6. **What is overfitting?** A rule captures training-specific details that fail to generalize. A gap between low training error and worse validation error is evidence, not the sole definition.
7. **Why a baseline?** It shows whether complexity improves a meaningful reference. A majority classifier can expose misleading accuracy on imbalanced data.
8. **What does a gradient do?** It gives local sensitivity of an objective to parameters. Moving against it can reduce a smooth objective with an appropriate step size.
9. **Why normalize features?** Some penalties and distance methods depend on numerical scale. Scaling is a choice tied to the algorithm, not a universal requirement for every model.
10. **Why restart a notebook kernel?** To detect hidden state and missing execution dependencies. Saved outputs alone do not prove the current code runs.

## Intermediate

11. **What is leakage?** Information unavailable for the intended prediction, or reserved for assessment, influences fitting or selection. Fitting an imputer before cross-validation is a common example.
12. **Ridge versus Lasso?** L2 penalty shrinks coefficients continuously; L1 can set some to zero. Scaling and correlated features affect interpretation and selection stability.
13. **Precision versus recall?** Precision asks how many flagged positives are real; recall asks how many real positives were found. Choose tradeoffs using operational costs and validation evidence.
14. **Why can ROC-AUC look favorable with rare positives?** It summarizes ranking across thresholds, while small false-positive rates can still yield many false alerts when negatives dominate. Inspect precision-recall and workload too.
15. **How should preprocessing enter CV?** Inside each training fold through a pipeline, so held-out folds do not influence fitted transformations.
16. **Bagging versus boosting?** Bagging averages resampled learners to reduce variance; boosting builds sequential corrections to an objective. Actual bias/variance behavior depends on learner and settings.
17. **Why do trees not require standardization in the same way KNN does?** Axis-aligned splits depend mainly on ordering within each feature, whereas KNN compares distances combining feature scales.
18. **What does PCA optimize?** A low-rank linear representation preserving maximal variance or minimizing squared reconstruction error under corresponding formulations. High variance need not predict the target.
19. **Why tune on validation rather than test?** Repeated selection adapts to the sample. A test used repeatedly becomes part of development, weakening its independent-assessment role.
20. **When use grouped splits?** When records share entities such as people or devices and deployment requires generalization to unseen entities. Random row splits may leak entity-specific patterns.

## Advanced reasoning

21. **What does nested CV estimate?** Performance of a selection procedure when tuning occurs within inner folds and evaluation occurs on outer folds. It does not eliminate all data-dependence or deployment mismatch.
22. **Calibration versus discrimination?** Ranking positives above negatives differs from assigning probabilities that match observed frequencies. A model can rank well while being poorly calibrated.
23. **Why can feature importance mislead with correlated inputs?** Several features can substitute for one another; importance depends on the fitted model, perturbation method, and evaluation distribution. It is not automatically causal relevance.
24. **What is distribution shift?** Training and deployment conditions differ. Distinguish changes in inputs, target prevalence, and input-target relationships because interventions differ.
25. **Why are confidence intervals for a single test score insufficient after extensive model selection?** Selection introduces additional dependence and optimism. The reported protocol must account for the whole process, not only the last model's fixed predictions.
26. **Why can a stationary point fail to be a minimum?** Its gradient is zero but local curvature may indicate a maximum or saddle. The first derivative alone is insufficient.
27. **Why is offline recommender evaluation difficult?** Observed clicks depend on what the previous policy exposed. Missing interactions are not simple random negatives.
28. **What makes a model artifact a security concern?** Some serialization formats can execute code when loaded. Load only trusted artifacts with provenance and appropriate access controls; a filename is not a trust boundary.
29. **How evaluate a deployed model responsibly?** Monitor input validity, performance where labels arrive, calibration, subgroup behavior, operational costs, and changes over time. Define response procedures before alerts occur.
30. **What would make you choose a simpler model?** Comparable validated performance with clearer failure modes, lower latency, easier maintenance, or better uncertainty handling. Simplicity is a tradeoff grounded in requirements, not a universal winner.

Practice by giving a 30-second explanation, a small example, and one limitation for each answer. Then implement the example using a completed lesson instead of relying on memorized phrasing.
