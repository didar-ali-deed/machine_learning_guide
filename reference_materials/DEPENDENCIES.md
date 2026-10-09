# Dependency strategy

The base environment contains Notebook, ipykernel, nbclient, nbformat, NumPy, pandas, Matplotlib, Seaborn, and scikit-learn. `requirements.in` lists these direct needs. `requirements.txt` pins the actual Windows x64 Python 3.11.9 installation, including its transitive dependencies and packaging tools. A version freeze provides repeatable resolution for that target; it is not a cryptographic artifact lock or a guarantee of compatibility on every platform.

The installed core versions are Notebook 7.6.3, NumPy 2.4.6, pandas 3.0.6, Matplotlib 3.11.2, Seaborn 0.13.2, scikit-learn 1.9.1, ipykernel 7.4.0, and nbclient 0.11.0. The execution report records the environment used by each test run. Do not silently upgrade versions after producing execution evidence.

## Optional stages

| Stage | Packages to consider only when implemented | Default alternative |
|---|---|---|
| Excel and classical time series | openpyxl, statsmodels | CSV, explicit NumPy mechanisms |
| External boosting | xgboost, lightgbm, catboost | scikit-learn histogram gradient boosting |
| Advanced search and embeddings | optuna, umap-learn | randomized search, PCA |
| Neural networks | CPU PyTorch | NumPy mechanism first |
| Pretrained NLP | transformers, sentence-transformers | local bag-of-words/TF-IDF examples |
| Explanations | shap, lime | permutation importance and explicit toy calculations |
| Serving and tracking | fastapi, uvicorn, httpx, mlflow | local Python prediction function and JSON experiment records |

`requirements-optional.txt` is a commented planning reference, not an installed or validated optional lock. Pin and test a separate extension environment when those notebooks are authored. GPU tooling, Docker installation, pretrained model downloads, and cloud services are not installed by the current setup.

For a different operating system or Python minor version, resolve `requirements.in` in a separate environment, execute the full available batch, and record a new platform-specific lock. Do not claim the Windows freeze has verified that environment.

## Update procedure

1. Preserve the working lock and execution evidence.
2. Resolve chosen updates in an isolated environment.
3. Run package consistency, infrastructure, structure, link, and notebook checks.
4. Review changed numerical results and plots; a successful import is insufficient.
5. Record the tested versions and regenerate status. Never use global package installation to repair a local project.
