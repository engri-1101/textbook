# Branch & Bound and Knapsack Lab

**Objectives**
- Preform the branch and bound algorithm
- Apply branch and bound to the knapsack problem
- Understand the geometry of the branch and bound algorithm

**Brief description:** In this lab, we will try solving an example of a knapsack problem with the branch-and-bound algorithm. We will also see how adding a cutting plane helps in reducing the computation time and effort of the algorithm. Lastly, we will explore the geometry of the branch and bound algorithm.


```python
# imports -- don't forget to run this cell
import pandas as pd
import gilp
from gilp.visualize import feasible_integer_pts
from ortools.linear_solver import pywraplp as OR
```


    ---------------------------------------------------------------------------

    ModuleNotFoundError                       Traceback (most recent call last)

    <ipython-input-35-ecb1bde66296> in <module>
          1 # imports -- don't forget to run this cell
          2 import pandas as pd
    ----> 3 import gilp
          4 from gilp.visualize import feasible_integer_pts
          5 from ortools.linear_solver import pywraplp as OR


    ModuleNotFoundError: No module named 'gilp'


## Part 1: Branch and Bound Algorithm

Recall that the branch and bound algorithm (in addition to the simplex method) allows us to solve integer programs. Before applying the branch and bound algorithm to the knapsack problem, we will begin by reviewing some core ideas. Furthermore, we will identify a helpful property that will make branch and bound terminate quicker later in the lab!

**Q1:** What are the different ways a node can be fathomed during the branch and bound algorithm? Describe each.

**A:**  A node can be fathomed in an itteration of the branch and bound algorith by either rounding up or rounding down. 

**Q2:** Suppose you have a maximization integer program and you solve its linear program relaxation. What does the LP-relaxation optimal value tell you about the IP optimal value? What if it is a minimization problem?

**A:** If it is a minimumization program the LP relaxation puts a lowwer bound on the optimal solution, and if it is a maximazation problem, the LP optimal solution places an upper bound on the IP optimal solution. 

**Q3:** Assume you have a maximization integer program with all integral coefficents in the objective function. Now, suppose you are running the branch and bound algorithm and come across a node with an optimal value of 44.5. The current incumbent is 44. Can you fathom this node? Why or why not?

**A:** you can fathom this node by rounding up.

**Q4:** If the optimal solution to the LP relaxation of the original program is integer, then you have found an optimal solution to your integer program. Explain why this is true.

**A:** The optimal solution to the LP relaxation puts an ipper or lower bound on the IP optimal solution, so if the LP relaxation is integer, it is the best the IP can possibly be, as the IP cannot be better than the LP. 

**Q5:** If the LP is infeasible, then the IP is infeasible. Explain why this is true.

**A:** The LP is the same as the IP but with a restriction removed, so if no solution to the LP exists, no solution to the IP exists, as the LP is easier to solve. 

The next questions ask about the following branch and bound tree. If the solution was not integral, the fractional $x_i$ that was used to branch is given. If the solution was integral, it is denoted *INT*. In the current iteration of branch and bound, you are looking at the node with the *****.

<img src="part1_bnb_tree.png" width="500"/>

**Q6:** Can you determine if the integer program this branch and bound tree is for is a minimization or maximixation problem? If so, which is it?

**A:** This is a maximization problem

Hint: For **Q7-8**, you can assume integral coefficents in the objective function.

**Q7:** Is the current node (marked $z^*$) fathomed? Why or why not? If not, what additional constraints should be imposed for each of the next two nodes?

**A:** This node is fathomed, it should have two other nodes, one with a constraint that z=<16 and one with z>=17. 

**Q8:** Consider the nodes under the current node (where $z = 16.3$). What do you know about the optimal value of these nodes? Why? 

**A:** The optimal value of these nodes will be the optimal value of the associated nodes is integer because each of those nodes will fathom until there is an integer solution. 

## Part 2: The Knapsack Problem

In this lab, you will solve an integer program by branch and bound. The integer program to be solved will be a knapsack problem.

