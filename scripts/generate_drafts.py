"""Populate every missing inventory notebook with an explicit unexecuted draft.

Never overwrite an existing lesson. A draft is a topic brief and code starting
point, not a completed 21-section academy lesson. No notebook code runs here.
"""
from __future__ import annotations
import json
import os
from pathlib import Path
from academy_tools import ROOT, inventory
from draft_material import CARDS, ESTIMATORS, CLUSTERS, REDUCERS


def estimator_demo(record, spec):
    classification = spec['task'] == 'classification'
    classes = 3 if record['id'] in {'06-02', '06-03'} else 2
    features = 1 if record['id'] == '05-01' else 4
    data = (f"from sklearn.datasets import make_classification\n"
            f"X, y = make_classification(n_samples=160, n_features=4, n_informative=3,\n"
            f"    n_redundant=0, n_classes={classes}, n_clusters_per_class=1, random_state=42)"
            if classification else
            f"from sklearn.datasets import make_regression\n"
            f"X, y = make_regression(n_samples=160, n_features={features}, noise=5, random_state=42)")
    if spec['name'] == 'PoissonRegressor':
        data += "\nrng = np.random.default_rng(42)\ny = rng.poisson(np.exp(.2*X[:, 0] + .1*X[:, 1]))"
    prep = spec['preparation']
    if prep == 'nonnegative':
        data += "\n# Fixed feature map; not fitted using held-out rows.\nX = np.maximum(np.rint(3 + X), 0)"
    elif prep == 'binary':
        data += "\nX = (X > 0).astype(float)"
    stratify = ', stratify=y' if classification else ''
    stratify_train = ', stratify=y_fit' if classification else ''
    data += f"""
from sklearn.model_selection import train_test_split
X_fit, X_test, y_fit, y_test = train_test_split(
    X, y, test_size=.2, random_state=42{stratify})
X_train, X_validation, y_train, y_validation = train_test_split(
    X_fit, y_fit, test_size=.25, random_state=43{stratify_train})
assert len(X_train) + len(X_validation) + len(X_test) == len(X)
"""
    constructor = f"{spec['name']}({spec['arguments']})"
    fitting = f"from {spec['module']} import {spec['name']}\n"
    if prep in {'nonnegative', 'binary'}:
        fitting += f"model = {constructor}\n"
    else:
        fitting += "from sklearn.pipeline import make_pipeline\nfrom sklearn.preprocessing import StandardScaler\n"
        fitting += f"model = make_pipeline(StandardScaler(), {constructor})\n"
    fitting += "model.fit(X_train, y_train)\nvalidation_prediction = model.predict(X_validation)\n"
    fitting += "assert validation_prediction.shape == y_validation.shape\n"
    if classification:
        evaluation = """from sklearn.metrics import accuracy_score, f1_score
print('Validation accuracy:', accuracy_score(y_validation, validation_prediction))
# No configuration search is performed against the test data.
test_prediction = model.predict(X_test)
print('Final synthetic test accuracy:', accuracy_score(y_test, test_prediction))
print('Final synthetic macro F1:', f1_score(y_test, test_prediction, average='macro', zero_division=0))
"""
    else:
        evaluation = """from sklearn.metrics import mean_absolute_error, mean_squared_error
print('Validation MAE:', mean_absolute_error(y_validation, validation_prediction))
# No configuration search is performed against the test data.
test_prediction = model.predict(X_test)
print('Final synthetic test MAE:', mean_absolute_error(y_test, test_prediction))
print('Final synthetic test RMSE:', np.sqrt(mean_squared_error(y_test, test_prediction)))
"""
    return [data.strip(), fitting.strip(), evaluation.strip()]


def cluster_demo(spec):
    return [f"""from sklearn.datasets import make_blobs
from sklearn.cluster import {spec['name']}
from sklearn.metrics import silhouette_score
X, generation_labels = make_blobs(n_samples=80, centers=3, cluster_std=.45, random_state=42)
model = {spec['name']}({spec['arguments']})
labels = model.fit_predict(X)
assert labels.shape == (len(X),)
print('Assigned labels:', np.unique(labels, return_counts=True))
# Descriptive in-sample geometry, not supervised test accuracy.
retained = labels >= 0
if 1 < len(np.unique(labels[retained])) < retained.sum():
    print('Non-noise silhouette:', silhouette_score(X[retained], labels[retained]))
else:
    print('Silhouette undefined for this extracted partition.')
""".strip()]


def reducer_demo(spec):
    preprocessing = "X = np.abs(X)" if spec['name'] == 'NMF' else ''
    return [f"""from sklearn.datasets import make_blobs
from sklearn.{spec['module']} import {spec['name']}
X, generation_labels = make_blobs(n_samples=80, n_features=4, centers=3, random_state=42)
{preprocessing}
model = {spec['name']}({spec['arguments']})
representation = model.fit_transform(X)
assert representation.shape == (80, 2)
assert np.isfinite(representation).all()
print('In-sample representation shape:', representation.shape)
# This is a representation illustration, not a held-out predictive experiment.
""".strip()]


