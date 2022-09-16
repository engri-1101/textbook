# Mathematical Model

```{admonition} Shortest path problem
**input:**
- a directed graph $G=(N,A)$,
- a *source* node $s$ (which is in $N$), 
- a non-negative length $\ell (i,j)$ for each
arc $(i,j)$ in $A$

**output:**
- a path from $s$ to each node $i$ in $N$

**goal:**
minimize the length of the path from $s$ to $i$, for each $i\in N$

```

Note that unlike the traveling salesman problem, we do not need to go
through all other nodes on the way.

As the next step, we shall explain why this problem can be used
to model our problem of finding the quickest way to the office.
We can model the map of our city
by a graph as follows. Introduce a node for each intersection
on the map. For each pair of intersections (say, 7th Ave. \& 33rd St. and
7th Ave. \& 32nd St.) if there is a street connecting them (going the
right way) and this street does not cross any other intersection along the way,
we introduce an arc from the node corresponding to the first intersection, 
to the
node corresponding to the second intersection. 
In our example, 7th Ave. is one-way
going downtown, and so there is only an arc from the first to the second
of them, and not from the second to the first. The length of an arc
is the length of time to drive between the two intersections in that
direction.
By solving the shortest path problem for the graph derived from our
city map, we can compute routes in the city.