**Knapsack Problem:** We are given a collection of $n$ items, where each item $i = 1,\dots,n$ has a weight $w_i$ and a value $v_i$. In addition, there is a given capacity $W$, and the aim is to select a maximum value subset of items that has a total weight at most $W$. Note that each item can be brought at most once.

$$\begin{align*}
\max \quad & \sum_{i=1}^n v_ix_i\\
\text{s.t.} \quad & \sum_{i=1}^n w_ix_i \leq W \\
& 0 \leq x_i \leq 1, \text{integer}, i = 1,\dots,n
\end{align*}$$

Consider the following data which we import from a CSV file:


```python
data = pd.read_csv('knapsack_data_1.csv', index_col=0)
data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>value</th>
      <th>weight</th>
    </tr>
    <tr>
      <th>item</th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>50</td>
      <td>10</td>
    </tr>
    <tr>
      <th>2</th>
      <td>30</td>
      <td>12</td>
    </tr>
    <tr>
      <th>3</th>
      <td>24</td>
      <td>10</td>
    </tr>
    <tr>
      <th>4</th>
      <td>14</td>
      <td>7</td>
    </tr>
    <tr>
      <th>5</th>
      <td>12</td>
      <td>6</td>
    </tr>
    <tr>
      <th>6</th>
      <td>10</td>
      <td>7</td>
    </tr>
    <tr>
      <th>7</th>
      <td>40</td>
      <td>30</td>
    </tr>
  </tbody>
</table>
</div>



and $W = 18$. 

**Q9:** Are there any items we can remove from our input to simplify this problem? Why? If so, replace `index` with the item number that can be removed in the code below. Hint: how many of each item could we possibly take?

**A:** we can remove item 7, because we cannot fit it in out Knapsack. 


```python
# TODO: replace index
data = data.drop(7)
```

**Q10:** If we remove item 7 from the knapsack, it does not change the optimal solution to the integer program. Explain why.

**A:** If we remove item 7, it does not change the optimal solution, because we could not fit it in our napsack anyways

**Q11:** Consider removing items $i$ such that $w_i > W$ from a knapsack input. How does the LP relaxation's optimal value change?

**A:** Removing any items with wi > W does not change the optimal value because we could not fit these items anyways. 

In **Q10-11**, you should have found that removing these items removes feasible solutions from the linear program  but does not change the integer program. This is desirable as the gap between the optimal IP and LP values can become smaller. By adding this step, branch and bound may terminate sooner. 

Recall that a branch and bound node can be fathomed if its bound is no better than the value of the best feasible integer solution found thus far. Hence, it helps to have a good feasible integer solution as quickly as possible (so that we stop needless work). To do this, we can first try to construct a good feasible integer solution by a reasonable heuristic algorithm before starting to run the branch and bound procedure.

In designing a heuristic for the knapsack problem, it is helpful to think about the value per unit weight for each item. We compute this value in the table below.


```python
data['value per unit weight'] = (data['value'] / data['weight']).round(2)
data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>value</th>
      <th>weight</th>
      <th>value per unit weight</th>
    </tr>
    <tr>
      <th>item</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>50</td>
      <td>10</td>
      <td>5.00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>30</td>
      <td>12</td>
      <td>2.50</td>
    </tr>
    <tr>
      <th>3</th>
      <td>24</td>
      <td>10</td>
      <td>2.40</td>
    </tr>
    <tr>
      <th>4</th>
      <td>14</td>
      <td>7</td>
      <td>2.00</td>
    </tr>
    <tr>
      <th>5</th>
      <td>12</td>
      <td>6</td>
      <td>2.00</td>
    </tr>
    <tr>
      <th>6</th>
      <td>10</td>
      <td>7</td>
      <td>1.43</td>
    </tr>
  </tbody>
</table>
</div>



**Q12:** Design a reasonable heuristic for the knapsack problem. Note a heuristic aims to find a decent solution to the problem (but is not necessarily optimal).

**A:** Put the biggest value per weight item that fits in the bag into the bag until no more items fit. 

