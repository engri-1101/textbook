# Geometry of the Simplex Method

Let's revisit the 2-dimensional example earlier, to visualize what the Simplex
Method is doing. The LP we considered was

$$\begin{align*}
\text{maximize}\ & 3x+2y\\
\text{such that}\\ & x \leq 4 \\
& y \leq 2 \\
& 2x + y \leq 6 \\
& y-x \leq 1 \\
& x \geq 0\\
& y \geq 0.
\end{align*}$$

The feasible region looks as follows.

```{attention} Feasible region should be here.
```

The first step of the Simplex Method rewrites the LP by introducing a new
variable for every constraint, let's call them $z_1$, $z_2$, $z_3$ and $z_4$,
and a new variable $z_0$ for the objective function.

$$\begin{alignat*}{20}
\text{maximize}\ &&z_0&=\ &&& 3x&+&2y\\
\text{such that}\& & z_1 &=& 4 &-& x \\
&& z_2 &=& 2 && &-& y \\
&& z_3 &=& 6 &-& 2x &-&y\\
&& z_4 &=& 1 &+& x &-& y
\end{alignat*}$$

$$x,y,z_1,z_2,z_3,z_4\geq 0.$$

The feasible solution associated with this dictionary is $ x= y=0$, and $
z_1=4$, $ z_2=2$, $ z_3=6$, $ z_4=1$. This corresponds to the origin in our
drawing (we will ignore the variables $z_1$, $z_2$, $z_3$ and $z_4$, because we
are only interested in $x$ and $y$ originally, and we know that the feasible
region of this first dictionary is the same as the feasible region of the
original LP in terms of the original variables).

```{attention} Initial feasible solution.
```

We can now choose to increase either $x$ or $y$ - let's choose $y$. The most
restricting constraint is constraint number 4. We solve for the equation for
$y$, and get $y=1+x-z_4$. We replace the fourth constraint with this equation,
and substitute $1+x-z_4$ for $y$ in every other constraint and the objective
function, and get

$$\begin{alignat*}{20}
\text{maximize}\ &&z_0&=\ &&& 3x&+&2(1+x-z_4)\\
\text{such that}\& & z_1 &=& 4 &-& x \\
&& z_2 &=& 2 && &-& (1+x-z_4) \\
&& z_3 &=& 6 &-& 2x &-&(1+x-z_4)\\
&& y &=& 1 &+& x &-& z_4
\end{alignat*}$$

$$x,y,z_1,z_2,z_3,z_4\geq 0.$$

which simplifies to

$$\begin{alignat*}{20}
\text{maximize}\ &&z_0 &=\ &2&+& 5x&-&2z_4\\
\text{such that}\& & z_1 &=& 4 &-& x \\
&& z_2 &=& 1 &-&x &+& z_4 \\
&& z_3 &=& 5 &-& 3x &+&z_4\\
&& y &=& 1 &+& x &-& z_4
\end{alignat*}$$

$$x,y,z_1,z_2,z_3,z_4\geq 0.$$

The feasible solution associated with this dictionary is $ x= z_4=0$, and
$y=1$, $ z_1=4$, $ z_2=1$, $ z_3=5$. This corresponds to the point $(0,1)$ in
our drawing (again ignoring the variables $z_1$, $z_2$, $z_3$ and $z_4$,
because we are only interested in $x$ and $y$).

```{attention} First iteration should be here
```

The Simplex Method increased the $y$-variable as much as possible, until it hit
one of the constraints, in particular the constraint $y-x\leq 1$ here! In the
dictionary this corresponded to the constraint $z_4 = 1 + x - y$, which was
indeed the most limiting constraint.

We can now increase $x$. The most restricting constraint is constraint number
2. We solve for the equation for $x$, and get $x=1-z_2+z_4$. We replace the
second constraint with this equation, and substitute $1-z_2+z_4$ for $x$ in
every other constraint and the objective function, and get

$$\begin{alignat*}{20}
\text{maximize}\ &&z_0 &=\ &2&+& 5(1-z_2+z_4)&-&2z_4\\
\text{such that}\& & z_1 &=& 4 &-& (1-z_2+z_4) \\
&& x &=& 1 &-&z_2 &+& z_4 \\
&& z_3 &=& 5 &-& 3(1-z_2+z_4) &+&z_4\\
&& y &=& 1 &+& (1-z_2+z_4) &-& z_4
\end{alignat*}$$

$$x,y,z_1,z_2,z_3,z_4\geq 0.$$

which simplifies to

