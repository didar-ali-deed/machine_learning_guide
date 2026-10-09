"""Small teaching utilities with explicit numerical input contracts."""
from __future__ import annotations

import math
from collections.abc import Iterable


def finite_mean(values: Iterable[int | float]) -> float:
    """Average nonempty finite ordinary Python numbers without changing inputs.

    Values must share measurement units. Boolean flags, missing values and
    nonfinite values are rejected. This teaching helper deliberately supports
    a narrower input domain than a general scientific statistics library.
    """
    snapshot = tuple(values)
    if not snapshot:
        raise ValueError("At least one measurement is required")
    for value in snapshot:
        if type(value) not in (int, float):
            raise ValueError("Expected ordinary Python numbers, excluding flags")
        if not math.isfinite(value):
            raise ValueError("Measurements must be finite")
    return math.fsum(snapshot) / len(snapshot)