**Q13:** Run your heuristic on the data above to compute a good feasible integer solution. Your heuristic should generate a feasible solution with a value of 64 or better. If it does not, try a different heuristic (or talk to your TA!)

**A:** Item 1, Item 4. Total Value = 64

We will now use the branch and bound algorithm to solve this knapsack problem! First, let us define a mathematical model for the linear relaxation of the knapsack problem.

**Q14:** Complete the model below.


```python
def Knapsack(table, capacity, integer = False):
    """Model for solving the Knapsack problem.
    
    Args:
        table (pd.DataFrame): A table indexd by items with a column for value and weight
        capcity (int): An integer-capacity for the knapsack
        integer (bool): True if the variables should be integer. False otherwise.
    """
    ITEMS = list(table.index)        # set of items
    v = table.to_dict()['value']     # value for each item 
    w = table.to_dict()['weight']    # weight for each item
    W = capacity                     # capacity of the knapsack
    
    # define model
    m = OR.Solver('knapsack', OR.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
    
    # decision variables
    x = {}    
    for i in ITEMS:
        if integer:
            x[i] = m.IntVar(0, 1, 'x_%d' % (i)) 
        else:
            x[i] = m.NumVar(0, 1, 'x_%d' % (i)) 
        
    # define objective function here
    m.Maximize(sum(v[i]*x[i] for i in ITEMS))
    
    # TODO: Add a constraint that enforces that weight must not exceed capacity
    # recall that we add constraints to the model using m.Add()
    m.Add(x[1]* w[1] +x[2]* w[2] +x[3]* w[3] +x[4] * w[4] +x[5] *w[5] + x[6] *w[6] <= W)
    return (m, x)  # return the model and the decision variables
```


```python
# You do not need to do anything with this cell but make sure you run it!
def solve(m):
    """Used to solve a model m."""
    m.Solve()
    
    print('Objective =', m.Objective().Value())
    print('iterations :', m.iterations())
    print('branch-and-bound nodes :',m.nodes())
    
    return ({var.name() : var.solution_value() for var in m.variables()})
```

We can now create a linear relaxation of our knapsack problem. Now, `m` represents our model and `x` represents our decision variables.


```python
m, x = Knapsack(data, 18)
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-30-3e731093df0d> in <module>
    ----> 1 m, x = Knapsack(data, 18)
    

    <ipython-input-26-5f45f60b5fa3> in Knapsack(table, capacity, integer)
         13 
         14     # define model
    ---> 15     m = OR.Solver('knapsack', OR.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
         16 
         17     # decision variables


    NameError: name 'OR' is not defined


We can use the next line to solve the model and output the solution


```python
solve(m)
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-13-19c524d9502f> in <module>
    ----> 1 solve(m)
    

    NameError: name 'm' is not defined


**Q15:** How does this optimal value compare to the value you found using the heuristic integer solution?

**A:** This optimal solution is higher than my heuristic solution

**Q16:** Should this node be fathomed? If not, what variable should be branched on and what additional constraints should be imposed for each of the next two nodes?


**A:** This node should not be fathomed because it is already integer

After constructing the linear relaxation model using `Knapsack(data1, 18)` we can add additional constraints. For example, we can add the constraint $x_2 \leq 0$ and solve it as follows:


