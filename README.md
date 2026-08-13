# Riemann-Sum-Simulator
Visualizes left, right, midpoint, trapezoidal, and Simpson's rule approximations of the definite integral of $f(x) = x^3 − 7x^2 + 15x − 8$ on [1, 4].  Compares the approximation to the exact integral value and reports percent error, updating live as you adjust the subinterval count, $n$

First version of this repo (file: Riemann_Quadratic.py) used a $f(x)$ with a constant second derivative and this muddled the overall trend of approximation accuracy that is important to demonstrate and understand. Specifically, the midpoint method outperformed the trapezoidal rule - the midpoint rule is surprisingly accurate on symmetric concave-down curves because of a fortuitous partial cancellation of the over-approximations and under-approximations. The trapezoidal rule on a concave-down curve always undershoots - so every trapezoid is missing a little sliver of area with no cancellation to compensate. This is confusing to students learning about the preference of the trapezoidal rule over Riemann sums in numeric approximations.

To better incorporate the primary emphasis of this project into the repo, $f(x)$ was made into a more complicated, cubic function with defined and non-constant first and second derivative functions and regions of different concavity in the interval [1, 4]. Furthermore, Simpson's rule was also added, the display shows all 5 methods now (no more clicking between them) with $n$ adjusting all at once, and comparative data for the purpose of developing intuition is displayed in the same location for all 5 graphs.

Here is some information about each method. This does not necessarily reflect the approach committed in the code, but serves as the mathematical basis:

**1. Reimann Sums (Left, Right, and Midpoint)**

Riemann sums approximate areas under curves using $n$ number of adjacent rectangles, with one corner of each rectangle placed on the curve $f(x)$ (the height of a given rectangle is the value of $f(x)$ at that $x$-value.)

Using *left endpoints*, in series notation the sum under the curve is given by:

$$
S_{\text{left}}(n)=\sum_{i=1}^n f(m_i)\Delta x
$$

Where $m_i=a+(i-1)\Delta x$ and $\Delta x=\frac{b-a}{n}$. This is because in the interval [a, b] with the sum starting at $i=1$, the function height needs to be located at each rectangle's left endpoint, the first one starting at $a$ (the function height being $f(a)$) - so we need to subtract 1 off of $i$ to achieve that. Subsequently adding $i\Delta x$ locates the following rectangle for each iteration of the series up to $n$. $\Delta x$ is merely the width of each rectangle (which when multiplied by the former gives the area of the $i$-th rectangle) - $n$ equal-sized subintervals in [a, b] results in the given formula. So:

$$
\sum_{i=1}^n f(m_i)\Delta x=\frac{(b-a)}{n} \sum_{i=1}^n f(a+\frac{(b-a)(i-1)}{n})
$$

Using *right endpoints* and the same logic as we did previously:

$$
S_{\text{right}}(n)=\sum_{i=1}^n f(M_i)\Delta x
$$

$M_i$ now is simply $a+i\Delta x$ as the right endpoint and corresponding function height is located at the interval start value $a$ plus 1 subinterval. We need to start there, so we add just one $\Delta x$ to start. Everything else is the same. Clearly, computationally, especially if done by hand, this is a little easier the left Riemann sums, even if the results aren't the same for finite $n$. However, both left and right sums still have significant issues in estimating the areas under increasing and decreasing slopes without under-estimating or over-estimating.

$$
\sum_{i=1}^n f(M_i)\Delta x=\frac{(b-a)}{n} \sum_{i=1}^n f(a+\frac{(b-a)}{n}i)
$$

Using *midpoints* finally, we sample $f(x)$ at the center of each subinterval rather than either edge, in order to slightly mitigate the issue of under/over-approximation. The midpoint of the $i$-th subinterval is the average of its left and right endpoints:

$$
S_{\text{mid}}(n)=\sum_{i=1}^n f(\bar{m}_i)\Delta x
$$

Where $\bar{m}_i=a+(i-\frac{1}{2})\Delta x$. This is just the left endpoint formula $a+(i-1)\Delta x$ shifted right by half a subinterval width $\frac{\Delta x}{2}$, placing the sample point exactly at the center. So:

$$
\sum_{i=1}^n f(\bar{m}_i)\Delta x=\frac{(b-a)}{n}\sum_{i=1}^n f(a+\frac{(b-a)(2i-1)}{2n})
$$

The midpoint rule is generally more accurate than either left or right Riemann sums for smooth functions. Intuitively, the rectangle's flat top crosses the curve at the midpoint, so the region it overshoots on one side of that point tends to cancel with the region it undershoots on the other — a partial error cancellation that neither endpoint method benefits from.

Of course, the definition of the integral is the limit as $n$ goes to infinity. Knowledge in series and limit evaluation is needed to confirm this, but that's not the purpose of this project!

$$
\int_a^bf(x)\,dx=\lim_{n\to\infty}\sum_{i=1}^n f(a+i\Delta x)\Delta x
$$

**2. The Trapezoidal Rule**

