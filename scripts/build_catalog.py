"""Maintain the complete curriculum inventory without creating placeholder notebooks."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Each semicolon-separated entry is a dedicated planned notebook.
MODULES = [
('00_Getting_Started', 'Describe a learning problem, identify its data, and run a notebook safely.', '''What is Machine Learning?;Machine Learning types and terminology;Python and Jupyter introduction;What is Artificial Intelligence?;Machine Learning versus Deep Learning;Supervised learning;Unsupervised learning;Semi-supervised and self-supervised learning;Reinforcement learning introduction;Datasets features labels and predictions;Installing Python and Jupyter;Virtual environments and package management;How to use notebooks;Introduction to Git and GitHub;A first complete Machine Learning example'''),
('01_Python_Foundations', 'Write small Python programs and inspect, transform, and visualize tabular arrays.', '''Variables and data types;Operators;Strings;Lists tuples sets and dictionaries;Conditions and loops;Functions and parameters;Scope;List comprehensions;Modules and packages;File handling;Exceptions and debugging;Classes and object-oriented programming;NumPy basics;Indexing slicing and shapes;Vectorization and broadcasting;Pandas basics;Filtering grouping and merging;Visualizing data;Matplotlib;Seaborn;Exploratory analysis'''),
('02_Mathematics_for_ML', 'Calculate and interpret the algebra, derivatives, probabilities, and objectives used in learning.', '''Fractions percentages and exponents;Variables and equations;Functions and derivatives;Functions and graphs;Linear and quadratic equations;Logarithms and exponentials;Scalars vectors and matrices;Vector addition and multiplication;Dot products;Matrix multiplication;Matrix transpose;Matrix inverse and pseudoinverse;Rank;Norms and distances;Eigenvalues and eigenvectors;Singular Value Decomposition;Limits and continuity;Derivatives;Partial derivatives;Chain rule;Gradients;Gradient descent;Multivariable differentiation;Backpropagation mathematics;Probability rules;Conditional probability;Bayes theorem;Random variables;Bernoulli distribution;Binomial distribution;Normal distribution;Poisson distribution;Mean median and mode;Variance and standard deviation;Covariance and correlation;Sampling;Central Limit Theorem;Confidence intervals;Hypothesis testing;Maximum likelihood estimation;Loss functions;Convexity;Regularization;Gradient descent variants;Entropy;Cross-entropy;KL divergence'''),
('03_Data_Analysis_and_Preprocessing', 'Build train-only transformations and detect data-quality failures before modeling.', '''Loading CSV JSON and Excel;Understanding dataset structure;Exploratory Data Analysis;Data quality assessment;Missing values and imputation;Outlier detection and handling;Duplicate records;Categorical encoding;One-hot versus ordinal encoding;Normalization and standardization;Feature transformations;Feature construction;Feature selection introduction;Class imbalance;Data leakage;Train validation and test splitting;Data preprocessing pipelines;ColumnTransformer;Data validation'''),
('04_Machine_Learning_Foundations', 'Design reproducible experiments that distinguish fit from generalization.', '''What learning means mathematically;Parameters versus hyperparameters;Training versus inference;Supervised prediction;Generalization;Empirical risk minimization;Bias versus variance;Overfitting and underfitting;Training and validation curves;Loss and objective functions;Regularization intuition;Baseline models;Evaluation metrics;Experimental design;Reproducibility;Common modeling mistakes'''),
('05_Regression_Algorithms', 'Derive regression predictions and losses, compare estimators, and diagnose residuals.', '''Simple Linear Regression from scratch;Multiple Linear Regression;Ordinary Least Squares;Normal Equation;Batch Gradient Descent;Stochastic Gradient Descent;Mini-Batch Gradient Descent;Polynomial Regression;Ridge Regression;Lasso Regression;Elastic Net Regression;Bayesian Ridge Regression;Huber Regression;RANSAC Regression;Quantile Regression;Poisson Regression;K-Nearest Neighbors Regression;Support Vector Regression;Decision Tree Regression;Random Forest Regression;Gradient Boosting Regression;Regression metrics;Residual analysis;Multicollinearity;Statistical assumptions'''),
('06_Classification_Algorithms', 'Connect class probabilities to decisions and evaluate the costs of classification errors.', '''Binary Logistic Regression;Multiclass Logistic Regression;Softmax Regression;Perceptron;SGD Classifier;K-Nearest Neighbors Classifier;Gaussian Naive Bayes;Multinomial Naive Bayes;Bernoulli Naive Bayes;Linear Discriminant Analysis;Quadratic Discriminant Analysis;Linear Support Vector Machine;Kernel Support Vector Machine;Decision Tree Classification;Random Forest Classification;Sigmoid function;Decision boundaries;Probabilities versus labels;Confusion matrix;Accuracy precision recall and F1;Sensitivity and specificity;ROC and AUC;Precision-recall curves;Classification thresholds;Probability calibration;Multiclass and multilabel evaluation'''),
('07_Decision_Trees_and_Ensembles', 'Explain splitting, randomization, and sequential error correction with controlled experiments.', '''Decision Tree Classifier;Decision Tree Regressor;Entropy and Gini impurity;Information gain;Tree pruning;Bagging;Random Forests;Extra Trees;AdaBoost;Gradient Boosting;Histogram Gradient Boosting;XGBoost;LightGBM;CatBoost;Voting ensembles;Stacking;Blending;Bagging versus boosting'''),
('08_Model_Evaluation_and_Optimization', 'Choose defensible validation designs and tune models without leaking test information.', '''Holdout validation;K-Fold Cross-Validation;Stratified K-Fold;Grouped validation;Time-series validation;Cross-validation leakage;GridSearchCV;RandomizedSearchCV;Bayesian hyperparameter optimization;Nested cross-validation;Learning curves;Validation curves;Feature selection;Recursive Feature Elimination;Threshold optimization;Imbalanced-learning strategies;Error analysis;Model comparison;Statistical uncertainty of evaluation results'''),
('09_Clustering', 'Choose and evaluate cluster geometry while distinguishing structure from arbitrary labels.', '''K-Means;K-Means++ initialization;Mini-Batch K-Means;Hierarchical Clustering;Agglomerative Clustering;DBSCAN;OPTICS;HDBSCAN;Gaussian Mixture Models;Expectation-Maximization;Spectral Clustering;Mean Shift;Affinity Propagation;Cluster evaluation and silhouette scores;Cluster visualization and algorithm selection'''),
('10_Dimensionality_Reduction', 'Explain projection, reconstruction, and neighborhood preservation with explicit information tradeoffs.', '''Principal Component Analysis;PCA from scratch;Singular Value Decomposition;Kernel PCA;Independent Component Analysis;Factor Analysis;Non-negative Matrix Factorization;t-SNE;UMAP;Random Projection;Feature selection versus feature extraction;Autoencoder-based representation learning'''),
('11_Anomaly_Detection', 'Score unusual observations and evaluate rare-event alerts using labeled audit examples.', '''Statistical anomaly detection;Z-score and robust statistics;Isolation Forest;Local Outlier Factor;One-Class SVM;Robust covariance approaches;Autoencoder anomaly detection;Anomaly detection evaluation;Suspicious transactions;Sensor anomalies'''),
('12_Time_Series', 'Forecast future values using chronological validation and information available at forecast time.', '''Time-series basics;Trend seasonality and stationarity;Moving averages;Exponential smoothing;Autoregression AR;Moving Average MA;ARMA;ARIMA;SARIMA;Feature-based forecasting;Lag features and rolling windows;Time-series cross-validation;Forecasting with Random Forests;Forecasting with Gradient Boosting;LSTM forecasting;Forecasting metrics;Data leakage in time series;Advanced forecasting libraries'''),
('13_Probabilistic_Machine_Learning', 'Distinguish likelihood, prior, posterior, approximation, and predictive uncertainty.', '''Bayesian inference;Prior likelihood and posterior;Maximum Likelihood Estimation;Maximum a Posteriori Estimation;Bayesian Linear Regression;Gaussian Mixture Models;Hidden Markov Models;Gaussian Processes;Variational inference intuition;Monte Carlo sampling;Uncertainty estimation;Probabilistic predictions'''),
('14_Neural_Network_Foundations', 'Derive backpropagation and train small networks with NumPy before PyTorch.', '''Biological versus artificial neurons;Perceptron mathematics;Activation functions;Feedforward neural networks;Loss functions;Computational graphs;Chain rule revision;Backpropagation by hand;Neural networks from scratch with NumPy;Multilayer Perceptron;Weight initialization;Vanishing and exploding gradients;Stochastic optimization;SGD optimizer;Momentum;RMSprop;Adam;Dropout and regularization;Batch normalization;Training and validation loops;PyTorch tensors and automatic differentiation;Building a PyTorch training pipeline'''),
('15_Deep_Learning', 'Trace tensor shapes through convolution, recurrence, and attention in CPU-sized experiments.', '''Convolutional Neural Networks;Convolution and pooling operations;CNN image classification;Transfer learning;Fine-tuning pretrained models;Recurrent Neural Networks;Long Short-Term Memory;Gated Recurrent Units;Sequence modeling;Attention mechanisms;Self-attention from scratch;Transformer architecture;Positional encoding;Multi-head attention;Encoder and decoder concepts;Optimization and regularization;Representation learning;Self-supervised learning foundations'''),
('16_Natural_Language_Processing', 'Transform text into representations and evaluate classification, retrieval, and generation systems.', '''Text cleaning;Tokenization;Stopwords and stemming;Lemmatization;Bag of Words;TF-IDF;Text classification;Sentiment analysis;Topic modeling;Latent Dirichlet Allocation;Word embeddings;Word2Vec;Transformer-based NLP;BERT concepts and fine-tuning;Sentence embeddings;Semantic similarity;Information retrieval;Retrieval-Augmented Generation fundamentals;Evaluating NLP systems'''),
('17_Computer_Vision', 'Interpret pixel tensors and evaluate recognition, localization, segmentation, and OCR.', '''Images as numerical arrays;Image preprocessing;Filters and convolution;Edge detection;Feature extraction;Traditional image classifiers;CNN-based image classification;Transfer learning;Image augmentation;Object detection fundamentals;Image segmentation fundamentals;OCR fundamentals;Computer vision metrics'''),
('18_Recommendation_Systems', 'Build and evaluate recommenders with honest temporal splits and cold-start analysis.', '''Popularity-based recommendations;Content-based filtering;Collaborative filtering;User-based KNN recommendations;Item-based KNN recommendations;Matrix Factorization;Alternating Least Squares;Implicit feedback;Ranking metrics;Cold-start problems;Hybrid recommenders'''),
('19_Reinforcement_Learning', 'Compute returns and value updates in small reproducible environments.', '''Agents and environments;States and actions;Rewards;Markov Decision Processes;Bellman equations;Multi-armed bandits;Value iteration;Policy iteration;Monte Carlo learning;Temporal Difference learning;Q-Learning;SARSA;Deep Q-Network fundamentals;Exploration versus exploitation;Policy gradient fundamentals'''),
('20_Advanced_ML_Paradigms', 'Select learning protocols when labels, distributions, costs, or objectives change.', '''Semi-supervised learning;Self-supervised learning;Active learning;Online learning;Incremental learning;Transfer learning;Multitask learning;Cost-sensitive learning;Metric learning;Learning to rank;Ensemble diversity;Domain adaptation;Concept drift;Uncertainty-aware learning'''),
('21_Interpretability_Ethics_and_Robustness', 'Audit explanations, subgroup performance, robustness, privacy, and uncertainty.', '''Feature importance;Permutation importance;Partial Dependence Plots;Individual Conditional Expectation;SHAP;LIME;Global versus local explanations;Fairness metrics;Dataset bias;Robustness testing;Model calibration;Data and model privacy;Responsible AI principles;Limitations of interpretability'''),
('22_MLOps_and_Deployment', 'Package, test, serve, monitor, and document a reproducible model safely.', '''End-to-end ML pipelines;Saving and loading models;Model artifact security;FastAPI prediction endpoints;Docker fundamentals;Experiment tracking;MLflow fundamentals;Model versioning;Data validation;Unit testing;Integration testing;CI fundamentals;Model monitoring;Data drift;Concept drift;Retraining strategies;Reproducibility;Production readiness;Model documentation'''),
('23_Real_World_Capstones', 'Deliver a reproducible business report with baseline, tuning, held-out results, interpretation, and limitations.', '''House Price Prediction;Customer Churn Classification;Fraud or Anomaly Detection;Customer Segmentation;Time-Series Demand Forecasting;Sentiment Analysis;Image Classification;Recommendation System;End-to-End FastAPI ML Deployment'''),
]

FIRST = ['00-01', '00-02', '00-03', '01-13', '01-16', '01-18', '02-07', '02-03']
OPTIONAL = {'XGBoost', 'LightGBM', 'CatBoost', 'UMAP', 'Advanced forecasting libraries',
            'SHAP', 'LIME', 'MLflow fundamentals', 'BERT concepts and fine-tuning',
            'Fine-tuning pretrained models'}

def slug(title):
    return re.sub(r'[^a-z0-9]+', '_', title.lower()).strip('_')

def build():
    records = []
    for directory, outcome, topics in MODULES:
        (ROOT / directory).mkdir(exist_ok=True)
        module = directory[:2]
        for number, title in enumerate(topics.split(';'), 1):
            ident = f'{module}-{number:02d}'
            if ident in FIRST:
                index = FIRST.index(ident)
                prereqs = FIRST[max(0, index - 1):index]
            elif number > 1:
                prereqs = [f'{module}-{number - 1:02d}']
            else:
                prereqs = ['02-03'] if int(module) <= 2 else [f'{int(module)-1:02d}-01']
            # Break foundation ordering cycles introduced by the eight-lesson on-ramp.
            if ident == '01-01': prereqs = ['00-03']
            if ident == '02-01': prereqs = ['01-18']
            records.append(dict(id=ident, module=module, title=title,
                path=f'{directory}/{number:02d}_{slug(title)}.ipynb',
                prerequisites=prereqs, hours=6 if module == '23' else (4 if int(module) >= 5 else 2),
                outcome=outcome, optional=title in OPTIONAL,
                kind='algorithm' if module in {'05','06','07','09','10','11','13','14','15','18','19'} else 'lesson'))
            if ident == '01-09':
                records[-1]['dependencies'] = ['src/academy/measurements.py']
    for directory in ['datasets','src/academy','exercises','solutions','assessments','diagrams',
                      'reference_materials','tests','reports','lesson_sources']:
        (ROOT / directory).mkdir(parents=True, exist_ok=True)
    destination = ROOT / 'reference_materials' / 'notebook_inventory.json'
    destination.write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
    render(records)
    print(f'Inventory: {len(records)} notebooks across {len(MODULES)} modules; no placeholder notebooks created.')

def render(records):
    rows = ['# Complete Machine Learning Academy syllabus', '',
        'The full scope is planned here. A notebook link appears only after the file exists. Planned links open its module specification; the intended filename remains visible there. Status is maintained in [PROGRESS.md](PROGRESS.md).', '',
        'Hours include reading, manual calculations, experiments, and exercises. They are estimates, not deadlines. A beginner may need more time. The eight-lesson on-ramp precedes the full numbered sequence.', '']
    for directory, outcome, _ in MODULES:
        module_records = [r for r in records if r['module'] == directory[:2]]
        rows += [f'## {directory.replace("_", " ")}', '', outcome, '',
                 '| ID | Notebook or planned specification | Hours | Prerequisites | Outcome focus |',
                 '|---|---|---:|---|---|']
        module_doc = [f'# {directory.replace("_", " ")}', '', outcome, '',
                      '[Syllabus](../SYLLABUS.md) · [Progress](../PROGRESS.md)', '']
        for r in module_records:
            exists = (ROOT / r['path']).is_file()
            target = r['path'] if exists else f'{directory}/README.md#{r["id"]}'
            label = r['title'] + ('' if exists else ' — planned')
            pre = ', '.join(f'[{p}](#{p})' for p in r['prerequisites']) or 'None'
            # Prerequisite links point to stable syllabus IDs, even for planned lessons.
            rows += [f'| <a id="{r["id"]}"></a>{r["id"]} | [{label}]({target}) | {r["hours"]} | {pre} | {r["title"]} |']
            module_doc += [f'<a id="{r["id"]}"></a>', f'## {r["id"]}: {r["title"]}', '',
                f'Intended notebook: `{Path(r["path"]).name}`. Study estimate: {r["hours"]} hours.', '',
                ('[Open notebook](' + Path(r['path']).name + ')' if exists else 'Status: planned; no lesson file exists yet.'), '',
                f'Prerequisites: {", ".join(r["prerequisites"]) or "none"}.',
                'Optional dependency or larger extension.' if r['optional'] else 'Target: small CPU example with local or generated data.', '']
        (ROOT / directory / 'README.md').write_text('\n'.join(module_doc), encoding='utf-8')
        rows.append('')
    rows += [f'Total planned notebooks: **{len(records)}**. Estimated total study time: **{sum(r["hours"] for r in records)} hours**.', '']
    (ROOT / 'SYLLABUS.md').write_text('\n'.join(rows), encoding='utf-8')

if __name__ == '__main__':
    build()
