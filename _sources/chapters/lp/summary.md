# Summary of Simplex Method

We described above, by example, a method for solving LPs, known as the *Simplex
Method*. It can be summarized as follows.

```{admonition} Simplex Method

**Initialization:** Set up the first dictionary: replace the inequality
constraints by equality constraints by introducing new nonnegative variables.
The first dictionary has the new variables on the left hand side, and the other
variables on the right hand side.

**Loop:** Then repeat the following:
- identify a variable that has positive coefficient in objective function
- determine how much this variable can increase, and the most restrictive
  constraint
- rearrange dictionary, by solving for the increasing variable in the most
  restrictive constraint, and substituting this in the other equalities and the
  objective.  ```
