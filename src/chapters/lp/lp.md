# Linear Programming

```{admonition} Definition

A **Linear Program** (or Linear Programming Problem) is an optimization problem
with a {\em linear} objective function, and constraints that are either
"$\leq$", "$\geq$" or "$=$"-constraints, that have *linear* functions on *both*
sides of the (in)equality.
```

**Examples.** Examples of Linear Programs (LPs for short) are the mathematical
programming formulation of the Max Flow Problem above, as well as the
mathematical programming formulation of the Assignment Problem, if we change
the constraints  $x_{ij} \in \{0,1\}$ for all $i,j$ to $0 \leq x_{ij} \leq 1$
for all $i,j$. (We will get back to mathematical programs with restrictions
that variables have to be integer in the very near future.)

$$
\begin{align*}
\text{minimize}\ & 2x \\
\text{such that}\ & x \geq 5 \\
& 2x \leq 16 \\
& 5x \leq 50.
\end{align*}
$$

As you know, as soon as we define a new problem in this course (in this case a
generalization of the problems we saw before), our goals then are (1) to come
up with an algorithm to find an optimal solution for this problem, and (2) to
find a (relatively easy) argument to show that a solution is indeed optimal. We
will now tackle the first goal. The second goal will also be addressed here,
but we will actually see a more satisfying argument at a later point in this
course.
