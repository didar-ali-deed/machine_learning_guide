# Mathematics reference — explained foundation edition

This is a revision aid, not a replacement for derivations and exercises. Detailed probability, matrix factorization, information theory, and multivariable optimization notebooks remain in the [planned mathematics module](02_Mathematics_for_ML/README.md).

## Arithmetic and means

A fraction $a/b$ divides an amount into $b$ equal parts, with $b\ne0$. A percentage is a fraction of one hundred: $3/4=0.75=75\%$. A power repeats multiplication: $2^3=2\times2\times2=8$.

For n observed numerical values $x_i$, the mean is $\bar x=(1/n)\sum_{i=1}^n x_i$. The sum symbol instructs us to add each indexed value. For 2, 4, 6, the mean is 12/3=4. It retains the measurement's units. An extreme value can move the mean substantially; a median uses the middle sorted position instead.

## Weighted sums and shapes

For X with shape `(n,p)` and weights w with shape `(p,)`, predictions are $\hat y=Xw+b$. Each row produces one output. The scalar b is added to every row's weighted sum. For features `[2,1]`, weights `[3,5]`, and b=2, the prediction is $6+5+2=13$.

Each product must contribute compatible output units. If a feature is area and the output is money, its coefficient has money-per-area units. Matching shapes cannot detect an incorrect feature order. The [matrix lesson](02_Mathematics_for_ML/07_scalars_vectors_and_matrices.ipynb) works through this mechanism.

## Distances and spread

Euclidean distance between equal-length vectors x and z is $\sqrt{\sum_j(x_j-z_j)^2}$. Between `(0,0)` and `(3,4)` it is five. Its interpretation depends on comparable coordinate scales; dollars and years should not be mixed without a deliberate metric.

Sample variance is $s^2=\sum_i(x_i-\bar x)^2/(n-1)$ for n>1. For 2, 4, 6, deviations are -2, 0, 2 and squared deviations sum to eight, giving variance four. Standard deviation is $s=\sqrt{s^2}=2$. Variance has squared units; standard deviation returns to original units. The n-1 denominator corrects bias for estimating population variance under standard independent-sampling assumptions; a descriptive population variance uses n instead.

## Derivatives and optimization

A derivative is $f'(x)=\lim_{h\to0}[f(x+h)-f(x)]/h$. For $f(x)=x^2$, expanding the numerator gives $2x+h$, whose limit is $2x$. At x=3 the slope is six. Derivative units are output units divided by input units.

The chain rule for $f(g(x))$ is $f'(g(x))g'(x)$. If $g(x)=x-3$ and $f(u)=u^2$, the derivative of $(x-3)^2$ is $2(x-3)\times1$. A gradient collects corresponding partial derivatives in multiple dimensions.

Gradient descent updates $w\leftarrow w-\eta\nabla L(w)$, where L is the objective and positive eta is the learning rate. For $L=(w-3)^2$, starting at zero with eta=0.1 gives $w=0.6$. This lowers loss from nine to 5.76. A larger step can overshoot; [the derivative lesson](02_Mathematics_for_ML/03_functions_and_derivatives.ipynb) derives the exact stable interval for this quadratic.

## Prediction losses

For n predictions $\hat y_i$ and outcomes $y_i$, MAE is $(1/n)\sum_i|\hat y_i-y_i|$. Predictions `[4,4]` against `[5,7]` give `(1+3)/2=2` in target units. MSE is $(1/n)\sum_i(\hat y_i-y_i)^2$, giving `(1+9)/2=5` in squared target units. Squaring penalizes large errors more strongly. RMSE takes the square root of MSE and restores target units.

For a linear model with residual vector $r=Xw-y$, $L=\|r\|_2^2/n$ has gradient $\nabla_wL=2X^Tr/n$. X is `(n,p)`, r is `(n,)`, and the result is `(p,)`. The full regression sequence will derive this step by step; the formula is provided here for revision, not as a completed derivation.

## Probability

For equally likely outcomes, probability is favorable outcomes divided by all possible outcomes. Conditional probability is $P(A\mid B)=P(A\cap B)/P(B)$ when P(B)>0: restrict attention to cases where B occurred. If two of five rainy days had delays, the observed conditional delay frequency is 2/5, not two divided by all recorded days.

Bayes' rule is $P(A\mid B)=P(B\mid A)P(A)/P(B)$. For an invented event with P(A)=0.1, P(B|A)=0.8, and P(B|not A)=0.2, total P(B)=0.08+0.18=0.26. The posterior is 0.08/0.26, approximately 0.308. A common mistake is reversing P(B|A) and P(A|B).

## Classification metrics

Define TP as true positives, FP false positives, FN false negatives, and TN true negatives. Precision is TP/(TP+FP); recall is TP/(TP+FN); specificity is TN/(TN+FP). With TP=8, FP=2, FN=4, precision is 0.8 and recall is 2/3. State what happens when a denominator is zero rather than silently assigning meaning to an undefined ratio.

Binary cross-entropy for one label y in `{0,1}` and predicted positive probability p is $-[y\log p+(1-y)\log(1-p)]$. For y=1 and p=0.8, it is approximately 0.223 using natural logarithms. It strongly penalizes confident wrong predictions. Numerically stable implementations should operate on logits when available.

## Information and regularization

Entropy $H(p)=-\sum_k p_k\log p_k$ summarizes uncertainty for a discrete probability distribution; zero-probability terms contribute zero by their limit. A fair binary distribution has entropy $\log2$ nats. KL divergence $D_{KL}(p\|q)=\sum_kp_k\log(p_k/q_k)$ compares distributions and is generally asymmetric; if q assigns zero probability where p is positive, it is infinite.

Ridge adds $\lambda\sum_jw_j^2$ to a data-fitting objective; Lasso adds $\lambda\sum_j|w_j|$. Lambda controls penalty strength. Exact scaling conventions differ across estimators, so compare the documented objective before transferring a numerical hyperparameter. Scaling features and handling the intercept consistently are essential.
