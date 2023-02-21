# Modeling with Shortest Paths

In The Traveling Salesman Problem handout, we saw that the VLSI problem was a special case of the TSP: for any input to the VLSI problem, we could construct a TSP input such that the cheapest TSP tour gave an optimal VLSI problem. 

We will next consider a problem from inventory management.  At first glance, it might not seem  like a shortest path problem.  We will, however, make an analogous argument: for any input to the inventory problem, we can construct an input to the shortest path problem; finding a shortest path in the graph constructed will allow us to find an optimal solution to the original inventory problem.

In this inventory problem, a company plans to sell steel beams.  Beams come in several sizes, and the company wants to choose which beams they should stock. More specifically, steel beams come in $n$ different types.  All beam types have the same cross-sectional area, but different beam types have different heights.  We say that beams are of type $i$, for $i=1, 2, \ldots, n$.  For each beam type $i$, we have the following parameters:
- Beams of type $i$ have height $h(i)>0$.  We assume that the beam types are ordered in increasing height, so that 

$$h(1)<h(2)<\cdots < h(n-1)<h(n).$$
- There is a known demand $d(i)>0$ for beams of height $h(i)$.
- We pay an acquisition cost $c(i)>0$ for each type $i$ beam we stock. Taller beams cost more: 

$$c(1)<c(2)<\cdots <c(n-1)<c(n).$$
- There is a fixed cost $k(i)>0$ if we choose to stock any beams of type $i$. This cost covers all of the setup necessary to sell beams of type $i$ (e.g., configuring warehouse and sales space).

Because the beams all have the same cross-section, we can do two things to supply a beam of height $h(i)$: we can either supply a beam of type $i$, or we can cut down a taller beam of height $h(j)$ to height $h(i)$ (where $j>i$).  When we cut down a larger beam, we throw out any leftover material.

Our goal is to figure out which beams to stock so as to minimize our total cost.  For example, suppose we have only beams of $n=2$ types.  We could stock beams of type 1 and 2, in which case we must pay the fixed costs for both beam types 1 and 2.  We also  pay $c(1)$ for each of the  $d(1)$ type-1 beams we must acquire, and we  pay $c(2)$ for each of the $d(2)$ type-2 beams we must acquire. In total, doing so costs 

$$k(1)+k(2)+c(1) \cdot d(1)+c(2) \cdot d(2).$$   
It might be cheaper to instead only stock beams of type 2 and to cut them down anytime we need to supply a beam of height $h(1)$.  In this case, the only fixed cost we pay is $k(2)$.  However, we now need to acquire $d(1)+d(2)$ type-2 beams to meet the demand for beams of heights $h(1)$ and $h(2)$.  The total cost of this second option is thus 

$$k(2)+c(2)\left(d(1)+d(2)\right).$$  
In this second option, fixed storage cost is reduced, but since $c(1)<c(2)$, the total acquisition cost is greater.  This problem, then, requires finding the optimal way to balance the fixed storage cost with the per-beam acquisition cost.

Moving back to the general problem with $n$ different beam heights, notice that we must always stock the beam of type $n$: these are the only beams that can be used to supply the $d(n)$ necessary beams of height $h(n).$  One way to express a solution to the inventory problem is to first specify the smallest type of beam we choose to stock.  We then specify the next smallest beam type we chose to stock, and continue doing so until we specify beams of type $n$.  
For example, suppose that $n=7$ and we choose to first stock beams of type 2, next stock beams of type 6, and finally stock beams of type 7.  Our total cost would be

$$\left[k(2) + c(2)\left(d(1)+d(2)\right)\right]
+ \left[k(6) + c(6)\left(d(3)+d(4)+d(5)+d(6)\right)\right] +
\left[k(7) + c(7)\left(d(7)\right)\right].$$  

More succinctly, the total cost is:

$$\left[k(2) + c(2)\sum_{i=1}^2 d(i)\right]
+ \left[k(6) + c(6)\sum_{i=3}^6 d(i)\right] +
\left[k(7) + c(7)\sum_{i=7}^7 d(i)\right].$$

Notice that these terms account for our costs in the exact same order as our sequential decisions!  If the first beam we supply is of type 2, then we pay exactly $k(2) + c(2)\sum_{i=1}^2 d(i)$ for stocking type-2 beams (or, in other words, supplying beams of height at most $h(2)$.  If the next-smallest beam we store is of type 6, then we pay exactly $k(6) + c(6)\sum_{i=3}^6 d(i)$ to stock type-6 beams --- that is, to supply beams of heights from $h(3)$ through $h(6).$  We finally pay $k(7) + c(7)\sum_{i=7}^7 d(i)$ to stock height $h(7)$ beams.

We now use this intuition to specify how to take any input to the inventory problem with $n$ beam types, and construct an input to the shortest path problem.  Our shortest path instance will have $n+1$ nodes: nodes $1, 2, \ldots, n$ and an extra node 0.  Node 0 will be our source node.  Arcs will encode sequential inventory decisions. Our shortest path will begin with some arc $(0, i)$, and this arc will represent that beams of type $i$ is the smallest beam type we stock.  If  we traverse an arc $(i, j)$ in the path, then this represents the decision that "we have chosen to stock beams of type $i$, and the next-smallest-beam-type we choose to stock is of type $j$."  In the preceding example, we would encode the decision to "first stock beams of type 2, then of type 6, and then of type 7" as a path $(0, 2), (2, 6), (6, 7).$  The length $\ell(i, j)$ should encode the cost of the decision to "stock beams of type $i$ followed by type $j$."  That is, 

$$\ell(i, j)=k(j)+c(j)\sum_{r=i+1}^j d(r).$$

Our full input to the shortest path problem is:
- A directed graph $G=(N, A)$ where $N=\{0, 1, ..., n\}.$   $A=\{(i, j): 0\leq i<j\leq n\},$ representing any possible decision to "stock beams of type $i$, and then the next-smallest-beam-type we stock is of type $j$."
- Our source is $s=0$ and our destination is $t=n.$
- The length of arc $(i, j)$ is $k(j)+c(j)\sum_{r=i+1}^j d(r)$, for $ 0\leq i<j\leq n.$

Given a shortest path in this instance, we readily attain a solution to the original inventory problem.  We do so by stocking exactly those beams whose corresponding nodes are visited in the shortest path.  For example, if $n=7$ and found the shortest 0-7 path to be $(0, 2), (2, 6), (6, 7),$ we'd exactly have the solution and cost discussed above: stock beams of type 2, 6, and 7!

We have shown that we can model the inventory stocking problem as a shortest path problem. Note that there will several steps along the way in showing that this is a correct formulation. First, we had to explain how to map any input to the inventory problem into an input for the shortest path problem --- that is, how to construct the graph, how to determine the arc lengths, and what source (and destination) node captured the decisions needed to be made. Then, we showed how to interpret any output from the shortest path problem, that is, a path from node 0 to node $n$ as a sequence of decisions. What we actually showed was a precise correspondence --- for each sequence of decisions there was a corresponding path, and vice versa --- each path from node 0 to node $n$ could be interpreted as the decisions about which beam types to store in inventory (and which ones not to store). And finally, we argued that the length of each path was exactly equal to the cost of the corresponding inventory decisions. Consequently, solving the shortest path input that was constructed in this way, precisely solved the inventory management problem.


This completes the explanation that the inventory problem can be modeled by the shortest path problem.  We have established Dijkstra's algorithm to solve shortest path problems.  Hence, we now have a to solve this inventory problem:  convert it to a shortest path problem and solve it using Dijkstra's algorithm.