```python
m, x = Knapsack(data, 18)
m.Add(x[2] <= 0)
solve(m)
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-31-041df17acbb8> in <module>
    ----> 1 m, x = Knapsack(data, 18)
          2 m.Add(x[2] <= 0)
          3 solve(m)


    <ipython-input-26-5f45f60b5fa3> in Knapsack(table, capacity, integer)
         13 
         14     # define model
    ---> 15     m = OR.Solver('knapsack', OR.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
         16 
         17     # decision variables


    NameError: name 'OR' is not defined


 **NOTE:** The line `m, x = Knapsack(data1, 18)` resets the model `m` to the LP relaxation. All constraints from branching have to be added each time.

**Q17:** Use the following cell to compute the optimal value for the other node you found in **Q16**.


```python
m, x = Knapscack(data1,18)
```

**Q18:** What was the optimal value? Can this node be fathomed? Why? (Hint: In **Q13**, you found a feasible integer solution with value 64.)

**A:** The optimal value is 65

If we continue running the branch and bound algorithm, we will eventually reach the branch and bound tree below where the $z^*$ indictes the current node we are looking at.

<img src="part2_bnb_tree.png" width="700"/>

**Q19:** The node with $z = 64.857$ was fathomed. Why are we allowed to fathom this node? (Hint: think back to **Q3**)

**A:** Because we round up the previous value

**Q20:** Finish running branch and bound to find the optimal integer solution. Use a separate cell for each node you solve and indicate if the node was fathomed with a comment. (Hint: Don't forget to include the constraints further up in the branch and bound tree.)


```python
# Template
m, x = Knapsack(data, 18)
m.Add(x[1]<=0)
m.Add(x[4]>=1)
m.Add(x[3]<=0)
m.Add(x[2]<=0)

