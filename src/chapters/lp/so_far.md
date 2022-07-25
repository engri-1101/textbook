# Optimization Models So Far

Let us take a step back, and have a closer look at the range of different
optimization models that we have seen so far in this course. All of these
formulations had

- decision variables (often denoted by $x$ with some index),
- constraints on these variables, and
- an objective function in terms of these variables.

For instance, given an instance of the Max Flow Problem (a directed graph
$G=(V,A)$ with nodes $s,t\in V$ and capacities $u(v,w)$ for every arc $(v,w)\in
A$), the Max Flow Problem could be formulated

- with decision variables $f(v,w)$ for each $(v,w) \in A$,
- with two types of constraints:
    - capacity constraints: $0 \leq f(v,w) \leq u(v,w)$ for each $(v,w) \in A$,
      and
    - flow conservation constraints: $\sum_{(w,v)\in A} f(w,v) = \sum_{(v,w)\in
      A} f(v,w)$ for each node $v \in N \setminus \{s,t\}$,
-  and the objective (the value of the flow) expressed in terms of the
   variables: ${\sum_{(w,t) \in A} f(w,t) - \sum_{(t,w)\in A} f(t,w)}$.

In short, we had the following mathematical programming formulation for the Max
Flow Problem.

```{admonition} Max Flow Problem
$$\begin{align*}
\text{maximize}\ & \sum_{(w,t) \in A} f(w,t) - \sum_{(t,w)\in A} f(t,w) \\
\text{st}\ & \sum_{(w,v)\in A} f(w,v) = \sum_{(v,w)\in A} f(v,w) &&
\text{for each node $v \in N \setminus \{s,t\}$,} \\
& 0 \leq f(v,w) \leq u(v,w) && \text{for each $(v,w) \in A$.}
\end{align*}$$
```

As a second example, recall the Assignment Problem. Here we had decision
variables $x_{ij}$ for each worker $i$ and task $j$, taking on a value $0$ or
$1$.  These had the following interpretation: if $x_{ij}=1$ then worker $i$ is
assigned to task $j$, and if $x_{ij}=0$ then worker $i$ is *not* assigned
to task $j$.  Using these decision variables, we could then express the
constraint that every task must be assigned to exactly one worker as

$$\sum_{i=1}^n x_{ij} = 1 \text{ for each task $j=1,\ldots,n$},$$

and the constraint that every worker must be assigned exactly one task as

$$\sum_{j=1}^n x_{ij} = 1 \text{ for each worker $i=1,\ldots,n$}.$$

The objective for this problem is the total time required to execute all tasks,
which can be expressed in terms of the decision variables as $\sum_{i=1}^n
\sum_{j=1}^n t_{ij} x_{ij}$.

Summarizing, we had the following mathematical programming formulation for the
Assignment Problem.

```{admonition} Assignment Problem
$$\begin{align*}
\text{minimize}\ & \sum_{i=1}^n \sum_{j=1}^n t_{ij} x_{ij} \\
\text{st}\ & \sum_{i=1}^n x_{ij} = 1  && \text{ for each task $j=1,\ldots,n$,} \\
& \sum_{j=1}^n x_{ij} = 1 && \text{ for each worker $i=1,\ldots,n$,} \\
& x_{ij} \in \{0,1\} && \text{ for each $i=1,\ldots,n;\ j=1,\ldots,n$}.
\end{align*}$$
```

Ignoring the fact that the decision variables in the Assignment Problem can
only take on two values ($0$ or $1$), we see that the constraints and objective
functions of both these optimization formulations involve only *linear
functions* in the decisions variables!

```{admonition} Definition
A function $f(x_1,x_2,\ldots,x_n)$ is  **a linear function** (in the variables
$x_1, x_2, \ldots, x_n$) if it can be written as

$$f(x_1,x_2,\ldots,x_n) = c_0 + c_1 x_1 + c_2 x_2 + \cdots + c_n x_n$$

for some *constants* $c_0, c_1, \ldots, c_n$ (i.e., numbers that do not depend
on $x_1, x_2, \ldots, x_n$).
```

In fact, all the problems that we have studied so far in this course have
formulations that only involve linear functions, and lots of other problems can
be modeled using only linear functions as well! In this handout we will study
how to find optimal solutions to such mathematical programs.
