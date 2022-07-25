# Finding an Optimal Solution of a Linear Program

Let us consider the simple example in the previous paragraph.

$$\begin{align*}
\text{minimize}\ & 2x\\
\text{such that}\ & x \geq 5 \\
& 2x \leq 16 \\
& 5x \leq 50.
\end{align*}$$

We can actually solve this problem by inspection: an optimal solution is $x^* =
5$, with objective value $2x^*=10$. How did we see this, and can we generalize
this intuition to linear programs that look more complicated? For this example,
we can simplify the constraints to $x\geq 5$, $x\leq 8$ and $x\leq 10$, and
combine these to be $x\in[5,8]$. To minimize the function $2x$ we obviously
want to make $x$ as small as possible, i.e., $5$. It is unclear how this
reasoning generalizes to give us a method for a linear program with more than
one variable, however.

Here is another way of reasoning: graphically.

```{attention} 1D graphical solve should be here
```

We associate values of $x$ with points on the number line. The border of the
region of values of $x$ that make a constraint feasible is drawn for every
constraint, with a pair of arrows indicating on which side the values of $x$
lie that make the constraint satisfied. The shaded region then is the
intersection of all these regions: it is the region containing the values of
$x$ for which all constraints are satisfied. To minimize $2x$ we find the point
in the shaded region that makes this function as small as possible: $x^*=5$.


Let's see if this idea generalizes to an LP with two variables. Let's consider
the following linear program.

$$\begin{align*}
\text{maximize} & 3x+2y\\
\text{such that}\ & x \leq 4 \\
& y \leq 2 \\
& 2x + y \leq 6 \\
& y-x \leq 1 \\
& x \geq 0\\
& y \geq 0.
\end{align*}$$

We can associate values of the variables with a point on the plane, associating
the first coordinate with the $x$-variable, and the second coordinate with the
$y$-variable.  Again, we plot the constraints as regions in the plane that
correspond to values of the variables such that a constraint is satisfied.

```{attention} 2D feasible region should be here
```

We now know which values for $x$ and $y$ are {\em feasible}, by which we mean
values so that all constraints are satisfied. We will refer to the region of
points corresponding to feasible solutions as the {\em feasible region} (the
shaded region in both pictures above).

Let's find an optimal solution: in the drawing this corresponds to a point in
the feasible region that has the best objective value. We can do this
graphically as well. Let's draw a line through all points corresponding to
solutions with objective value $6$ (where $6$ is just a arbitrary value that I
chose here). This is the line $3x+2y=6$, and we add it to the figure (it is the
dashed line in the drawing below).

```{attention} Isoprofit line (6) should be here
```

The line $3x+2y=6$ intersects the feasible region, which means all points in
this intersection of the line and the feasible region correspond to {\em
feasible} solutions that have objective value $6$. Are there solution with
higher objective value? Let's draw the line $3x+2y=9$.

```{attention} Isoprofit line (9) should be here
```

The line $3x+2y=9$ also intersects the feasible region, which means all points
in this intersection of this line and the feasible region correspond to
feasible solution with  objective value $9$. How about solutions with objective
value 12? We add the line $3x+2y=12$.

```{attention} Isoprofit line (12) should be here
```

This line has an empty intersection with the feasible region, from which we can
conclude that there are no feasible solutions with objective value $12$. But
what is now the best objective value we can achieve? From the picture above we
clearly get the right idea: we can think of the objective value as defining
parallel lines, one for each possible objective value. We are trying to push
this line as far to the top right as possible, while it still intersects the
feasible region.

```{attention} Isoprofit line (10) should be here
```

How did can we tell that $10$ is going to be the optimal objective value of the
Linear Program that we were trying to solve? We can conclude from the earlier
pictures that the line representing solutions with the highest objective value
are only going to intersect the feasible region in one point: the point that is
the intersection of the lines that represent the constraints $y\leq 2$ and
$2x+y\leq 6$ (i.e., the lines $y = 2$ and $2x+y = 6$). Simple algebra
immediately gives the intersection point, namely $x^*=2$, $y^*=2$, which
corresponds to an objective value of $3x^*+2y^*=10$.