solve(m)
# fathomed?
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-33-667bdbfe4582> in <module>
          1 # Template
    ----> 2 m, x = Knapsack(data, 18)
          3 m.Add(x[1]<=0)
          4 m.Add(x[4]>=1)
          5 m.Add(x[3]<=0)


    <ipython-input-26-5f45f60b5fa3> in Knapsack(table, capacity, integer)
         13 
         14     # define model
    ---> 15     m = OR.Solver('knapsack', OR.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
         16 
         17     # decision variables


    NameError: name 'OR' is not defined



```python

```


```python

```

**A:** 

**Q21:** How many nodes did you have to explore while running the branch and bound algorithm?

**A:** 9

In the next section, we will think about additional constraints we can add to make running branch and bound quicker.

## Part 3: Cutting Planes

In general, a cutting plane is an additional constraint we can add to an integer program's linear relaxation that removes feasible linear solutions but does not remove any integer feasible solutions. This is very useful when  solving integer programs! Recall many of the problems we have learned in class have something we call the "integrality property". This is useful because it allows us to ignore the integrality constraint since we are garunteed to reach an integral solution. By cleverly adding cutting planes, we strive to remove feasible linear solutions (without removing any integer feasible solutions) such that the optimal solution to the linear relaxation is integral!

Conisder an integer program whose linear program releaxation is 

$$\begin{align*}
\max \quad & 2x_1+x_2\\
\text{s.t.} \quad & x_1 + x_2 \leq 3 \\
& 2x_1 \leq 5 \\
& -x_1 + 2x_2 \leq 2 \\
& x_1, x_2 \geq 0
\end{align*}$$

We can define this linear program and then visualize its feasible region. The integer points have been highlighted.


```python
lp = gilp.LP([[1,1],[2,0],[-1,2]],
             [3,5,2],
             [2,1])
fig = gilp.lp_visual(lp)
fig.set_axis_limits([3.5,2])
fig.add_trace(feasible_integer_pts(lp, fig))
fig
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-34-4ed4dd53b730> in <module>
    ----> 1 lp = gilp.LP([[1,1],[2,0],[-1,2]],
          2              [3,5,2],
          3              [2,1])
          4 fig = gilp.lp_visual(lp)
          5 fig.set_axis_limits([3.5,2])


    NameError: name 'gilp' is not defined


**Q22:** List every feasible solution to the integer program.

**A:** (x1 = 2, x2 =1), (x1 = 2, x2 = 0), (x1 = 1, x2 = 0)

**Q23:** Is the constraint $x_2 \leq 1$ a cutting plane? Why? (Hint: Would any feasible integer points become infeasible? What about feasible linear points?)

**A:** Yes, because it eliminates non-integer solutions without eliminating any integer solutions. 

Let's add this cutting plane to the LP relaxation!


```python
lp = gilp.LP([[1,1],[2,0],[-1,2],[0,1]],
             [3,5,2,1],
             [2,1])
fig = gilp.lp_visual(lp)
fig.set_axis_limits([3.5,2])
fig.add_trace(feasible_integer_pts(lp, fig))
fig
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-36-a7a33266d6aa> in <module>
    ----> 1 lp = gilp.LP([[1,1],[2,0],[-1,2],[0,1]],
          2              [3,5,2,1],
          3              [2,1])
          4 fig = gilp.lp_visual(lp)
          5 fig.set_axis_limits([3.5,2])


    NameError: name 'gilp' is not defined


**Q24:** Is the constraint $x_1 \leq 3$ a cutting plane? Why?

**A:** No, becasue it does not remove any feasable solutions

**Q25:** Can you provide another cutting plane? If so, what is it?

**A:** x1 <= 2

Let's look at the feasible region after adding the cutting plane from **Q23** and one of the possible answers from **Q25**. Notice the optimal solution to the LP relaxation is now integral!


```python
lp = gilp.LP([[1,1],[2,0],[-1,2],[0,1],[1,0]],
             [3,5,2,1,2],
             [2,1])
fig = gilp.lp_visual(lp)
fig.set_axis_limits([3.5,2])
fig.add_trace(feasible_integer_pts(lp, fig))
fig
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-37-b8c943fd579a> in <module>
    ----> 1 lp = gilp.LP([[1,1],[2,0],[-1,2],[0,1],[1,0]],
          2              [3,5,2,1,2],
          3              [2,1])
          4 fig = gilp.lp_visual(lp)
          5 fig.set_axis_limits([3.5,2])


    NameError: name 'gilp' is not defined


Let's try applying what we know about cutting planes to the knapsack problem! Again, recall our input was $W = 18$ and:


```python
data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>value</th>
      <th>weight</th>
      <th>value per unit weight</th>
    </tr>
    <tr>
      <th>item</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>50</td>
      <td>10</td>
      <td>5.00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>30</td>
      <td>12</td>
      <td>2.50</td>
    </tr>
    <tr>
      <th>3</th>
      <td>24</td>
      <td>10</td>
      <td>2.40</td>
    </tr>
    <tr>
      <th>4</th>
      <td>14</td>
      <td>7</td>
      <td>2.00</td>
    </tr>
    <tr>
      <th>5</th>
      <td>12</td>
      <td>6</td>
      <td>2.00</td>
    </tr>
    <tr>
      <th>6</th>
      <td>10</td>
      <td>7</td>
      <td>1.43</td>
    </tr>
  </tbody>
</table>
</div>



**Q26:** Look at items 1, 2, and 3. How many of these items can we take simultaneously? Can you write a new constraint to capture this? If so, please provide it.

**A:** only one of these items can be taken simeltaneously
x1 + x2 + x3 <= 1

**Q27:** Is the constraint you found in **Q26** a cutting plane? If so, provide a feasible solution to the linear program relaxation that is no longer feasible (i.e. a point the constraint *cuts off*).

**A:** This constarint is a cutting plane, as it cuts off feasable non-integer solutions without eliminating any integer solutions.

**Q28:** Provide another cutting plane involving items 4,5 and 6 for this integer program. Explain how you derived it.

**A:** x4 + x5 + x6 <= 2
We can have 2 of these items at a time. 

**Q29:** Add the cutting planes from **Q26** and **Q28** to the model and solve it. You should get a solution in which we take items 1 and 4 and $\frac{1}{6}$ of item 5 with an objective value of 66.


```python
m, x = Knapsack(data, 18)
m.Add(x[1]+x[2]+x[3] <=1)
m.Add(x[4]+x[5]+x[6]<=2)

solve(m)
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-39-e622e90acce4> in <module>
    ----> 1 m, x = Knapsack(data, 18)
          2 m.Add(x[1]+x[2]+x[3] <=1)
          3 m.Add(x[4]+x[5]+x[6]<=2)
          4 
          5 solve(m)


    <ipython-input-26-5f45f60b5fa3> in Knapsack(table, capacity, integer)
         13 
         14     # define model
    ---> 15     m = OR.Solver('knapsack', OR.Solver.CBC_MIXED_INTEGER_PROGRAMMING)
         16 
         17     # decision variables


    NameError: name 'OR' is not defined


Let's take a moment to pause and reflect on what we are doing. Recall from **Q9-11** that we dropped item 7 becuase its weight was greater than the capcity of the knapsack. Essentially we added the constraint $x_7 \leq 0$. This constraint was a cutting plane! It eliminated some linear feasible solutions but no integer ones. By adding these two new cutting planes, we can get branch and bound to terminate earlier yet again! So far, we have generated cutting planes by inspection. However, there are more algorithmic ways to identify them (which we will ignore for now).

If we continue running the branch and bound algorithm, we will eventually reach the branch and bound tree below where the $z^*$ indictes the current node we are looking at. 

<img src="part3_bnb_tree.png" width="700"/>

**NOTE:** Do not forget about the feasible integer solution our heuristic gave us with value 64.

**Q30** Finish running branch and bound to find the optimal integer solution. Use a separate cell for each node you solve and indicate if the node was fathomed with a comment. Hint: Don't forget the cutting plane constraints should be included in every node of the branch and bound tree.


```python
# Template
m, x = Knapsack(data, 18)
m.Add(x[1]+x[2]+x[3] <=1)
m.Add(x[4]+x[5]+x[6]<=2)
m.Add(x[5] >=1)

solve(m)
# fathomed?
```


```python

```


```python

```

**A:** 

**Q31:** Did you find the same optimal solution? How many nodes did you explore? How did this compare to the number you explored previously?

**A:** I did find the same optimal solution, but without exporing as many nodes. This time, I only had to explore 3 nodes, as opposed to 5 from last time. 

## Part 4: Geometry of Branch and Bound

Previously, we used the `gilp` package to viusualize the simplex algorithm but it also has the functionality to visualize branch and bound. We will give a quick overview of the tool. Similar to `lp_visual` and `simplex_visual`, the function `bnb_visual` takes an `LP` and returns a visualization. It is assumed that every decision variable is constrained to be integer. Unlike previous visualizations, `bnb_visual` returns a series of figures for each node of the branch and bound tree. Let's look at a small 2D example:

$$\begin{align*}
\max \quad & 5x_1+ 8x_2\\
\text{s.t.} \quad & x_1 + x_2 \leq 6 \\
& 5x_1 + 9x_2 \leq 45 \\
& x_1, x_2 \geq 0, \quad \text{integral}
\end{align*}$$


```python
nodes = gilp.bnb_visual(gilp.examples.STANDARD_2D_IP)
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-40-c5d79fee6538> in <module>
    ----> 1 nodes = gilp.bnb_visual(gilp.examples.STANDARD_2D_IP)
    

    NameError: name 'gilp' is not defined



```python
nodes[0].show()
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-41-56b8760f18ba> in <module>
    ----> 1 nodes[0].show()
    

    NameError: name 'nodes' is not defined


Run the cells above to generate a figure for each node and view the first node. At first, you will see the LP relaxation on the left and the root of the branch and bound tree on the right. The simplex path and isoprofit slider are also present.

**Q32:** Recall the root of a branch and bound tree is the unaltered LP relaxation. What is the optimal solution? (Hint: Use the objective slider and hover over extreme points).

**A:** The optimal solution to the LP relaxation is the optimal solution to the unaltered problem. 

**Q33:** Assume that we always choose the variable with the minimum index to branch on if there are multiple options. Write down (in full) each of the LPs we get after branching off the root node.

**A:** x1 <= 5
x2 <=5



**Q34:** Draw the feasible region to each of the LPs from **Q33** on the same picture.

**A:** 

Run the following cell to see if the picture you drew in **Q34** was correct.


```python
nodes[1].show()
```

The outline of the original LP relaxation is still shown on the left. Now that we have eliminated some of the fractional feasible solutions, we now have 2 feasible regions to consider. The darker one is the feasible region associated with the current node which is also shaded darker in the branch and bound tree. The unexplored nodes in the branch and bound tree are not shaded in.

**Q35:** Which feasible solutions to the LP relaxation are removed by this branch?

**A:** All solutions with x1 > 5 are eliminated by this branch

**Q36:** At the current (dark) node, what constraints will we add? How many feasible regions will the original LP relaxation be broken into?

**A:** we add a constraint x1 <=5 


```python
nodes[2].show()
```

**Q37:** What is the optimal solution at the current (dark) node? Do we have to further explore this branch? Explain.

**A:** The optimal solution at this branch is 40. We do not contunue any further as this solution is already optimal. We know this because all of the decision variables are integer. 

**Q38:** Recall shaded nodes have been explored and the node shaded darker (and feasible region shaded darker) correspond to the current node and its feasible region. Nodes not shaded have not been explored. How many nodes have not yet been explored?

**A:** 5 nodes have yet to be explored. 

**Q39:** How many nodes have a degree of one in the branch and bound tree? (That is, they are only connected to one edge). These nodes are called leaf nodes. What is the relationship between the leaf nodes and the remaining feasible region?

**A:** 6 nodes are leaves. These are the nodes that put the most constraint on the feasbable region. 


```python
# Show the next two iterations of the branch and bound algorithm
nodes[3].show()
nodes[4].show()
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-42-a1e4d1e8884d> in <module>
          1 # Show the next two iterations of the branch and bound algorithm
    ----> 2 nodes[3].show()
          3 nodes[4].show()


    NameError: name 'nodes' is not defined


**Q40:** At the current (dark) node, we added the constraint $x_1 \leq 1$. Why were the fractional solutions $1 < x_1 < 2$ not eliminated for $x_2 <= 3$?
 
**A:** Because an x2 value less than or equal to 3 allows room for the x1 varaible to be between 1 and 2, which is not constrained enough to always be integer. 


```python
# Show the next three iterations of the branch and bound algorithm
nodes[5].show()
nodes[6].show()
nodes[7].show()
```

**Q41:** What constraints are enforced at the current (dark) node? Why are there no feasible solutions at this node?

**A:**  x1>=6 and x2>=6 are the constraints enforced at this node, which leaves for no feasable solutions as the other constraints are violated. 


```python
nodes[8].show()
```

**Q42:** Are we done? If so, what nodes are fathomed and what is the optimal solution? Explain.

**A:** We are done, all nodes that need to be fathomed have been, and the optimal solution is x1 =0, x2 =5 which produces an objective value of 40

Let's look at branch and bound visualization for an integer program with 3 decision variables!


```python
nodes = gilp.bnb_visual(gilp.examples.VARIED_BRANCHING_3D_IP)
```


```python
# Look at the first 3 iterations
nodes[0].show()
nodes[1].show()
nodes[2].show()
```

Let's fast-forward to the final iteration of the branch and bound algorithm.


```python
nodes[-1].show()
```

**Q43:** Consider the feasible region that looks like a rectangular box with one corner point at the origin. What node does it correspond to in the tree? What is the optimal solution at that node?

**A:** This corresponds to node 3, which has an optimal solution of 36

**Q44:** How many branch and bound nodes did we explore? What was the optimal solution? How many branch and bound nodes would we have explored if we knew the value of the optimal solution before starting branch and bound?

**A:** In total, we explored 5 nodes, and we found an optimal soltion of 40. If we already knew the optimal solution, we would have only had to explore 3 nodes to find the optimal solution. 

## Bonus: Branch and Bound for Knapsack

Consider the following example:

| item | value | weight
|------|-------|-------
|  1   |   2   |   1 
|  2   |   9   |   3 
|  3   |   6   |   2 

The linear program formulation will be:


$$\begin{align*}
\max \quad & 2x_1+9x_2+6x_3\\
\text{s.t.} \quad & 1x_1+3x_2+2x_3 \leq 10 \\
& x_1, x_2, x_3 \geq 0, \quad \text{integer}
\end{align*}$$

In gilp, we can define this lp as follows:


```python
lp = gilp.LP([[1,3,2]],
             [10],
             [2,9,6])

for fig in gilp.bnb_visual(lp):
    fig.show()
```