$$\begin{alignat*}{20}
\text{maximize}\ &&z_0 &=\ &7&-& 5z_2&+&3z_4\\
\text{such that}\& & z_1 &=& 3 &+& z_2&-&z_4 \\
&& x &=& 1 &-&z_2 &+& z_4 \\
&& z_3 &=& 2 &+& 3z_2 &-&2z_4\\
&& y &=& 2 &-& z_2
\end{alignat*}$$

$$x,y,z_1,z_2,z_3,z_4\geq 0.$$

The feasible solution associated with this dictionary is $ z_2= z_4=0$, and
$x=1$, $y=2$, $ z_1=3$, $ z_3=2$. This corresponds to the point $(1,2)$ in our
drawing.

```{attention} Second iteration should be here
```

The Simplex Method now increased the $x$-variable as much as possible, until it
hit one of the constraints, in particular the constraint $y\leq 2$ here ---
this constraint actually limited the increase of $x$, because $y$ is set equal
to $1+x-z_4 = 1+x$ (because we are keeping $z_4$ fixed at $0$)! This implies
the limit $1+x \leq 2$, or $x\leq 1$, which is indeed the limit that the
Simplex Method put on $x$. In the dictionary this corresponded to the
constraint $z_2 = 1 - x + z_4$, which was indeed the most limiting constraint.

We can start to see a pattern here.

```{note}

The point is that the solution associated with the dictionaries in Simplex
Method correspond to "corner points" of the feasible region. Intuitively we
can interpret every step in the Simplex Method as moving the current feasible
solution to a next one, by moving along a boundary line of the feasible region,
until a next constraint is hit.
```

Let's finish this example for completeness' sake - fully understanding the
reasoning about the relationship of the constraints in the dictionary and the
original LP is not as important as the geometric insight that we have gained.

Increasing $z_4$ can still improve the solution. The most restricting
constraint is the third constraint. We solve for the equation for $z_4$, and
get $z_4=1+\tfrac 32 z_2 - \tfrac 12 z_3$. We replace the third constraint with
this equation, and substitute $1+\tfrac 32 z_2 - \tfrac 12 z_3$ for $z_4$ in
every other constraint and the objective function, and get

$$\begin{alignat*}{20}
\text{maximize}\ &&z_0 &=\ &7&-& 5z_2&+&3(1+\tfrac 32 z_2 - \tfrac 12 z_3)\\
\text{such that}\& & z_1 &=& 5 &+& z_2&-&(1+\tfrac 32 z_2 - \tfrac 12 z_3) \\
&& x &=& 1 &-&z_2 &+& (1+\tfrac 32 z_2 - \tfrac 12 z_3) \\
&& z_4 &=& 1 &+& \tfrac 32 z_2 &-&\tfrac 12z_3\\
&& y &=& 2 &-& z_2
\end{alignat*}$$

$$x,y,z_1,z_2,z_3,z_4\geq 0.$$

which simplifies to

$$\begin{alignat*}{20}
\text{maximize}\ &&z_0 &=\ &10&-& \tfrac 12 z_2&-&\tfrac 32 z_3\\
\text{such that}\& & z_1 &=& 4 &-& \tfrac 12 z_2&+& \tfrac 12 z_3 \\
&& x &=& 2 &+&\tfrac 12 z_2 &-&  \tfrac 12 z_3 \\
&& z_4 &=& 1 &+& \tfrac 32 z_2 &-&\tfrac 12z_3\\
&& y &=& 2 &-& z_2
\end{alignat*}$$

$$x,y,z_1,z_2,z_3,z_4\geq 0.$$

The feasible solution associated with this dictionary is $ z_2= z_3=0$, and
$x=2$, $y=2$, $z_1=4$, $ z_4=1$. This corresponds to the point $(2,2)$ in our
drawing.

```{attention} Third iteration should be here
```

The Simplex Method now increased the $z_4$-variable as much as possible, until
it hit one of the constraints, in particular the constraint $2x+y\leq 6$ here -
this constraint actually limited the increase of $z_4$, because $x$ is set
equal to $1-z_2+z_4 = 1+z_4$ (because we are keeping $z_2$ equal to $0$) and
$y$ is set equal to $2-z_2 = 2$. Note that $6\geq 2x+y = 2(1+z_4)+2=4+2z_4$
which implies the limit $z_4\leq 1$. In the current dictionary  $2x+y\leq 6$
corresponded to the constraint $ z_3 = 2 + 3z_2 -2z_4$, which was indeed the
most limiting constraint. Also note that this indeed means that $x$ now
increases to $2$ (because $x=1+z_4$).
