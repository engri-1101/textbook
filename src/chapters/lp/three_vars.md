# Soldiering On - Linear Programs with Three Variables

How about finding the optimal solution to the following LP:

$$\begin{align*}
\text{maximize}\ & 2x_1+x_2+x_3\\
\text{st}\ & x_1 \leq 4 \\
& x_2 \leq 4 \\
& x_1 + x_2 \leq 6 \\
& -x_1+2x_3 \leq 4 \\
& x_1, x_2, x_3 \geq 0.
\end{align*}$$

With the help of a computer (or exercising an inordinate amount of patience)
one might be able to plot this in 3-dimensional space. In fact, the
accompanying lab exercise will give you a computational tool to do exactly
this, but without such a tool, carefully graphing this problem would not really
be feasible. And even after solving this LPs with 3 variables, we would not be
content, because we would also want to solve LPs with 4, 5, 10, 27, etc.
variables. We thus need a different method, and abandon our current effort of
solving LPs graphically. We can console ourselves that the previous hard labor
at least gave us some geometric insight in what the feasible region and the
objective function of a Linear Program look like (and what points to consider
when looking for an optimal solution).[^footnote1]

[^footnote1]: In the first example the constraints corresponded to half-open
intervals of form $[a,\infty)$ or $(-\infty,b]$, the border of this region
being a (0-dimensional) point. In the second, the constraints corresponded to
*half-planes*, planar regions consisting of all points on one side of a
line, the border being a (1-dimensional) line. In 3 dimensions the constraints
will correspond to *3-dimensional half-spaces*, 3-dimensional regions
consisting of all points on one side of a plane, the border being a
(2-dimensional) plane. I think you can see a pattern here. In $n$-dimensional
space the constraints will correspond to $n$-dimensional half-spaces,
$n$-dimensional regions consisting of all points on one side of a
$(n-1)$-dimensional half-space, the border being an $(n-1)$-dimensional
half-space. Good luck picturing that!
