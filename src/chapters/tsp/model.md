# Mathematical Model

We now wish to formulate a mathematical model of this problem.  In order to do
this, we must first introduce some notation to describe the input in a concise
way. First of all, let the variable $n$ denote the number of cities. So, for
the particular input above, $n=7$. Then, we need some way to describe the
costs. We can index our cities as $1,2,3,4,5,6,7$ (sometimes the shorthand
$1,2,\ldots,7$ is used to indicate this).  In other words, NY corresponds to
city 1, Syracuse to city 2, and so forth. (If we are describing an arbitrary
input, then we refer to cities 1 through $n$, and this can then be denoted
$1,2,\ldots,n$, even if we have not specified the value that $n$ takes.) We can
use a doubly indexed array (or equivalently, a two-dimensional array) to
describe the table given above. Let $C[i,j]$ denote the cost of going from city
$i$ to city $j$, where $i$ and $j$ are variables that each can take any integer
value between 1 and $n$. Again, another shorthand notation for this is that the
costs are $C[i,j],$ $i=1,2,\ldots,n$, $j=1,2,\ldots,n$.  One final observation
about the input: in our example, the costs had the property that
$C[i,j]=C[j,i]$ for each $i=1,2,\ldots,n$, and each $j=1,2,\ldots,n$. In this
case, the input is said to be *it symmetric*.  There are cases in which the
input might not be symmetric, but this does not change any of the underlying
ideas involved.

Now we have given a way to describe the input. How do we describe what is a
feasible solution? We can describe the first tour proposed above by saying that
city 1 is first, city 3 is second, city 4 is third, and so forth. A more
mathematical description of this is to write that $\pi(1)=1$ (meaning that city
1 is first), $\pi(2)=3$ (meaning that city 3 is second), $\pi(3)=4$,
$\pi(4)=5$, $\pi(5)=6$, $\pi(6)=7$, and $\pi(7)=2$. We leave it implicit that
as the last part of the tour we return from city $\pi(7)$ to city $\pi(1)$. So
the general meaning of $\pi(i)=j$ is that city $j$ is the $i$th city of the
tour. To specify the tour, we must give a value to $\pi(i)$ for each
$i=1,\ldots,n$.  (Notice that the 2 has just disappeared from $1,2,\ldots,n$,
and this too is just a further shorthand.) For such a specification of
$\pi(i)$, $i=1,\ldots,n$, to be feasible, what properties must hold? Each city
must be visited, and each city must be visited at most once.  That is, for each
$j=1,\ldots,n$, there must exist exactly one $i$ (from amongst the integers 1
through $n$) such that $\pi(i)=j$. In this case, $\pi$ is called a *it
permutation*.  Notice that we did not require that the first city in the
ordering was the home city for the salesman. There is a good reason for this; a
circle does not start or end at any particular point! As long as we have some
permutation, we can interpret the cycle as starting at the home city. For
example, for the first tour proposed above, we could equally well have set
$\pi$ so that $\pi(1)=6$, $\pi(2)=7$, $\pi(3)=2$, $\pi(4)=1$, $\pi(5)=3$,
$\pi(6)=4$, and $\pi(7)=5$. (Make sure that you understand why this does
specify the same tour as the one given above.) Given any permutation $\pi$, we
can convert it into an equivalent one in which the first city is the home city
by starting with the home city and tracing cyclically around the tour $\pi$.

Now, how do we give a mathematical description of the objective function?  In
our example, we simply added $C[\pi(1), \pi (2)]$ and $C[\pi(2),\pi(3)]$ and so
forth through $C[\pi(6),\pi(7)]$ and then added the last part (returning home)
$C[\pi(7),\pi(1)]$.  We need a mathematical shorthand to replace "and so
forth".  This is done with a summation sign as follows:

$$\sum_{i=1}^6 C[\pi(i),\pi(i+1)]  + C[\pi(7),\pi(1)]$$

and so in general, the objective
function is

$$\sum_{i=1}^{n-1} C[\pi(i),\pi(i+1)] + C[\pi(n),\pi(1)].$$

In summary, the traveling salesman problem can now be described as the
following mathematically precise computational task.

```{admonition} Traveling Salesman Problem
**input:**
- an integer $n$ specifying the number of cities, and
- an array $C[i,j]$, for $i=1,2,\ldots,n$, $j=1,2,\ldots,n$ (not necessarily symmetric)

**output:**
- a permutation $\pi$ of $1,2,\ldots,n$

**goal:**
minimize the length of the tour, i.e., minimize

$$\sum_{i=1}^{n-1} C[\pi(i),\pi(i+1)] + C[\pi(n),\pi(1)]$$
```

Notice that in our way of describing things, the word problem does not refer to
one specific input, but rather to a general computational task that, for any
input of a certain type, seeks the desired output.
