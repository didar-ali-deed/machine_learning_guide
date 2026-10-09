# Assessment and mastery rubric

Score each dimension from 0 to 3: 0 absent, 1 copied or substantially incorrect, 2 mostly correct with a minor gap, 3 correct and independently explained.

| Dimension | Evidence for a score of 3 |
|---|---|
| Meaning | Explain the problem, row meaning, units, and prediction deadline |
| Mathematics | Define symbols and calculate a tiny example without code |
| Implementation | Reproduce the calculation and explain each important operation |
| Diagnosis | Check shapes, boundary cases, missingness, and plausible failures |
| Evaluation | Use an appropriate metric and avoid unavailable information |
| Communication | Interpret a plot and state limitations without overstating evidence |

A useful study gate is at least 14/18 with no zero dimension. This is a self-study rule, not a validated certification scale. Revisit any weak prerequisite even when the total passes.

## Foundation assessment

Given three past daily counts 4, 8, and 12 and two future outcomes 7 and 13: define a constant model, train it by hand, compute future MAE, reproduce the result, and visualize observations against predictions. Explain why fitting on all five outcomes changes the meaning of evaluation.

Answer: training mean is eight; absolute future errors are one and five; MAE is three. A horizontal prediction line makes deviations visible. Incorporating the future outcomes before prediction leaks the answers. Extra credit: distinguish averaging error magnitude from averaging signed error, where cancellation can hide mistakes.
