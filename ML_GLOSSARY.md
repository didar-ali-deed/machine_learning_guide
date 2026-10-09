# Machine Learning glossary — foundation and core edition

Terms are explained here in ordinary language. Advanced module-specific terms will expand this reference as those lessons are authored.

| Term | Meaning and concrete example |
|---|---|
| Artificial intelligence | A broad area concerned with systems performing tasks associated with intelligence; learning from examples is one approach |
| Machine learning | Estimating a rule's settings from examples, such as learning typical demand from past sales |
| Deep learning | Learning with neural networks containing multiple processing layers; it is a subset of ML |
| Dataset | A collection of recorded examples, such as daily bakery records |
| Observation | One recorded unit, such as one day or one customer visit; define which before analysis |
| Feature | An input available when a prediction is made, such as tomorrow's calendar date |
| Target/label | The outcome to predict, such as tomorrow's eventual sales |
| Model | A rule mapping inputs to predictions, such as a weighted sum of measurements |
| Parameter | A value learned from training data, such as a regression coefficient |
| Hyperparameter | A setting chosen outside parameter fitting, such as tree depth or learning rate |
| Training/fitting | Estimating model or preprocessing settings from designated examples |
| Inference | Applying fitted settings to new inputs |
| Regression | Predicting a numerical outcome, such as time or price |
| Classification | Predicting a category, such as spam versus legitimate mail |
| Clustering | Grouping examples by a chosen notion of similarity without supplied group labels |
| Supervised learning | Learning from examples paired with desired outputs |
| Unsupervised learning | Learning structure without a supplied prediction target |
| Semi-supervised learning | Combining some labeled examples with additional unlabeled ones |
| Self-supervised learning | Constructing training targets from the data itself, such as a hidden word |
| Reinforcement learning | Learning action choices from consequences and rewards over interaction |
| Baseline | A simple reference method, such as always predicting the training mean |
| Loss | A numerical measure of error used for an example or training objective |
| Objective | The quantity optimized, possibly combining data loss and a penalty |
| Metric | A reported performance measure; it may differ from the optimized loss |
| Accuracy | Fraction of classifications that match the supplied labels |
| Precision | Fraction of predicted positives that are actually positive |
| Recall/sensitivity | Fraction of actual positives detected by the model |
| Specificity | Fraction of actual negatives correctly identified |
| F1 | Harmonic mean of precision and recall under a stated positive class |
| Threshold | A cutoff turning a score or probability into a decision |
| Calibration | Agreement between stated probabilities and observed frequencies across comparable predictions |
| Generalization | Performance on relevant examples beyond those used for fitting |
| Overfitting | Learning training-specific detail that fails to transfer well to new examples |
| Underfitting | A model or fitting process is too limited to capture useful structure |
| Bias–variance tradeoff | Tension between systematic approximation limits and sensitivity to the particular training sample |
| Regularization | A constraint or penalty discouraging unstable or unnecessarily complex solutions |
| Validation set | Data used to guide model choices before final evaluation |
| Test set | Data reserved for assessment after those choices are fixed |
| Cross-validation | Repeated training/evaluation splits within the development data |
| Leakage | Information unavailable at prediction or reserved for assessment influences fitting or selection |
| Pipeline | A sequence that applies preprocessing and prediction consistently, fitting transforms in the proper training scope |
| Scaling | Changing numerical representation, often to comparable feature magnitudes |
| Standardization | Subtracting a fitted mean and dividing by a fitted standard deviation |
| Missingness | Absence of an observation; it need not mean a numerical zero |
| Imputation | Filling missing values using an explicit rule fitted in the training scope |
| Encoding | Representing categories or text numerically while preserving an intended meaning |
| Scalar | One number, such as an intercept |
| Vector | An ordered collection of numbers, such as one example's features |
| Matrix | A rectangular arrangement, such as examples by features |
| Tensor | A multidimensional numerical object; image batches commonly use four axes |
| Shape | The lengths of array axes, such as `(100, 3)` for 100 examples with three features |
| Dot product | Sum of corresponding products, such as quantities times prices |
| Derivative | Local output change per input change |
| Gradient | Collection of partial derivatives with respect to multiple inputs or parameters |
| Gradient descent | Repeated parameter updates opposite the gradient to reduce an objective |
| Learning rate | A multiplier controlling the size of an optimization update |
| Epoch | One traversal of the training data in an iterative learning procedure |
| Batch | A group of examples used together for an update or computation |
| Likelihood | How a chosen model assigns probability or density to observed data, viewed as a function of its parameters |
| Prior | A probability distribution over unknown quantities before the current observations are incorporated |
| Posterior | The updated distribution after combining the prior and likelihood |
| Uncertainty | Incomplete knowledge about outcomes, parameters, or evaluation; its source and representation must be stated |
| Distribution shift | A change between the data-generating conditions represented in training and those encountered later |
| Data drift | A change in observed input distributions over time |
| Concept drift | A change in the relationship between inputs and the target |
| Explainability | Methods for describing model behavior; an explanation need not establish causation |
| Fairness metric | A chosen comparison of outcomes or errors across groups; different criteria can conflict |
| Robustness | Stability under specified perturbations or changed conditions, not universal reliability |
| Reproducibility | Ability to rerun a documented process with controlled inputs, versions, and randomness |
| Kernel | In Jupyter, the process executing cells; in SVMs, a similarity function. Context matters |
| Virtual environment | A project-specific Python package installation isolated from other projects |

For calculations rather than definitions, use the [mathematics reference](MATHEMATICS_CHEATSHEET.md). For implemented examples, follow the [syllabus](SYLLABUS.md).
