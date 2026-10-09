# Datasets and provenance

Current lessons use tiny, explicitly invented values or seeded NumPy generators embedded in their notebooks. No external dataset is required. Bakery sales, emails, weather rows, transactions, and waiting times are teaching examples, not observations of real people or businesses. They support arithmetic demonstrations, not empirical claims about populations.

Future stored datasets must include a source/license note, column definitions, units, row meaning, generation seed if synthetic, missing-data rules, and prediction-time availability. Keep sensitive data and large binaries out of this repository. Built-in scikit-learn datasets are preferable to downloads when suitable.

For capstones, separate training, validation, and test data before fitting transformations. Use entity or chronological splits where observations are dependent. Record the split protocol and avoid repeatedly examining the test set while choosing models. Never alter raw source data to obtain a preferred result.