A trapezoid is a quadrilateral with one pair of parallel sides ($b_1$ and $b_2$) of different lengths connected by two sides that are not parallel and do not necessarily have an angular or symmetrical relationship to one another. If they did, it would be a "regular trapezoid" which we do not use here. In the area approximation under curves, the parallel bases are oriented vertically and act as the height of the function at two points separated by one subinterval - $f(x_{i=k})$ and $f(x_{i=k+1})$. One of the two remaining sides acts as the perpendicular distance between them (the "height" or altitude $h$ of the trapezoid itself) - this is $\Delta x=\frac{b-a}{n}$. The fourth is merely drawn between the two function-side endpoints of the heights and is not important in the calculation of the area, which for a trapezoid is:

$$
A = \frac{1}{2}h(b_2+b_1)
$$

Substituting $h=\Delta x=\frac{b-a}{n}$, $b_1=f(x_i)$, and $b_2=f(x_{i+1})$, the area of the $i$-th trapezoid is $\frac{\Delta x}{2}[f(x_i)+f(x_{i+1})]$. Summing over all $n$ strips:

$$
S_{\text{trap}}(n) = \frac{b-a}{2n} \sum_{i=1}^{n} [f(x_i)+f(x_{i+1})] = \frac{b-a}{2n} \sum_{i=1}^{n} [f(a+(i-1)\Delta x)+f(a+i\Delta x)]
$$

Notice that when simplified every interior point $f(x_1), f(x_2),~ ... ~~, f(x_{n-1})$ appears twice in this sum - once as the right base of strip $i$ and once as the left base of strip $i+1$ — while only the endpoints $f(a)$ and $f(b)$ appear once each. This gives the equivalent and more compact (closed) telescoping form:

$$
S_{\text{trap}}(n)=\frac{b-a}{2n}[f(a)+2\sum_{i=1}^{n-1}f(x_i)+f(b)]
$$

Or in open form, we see the characteristic 1-2-2-2-1 weighting of the terms:

$$
S_{\text{trap}}(n) = \frac{b-a}{2n}[f(x_0) + 2f(x_1) + 2f(x_2) + 2f(x_3) + ~...~ + 2f(x_{n-2}) + 2f(x_{n-1}) + f(x_n)]
$$

**3. Simpson's Rule**

Just like the trapezoidal rule - this is a more advanced method of numerical integration that is resorted to when elementary functions simply do not have antiderivatives that are elementary functions. Programs like MATLAB use trapz functions to do integral analysis for instance, as they work for any continuous, defined curve. The difference between trapezoidal approximation and the method used in Simpon's rule is the order of the approximation of $f(x)$ - first-degree polynomials in the former, and second-degree polynomials in the latter - the idea being that a parabola hugs the curve more closely than a flat rectangle top or a straight trapezoid edge, so the error is smaller.

We use the general formula for a quadratic $p(x) = Ax^2 + Bx + C$ that passes through the three points $(x_{i-1}, f(x_{i-1}))$, $(x_i, f(x_i))$, and $(x_{i+1}, f(x_{i+1}))$ - or at the start of the interval, $(x_0, f(x_0))$, $(x_1, f(x_1))$, and $(x_2, f(x_2))$. Since three points uniquely determine a parabola, this fit is exact - but we then have to use subinterval pairs $[x_{i-1}, x_{i+1}]$ (or $[x_0, x_2]$) with even $n$ as a result. We then integrate $p(x)$ over that pair of subintervals rather than $f(x)$ itself. That is the gist.

$$
\int_{x_0}^{x_2} f(x)dx \approx \int_{x_0}^{x_2} p(x)dx
$$

Working out $\int_{x_0}^{x_2} (Ax^2 + Bx + C) dx$ directly and substituting back the three known function values, the result simplifies to:

$$
\frac{x_2 - x_0}{6}[f(x_0) + 4f(x_1) + f(x_2)]
$$

Since the pair of subintervals has total width $x_2 - x_0 = 2\Delta x$, this becomes $\frac{\Delta x}{3}[f(x_0) + 4f(x_1) + f(x_2)]$ per pair. The midpoint $f(x_1)$ carries a weight of 4 while the two endpoints carry weight 1 each, so the parabolic fit naturally emphasizes the center of the interval. Summing over all $n/2$ pairs (again, where $n$ must be even), we get:

$$
S_{\text{simp}}(n) = \frac{\Delta x}{3} \sum_{i=1,3,5,...}^{n-1} [f(x_{i-1}) + 4f(x_i) + f(x_{i+1})]
$$

Just as with the trapezoidal rule, every interior boundary point is shared between two adjacent pairs. Expanding the sum and collecting repeated terms - endpoints appear once, odd-indexed points always land on a midpoint so they carry weight 4, even-indexed interior points appear as an endpoint in two adjacent pairs so they carry weight 2, creating the signature alternating 4-2-4-2-4 interior weighting:

$$
S_{\text{simp}}(n) = \frac{b-a}{3n}[f(x_0) + 4f(x_1) + 2f(x_2) + 4f(x_3) + ~...~ + 2f(x_{n-2}) + 4f(x_{n-1}) + f(x_n)]
$$

This converges to the true integral faster than any of the rectangle methods or the trapezoidal rule as $n$ increases, because the error depends on the fourth derivative of $f$ rather than the second — meaning smooth functions are approximated almost exactly even at modest $n$. The user can see this in the Python simulation data section.