def render_draft(record, lookup):
    ident = record['id']
    card = CARDS[ident]
    if ident in ESTIMATORS:
        demos = estimator_demo(record, ESTIMATORS[ident])
    elif ident in CLUSTERS:
        demos = cluster_demo(CLUSTERS[ident])
    elif ident in REDUCERS:
        demos = reducer_demo(REDUCERS[ident])
    else:
        demos = [card['example']]
    if not all(demos):
        raise ValueError(f'Missing computational material: {ident}')
    for index, code in enumerate(demos):
        compile(code, f'{ident}:draft-demo-{index}', 'exec')
    prereqs = []
    parent = Path(record['path']).parent
    for previous in record['prerequisites']:
        relative = os.path.relpath(lookup[previous]['path'], parent).replace('\\', '/')
        prereqs.append(f"[{previous}: {lookup[previous]['title']}]({relative})")
    all_records = list(lookup.values())
    position = next(i for i, r in enumerate(all_records) if r['id'] == ident)
    next_record = all_records[position+1] if position+1 < len(all_records) else None
    next_link = (f"[{next_record['title']}]({os.path.relpath(next_record['path'], parent).replace(chr(92), '/')})"
                 if next_record else '[progress ledger](../PROGRESS.md)')
    blocks = '\n\n'.join('```python\n'+demo+'\n```' for demo in demos)
    dependency_note = ('This is an optional-library or larger-model topic. The included core/fallback does not install that library, download weights, or claim to reproduce its complete algorithm.'
                       if record['optional'] else
                       'The included example uses local or synthetic observations. Any simplified mechanism is a teaching starting point, not a production-equivalent implementation.')
    return f"""# {record['title']}

> **GENERATED DRAFT — NOT EXECUTED OR EDUCATIONALLY VERIFIED.** This topic brief and code starting point was created under the user's generation-only instruction. It is not the academy's complete 21-section lesson. Full derivations, six worked exercises, plots, realistic comparisons, and manual review remain pending. Syntax validation does not prove numerical correctness or runtime compatibility.

## Learning focus and prerequisites

Learn to identify the central mechanism of **{record['title']}**, inspect its inputs and outputs, and recognize the limitation described below. Read prerequisites first: {', '.join(prereqs) or 'none'}. Module objective: {record['outcome']}

## Topic explanation

{card['explanation']}

## Inspectable computational starting point

The code uses `np` as the NumPy alias and `pd` as the pandas alias. `np.array` constructs an array, `@` denotes matrix multiplication, and `assert` states an expected invariant or worked value. Print the intermediate objects and check their shapes before interpreting a result. An assertion is a proposed check here; it has not been run in this draft.

```python
import numpy as np
import pandas as pd
```

{blocks}

## Experiment and reasoning tasks

1. Predict the printed quantities from the supplied example before running any cells. Explain how each input contributes to the result.
2. Change one relevant input or configuration and explain why the result should change. Identify an edge case where the displayed rule or model would be inappropriate.
3. Separate what this example demonstrates from what a complete study of {record['title']} would need to establish. Describe a validation boundary appropriate to its real application.

The supplied assertions document some expected values or structural invariants. They are not a complete worked-solutions section. Write your reasoning in private study notes and consult the reviewed prerequisites when a mathematical or Python step is unfamiliar.

## Assumptions, limitations, and pending work

{dependency_note} No paid API, credential, server, system installation, or optional plugin is required by the displayed starting point. The example must still receive numerical review and optional fresh-kernel testing before it can be labeled verified. Synthetic examples do not establish population performance. Any fitted preprocessing must use training observations only; future and test outcomes must stay outside model selection.

Pending authoring: intuition and analogy expansion; symbol/unit/shape definitions for every equation; manual derivation; essential scratch mechanism; library comparison; meaningful plots; hyperparameter experiments; six exercises with detailed solutions; five answered knowledge questions; five explained interview questions. Algorithm topics must explain learned parameters, prediction internals, assumptions, failure modes, and alternatives. Capstone topics additionally need the complete business-to-report workflow. This explicit backlog prevents a populated file from being mistaken for a finished course chapter.

## Navigation

Continue to {next_link}. Consult the [syllabus](../SYLLABUS.md), [student guide](../STUDENT_GUIDE.md), and [exact progress ledger](../PROGRESS.md) for the learning route and verification status.
"""


def main():
    records = inventory()
    lookup = {r['id']: r for r in records}
    missing = [r for r in records if not (ROOT/'lesson_sources'/f'{r["id"]}.lesson').exists()]
    absent = [r['id'] for r in missing if r['id'] not in CARDS]
    if absent:
        raise SystemExit(f'Topic-specific material missing for {absent}; no generic fallback written.')
    manifest_path = ROOT/'reference_materials/draft_lessons.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8')) if manifest_path.exists() else {}
    rendered = [(r, render_draft(r, lookup)) for r in missing]
    for record, source in rendered:
        destination = ROOT/'lesson_sources'/f'{record["id"]}.lesson'
        if destination.exists():
            raise RuntimeError(f'Refusing to overwrite existing lesson: {destination}')
        destination.write_text(source, encoding='utf-8')
        manifest[record['id']] = {'status':'draft', 'execution':'not requested',
                                 'full_educational_treatment':'pending', 'source':str(destination.relative_to(ROOT)).replace('\\','/')}
    manifest_path.write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
    print(f'Wrote {len(rendered)} topic-specific draft sources; preserved {len(records)-len(rendered)} existing lessons. No notebook was executed.')


if __name__ == '__main__':
    main()
