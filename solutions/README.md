# Worked solutions

All individual notebook exercises have detailed answers in section 18, followed by answered knowledge and interview questions. Solutions explain reasoning and caveats; a matching final number without valid reasoning is not sufficient.

## Cross-lesson practice answer

One row is one sale line. Product is categorical, quantity is an item count, and unit price is currency per item. Line revenues are 20, 20, 30, and 80. Product A totals 50, B totals 100, and the grand total is 150 currency units. Total quantity is ten items. Keep those two units distinct.

A product bar chart with a zero baseline displays the revenue comparison. It does not prove B is more profitable because costs are absent, nor prove a stable customer preference because only four invented transactions appear. A join to prices should be many-to-one and should reject unmatched products before calculating totals.

For future demand, use only information available before opening. A mean of earlier daily sales is an appropriate simple baseline. Keep later days for evaluation; choose any window length using an earlier validation period. Stockouts can censor true demand, so observed sales may understate what customers wanted.

## How to use a solution

Compare assumptions first, then calculations, then conclusions. If your answer differs because you stated a defensible alternative assumption, explain it. If the supplied answer reveals a prerequisite gap, redo the manual example with different values before moving forward.
