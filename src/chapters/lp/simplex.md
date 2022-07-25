# Simplex Method

How about finding the optimal solution to the following LP:

$$\begin{align*}
\text{maximize}\ & 14-\tfrac 32 x_4-x_6-\tfrac 12 x_7\\
\text{st}\ & x_4 \leq 4 \\
& x_4-x_6 \leq 2 \\
& -x_4 + x_6 \leq 2 \\
& \tfrac 12 x_4+ \tfrac 12 x_7 \leq 4 \\
& x_4, x_6, x_7 \geq 0.
\end{align*}$$

This is actually easy! (Find it before reading on.)

The coefficients of all variables in the objective function are negative, and
all variables are constrained to be nonnegative. This means that we have an
*upper bound* on the objective value of any feasible solution of $14$. Now
consider the solution $x_4^*=x_6^*=x_7^*=0$. This is a feasible solution (all
constraints are satisfied), and has objective value equal to $14$, matching the
upper bound! This means there is no feasible solution with a better objective
value, which means we found an optimal solution!

The method that we now present transforms LPs (of a certain type) into such an
easy LP, for which we can immediately read off an optimal solution, because the
coefficients of all variables in the objective function will be negative, and
all variables are constrained to be nonnegative. We will just use simple
algebra to rewrite the LP, *while not changing the feasible region or the
objective function*.

The type of LPs that we will tackle here are LPs that are maximization
problems, having only "$\leq$"-constraints with nonnegative constants as
right-hand sides, and nonnegative variables. It may seem that we have narrowed
the type of LP that we are considering drastically, but all of these
restrictions can be dropped. You will learn more about this in your homework,
and when you take ORIE 3300.

## First Steps

Recall the LP we are trying to solve:

$$\begin{align*}
\text{maximize}\ & 2x_1+x_2+x_3\\
\text{such that}\\ & x_1 \leq 4 \\
& x_2 \leq 4 \\
& x_1 + x_2 \leq 6 \\
& -x_1+2x_3 \leq 4 \\
& x_1, x_2, x_3 \geq 0.
\end{align*}$$

The first thing we do is to rewrite each constraint in the form $0 \leq
\cdots$. This may seem silly, but there is a method to the madness that will
soon become apparent.

$$\begin{alignat*}{20}
\text{maximize}\ &&&&&& 2x_1&+&\ x_2&+&x_3\\
\text{such that}\  &&0 &\leq\ & 4\;&-&x_1\\
&&0&\leq& 4\;&&&-&x_2 \\
&&0&\leq& 6\; &-& x_1 &-& x_2  \\
&&0&\leq& 4\;&+&x_1&&&-&2x_3
\end{alignat*}$$

$$x_1,x_2,x_3 \geq 0.$$

Recall that you know how to use algebra to solve systems of equations. So let's
make the LP more resemble a system of equations, by introducing new variables,
that we constrain to be nonnegative just like the other variables.

$$\begin{alignat*}{20}
\text{maximize}\ &&z\ \  &=\ &&& 2x_1&+&\ x_2&+&x_3\\
\text{such that}\  &&x_4 &=\ & 4\;&-&x_1\\
&&x_5&=& 4\;&&&-&x_2 \\
&&x_6&=& 6\; &-& x_1 &-& x_2  \\
&&x_7&=& 4\;&+&x_1&&&-&2x_3 \\
\end{alignat*}$$

$$x_1,x_2,x_3,x_4,x_5, x_6, x_7 \geq 0.$$

Note that we have only changed the appearance of the LP! The feasible region of
the original LP and the LP here in terms of $x_1$, $x_2$ and $x_3$ are exactly
the same. And we have added the variable $z$ so that we can handle the
objective function in a manner exactly analogously to how we handle the
constraints.

We will call this our first *dictionary*, by which we mean the following
specific form of writing the LP using equations.


```{admonition} Definition

We say an LP is in **dictionary form** if all constraints are equality
constraints, and all variables are constrained to be nonnegative. Further, each
variable only appears on the left-hand side *or* the right-hand side of the
constraints (not both), and each constraint has a *unique variable* on the
left-hand side. The objective function is in terms of the variables that appear
on the right-hand side of the constraints only. Finally, all constants on the
right-hand side of the constraints are nonnegative.
```

One nice consequence of this definition is that, similar to the LP where we
immediately saw an optimal solution, we can also read off a *feasible* solution
here: we can set all variables that appear on the right hand sides ($x_1$,
$x_2$ and $x_3$) to $0$, and a feasible solution would then have $x_4 = 4$,
$x_5 = 4$, $x_6=6$ and $x_7=4$. We call the feasible solution that we get from
a dictionary by setting all variables that appear on the right hand sides of
the constraints equal to $0$, *the feasible solution associated with this
dictionary*.

The objective value of the feasible solution associated with the dictionary
above is $0$. Another nice consequence of writing the LP in dictionary form is
that we see that there may be better solutions, because variables $x_1$, $x_2$
and $x_3$ all appear with a *positive* coefficient in the objective function,
and all these variables are equal to $0$ in this solution.

## Rewriting the LP

This motivates us to do the following. We want to find a solution where $x_1$,
$x_2$ or $x_3$ is positive --- let's choose $x_1$. We will find a different
dictionary for the LP, so that $x_1$ will now appear *on the left-hand side* of
one of the constraints.
% --- maintaining the convention that we associate a solution with an LP as
% follows: all variables that appear on the right-hand sides of constraints are
% set to $0$, and all variables that appear on the left-hand side of
% constraints will have the value that we can then read off immediately. We
% have to take care that our LP is actually of a form that allows us to do this
% (i.e., variables should not appear on both sides, and each constraint should
% have a unique variable on the left-hand side), and that this solution is
% actually feasible.

Let's think about increasing $x_1$ as much as possible, while maintaining a
feasible solution. The first constraint ($x_4=4-x_1$) tells us that $x_1$
cannot be increased to more than $4$, because otherwise $x_4$ has to become
negative, and this is not feasible. The second constraint ($x_5=2-x_2$) does
not put any limit on how much $x_1$ can increase, because increasing $x_1$ does
not affect either side of this equality. The third constraint ($x_6=6-x_1-x_2$)
puts a limit of $6$ on the value of $x_1$, before $x_6$ has to become negative.
Finally, the fourth constraint ($x_7=4+x_1-2x_3$) does not put any restrictions
on the increase of $x_1$ --- when $x_1$ increases, $x_7$ will increase as well,
and this is not a problem for feasibility.

We found a limit on how much we can increase $x_1$ (namely $4$), and the
constraint that put this limit on the amount that we can increase $x_1$ (the
first constraint). Note that if we want to increase $x_1$ to $4$, that $x_4$
(the left-hand side of the first constraint) will have to become equal to zero.
Because of our convention about variables on the right- and left-hand side of
the constraints, this means that we could actually move $x_4$ from the
left-hand side to the right-hand side, which is good, because we have to move
$x_1$ from the right-hand side to the left-hand side if it is non-zero!

We rewrite the first equation, by solving for $x_1$, obtaining $x_1 = 4 - x_4$.
Note that this equation is equivalent to $x_4 = 4 - x_1$. By replacing the
first equation with this equation, we have exactly the same feasible region for
the LP that we are trying to solve.

If we just replace the first equation, we no longer have an LP in dictionary
form however, because $x_1$ still appears on the right-hand side of some of the
other equations. This is easily fixed: we can substitute $4-x_4$ for every
occurrence of $x_1$ on the right-hand side of the equations (because we just
found that $x_1 = 4 - x_4$). $x_4$ will be a right-hand side variable, so it is
no problem that it will appear on the right-hand side of other equations as
well. (In general, there may be other right-hand side variables in the
expression for the variable we are increasing, but never left-hand side
variables!)

After that long discussion, we are finally ready to rewrite the LP for the
first time:

$$\begin{alignat*}{20}
\text{maximize}\ &&z \ \ &=\ &&& 2(4-x_4)&+&\ x_2&+&x_3\\
\text{such that}\  &&x_1 &=\ & 4\;&-&x_4\\
&&x_5&=& 4\;&&&-&x_2 \\
&&x_6&=& 6\; &-& (4-x_4) &-& x_2  \\
&&x_7&=& 4\;&+&(4-x_4)&&&-&2x_3
\end{alignat*}$$

$$x_1,x_2,x_3,x_4,x_5, x_6, x_7 \geq 0.$$

Note that we also substituted $4-x_4$ for $x_1$ in the objective function. Simplifying gives:

$$\begin{alignat*}{20}
\text{maximize}\ &&z\ \ &=\ & 8\;&-&2x_4&+&\ x_2&+&x_3\\
\text{such that}\  &&x_1 &=\ & 4\;&-&x_4\\
&&x_5&=& 4\;&&&-&x_2 \\
&&x_6&=& 2\; &+& x_4 &-& x_2  \\
&&x_7&=& 8\;&-&x_4&&&-&2x_3 \\
\end{alignat*}$$

$$x_1,x_2,x_3,x_4,x_5, x_6, x_7 \geq 0.$$

This is our second dictionary. Notice what we accomplished here: first of all,
this LP is equivalent to the LP we started with (we only did some algebraic
manipulations); second of all, it is in a form that we want our LPs to be in
(it is in dictionary form: every variable appears only on the right-hand side
of the equations, or only on the left-hand side of one equation, and we can
associate a feasible solution with this particular form of the LP, by setting
all variables on the right-hand side equal to zero); and finally the objective
value of the solution that we associate with this form is higher than the
objective value of the solution that we had before (we can actually immediately
see the objective value $z$ is $8$ because only right-hand side variables
appear in the objective function). The solution associated with this dictionary
is $ x_2=  x_3=  x_4=0$, and $ x_1=4$, $ x_5=4$, $ x_6=2$, $ x_7=8$.

## Rewriting the LP Again

Can we find a feasible solution with an even higher objective value? Well,
$x_2$ and $x_3$ appear in the objective function with a positive coefficient,
and these variables are currently $0$ in the solution that we associate with
the current dictionary. So let's try and see if we can do the same thing again,
now for $x_2$.

**Limit on increase of $x_2$.** The first constraint does not put a limit on
the increase of $x_2$, the second limits the increase to $4$, before $x_5$
becomes negative, the third limits the increase to $2$, before $x_6$ becomes
negative, and the fourth does not put a limit on the increase of $x_2$. We want
$x_2$ to increase as much as possible, but we cannot increase it by more than
$2$ because of the third constraint.

**Substitute $x_2$** We solve the third equation for $x_2$, and replace the
third equation with the expression we obtain: $x_2=2+x_4-x_6$. We substitute
$2+x_4-x_6$ for every other appearance of $x_2$ in the LP,

$$\begin{alignat*}{20}
\text{maximize}\ &&z\ \ &=\ & 8\;&-&2x_4&+&(2+x_4-x_6)&+&x_3\\
\text{such that}\  &&x_1 &=\ & 4\;&-&x_4\\
&&x_5&=& 4\;&&&-&(2+x_4-x_6) \\
&&x_2&=& 2\; &+& x_4 &-&x_6  \\
&&x_7&=& 8\;&-&x_4&&&-&2x_3
\end{alignat*}$$

$$x_1,x_2,x_3,x_4,x_5, x_6, x_7 \geq 0,$$

and simplify:

$$\begin{alignat*}{20}
\text{maximize}\ &&z\ \ &=\ & 10\;&-\;&x_4&-&\; x_6&+&x_3\\
\text{such that}\  &&x_1 &=\ & 4\;&-&x_4\\
&&x_5&=& 2\;&-&x_4&+&x_6 \\
&&x_2&=& 2\; &+& x_4 &-&x_6  \\
&&x_7&=& 8\;&-&x_4&&&-&2x_3
\end{alignat*}$$

$$x_1,x_2,x_3,x_4,x_5, x_6, x_7 \geq 0,$$

We have found the feasible solution $ x_3=  x_4=  x_6=0$, and $ x_1=4$, $
x_2=2$, $ x_5=2$, $ x_7=8$, with objective value $10$.

## And Again

The variable $x_3$ appears in the objective function with a positive
coefficient, and this variable is currently $0$ in the solution that we
associate with the current dictionary. So let's see if we can further improve
the solution, now by increasing $x_3$.

**Limit on increase of $x_3$.** The first constraint does not put a limit on
the increase of $x_3$, neither does the second or the third. The fourth is the
only constraint that puts a limit on the increase of $x_3$.

**Substitute $x_3$.** We replace the fourth equation with
$x_3=4-\tfrac 12 x_4 - \tfrac 12 x_7$, and substitute
$4-\tfrac 12 x_4 - \tfrac 12 x_7$ for every other appearance of $x_3$ in the LP,

$$\begin{alignat*}{20}
\text{maximize}\ &&z\ \ &=\ & 10\;&-&x_4\;&-&\; x_6&+&(4-\tfrac 12 x_4 - \tfrac 12 x_7)\\
\text{such that}\  &&x_1 &=\ & 4\;&-&x_4\;\\
&&x_5&=& 2\;&-&x_4\;&+&x_6 \\
&&x_2&=& 2\; &+& x_4\;&-&x_6  \\
&&x_3&=&4\;&-&\tfrac 12 x_4&&&&- \tfrac 12 x_7\\
\end{alignat*}$$

$$x_1,x_2,x_3,x_4,x_5, x_6, x_7 \geq 0,$$

and simplify:

$$\begin{alignat*}{20}
\text{maximize}\ &&z\ \ &=\ & 14\;&-&\tfrac 32 x_4&-&\; x_6&-& \tfrac 12 x_7\\
\text{such that}\  &&x_1 &=\ & 4\;&-&x_4\\
&&x_5&=& 2\;&-&x_4&+&x_6 \\
&&x_2&=& 2\; &+& x_4 &-&x_6  \\
&&x_3&=&4\;&-&\tfrac 12 x_4&& &-& \tfrac 12 x_7
\end{alignat*}$$

$$x_1,x_2,x_3,x_4,x_5, x_6, x_7 \geq 0,$$

## Done!

Note that this last LP is exactly in the form that we wanted (many pages ago):
The coefficients of all variables in the objective function are negative, and
all variables are constrained to be nonnegative. This means that we have an
*upper bound* on the objective value of any feasible solution of $14$. We also
have a feasible solution with objective value $14$: $x_4^*=x_6^*=x_7^*=0$ and
$x_1^*=4, x_5^*=2, x_2^*=2, x_3^*=4$. The objective value matches the upper
bound, which means there is no feasible solution with a better objective value,
which means we found an optimal solution!

And let's do it a quick check and plug this solution into the LP we started with:

$$\begin{align*}
\text{maximize}\ & 2x_1+x_2+x_3\\
\text{such that}\\ & x_1 \leq 4 \\
& x_2 \leq 4 \\
& x_1 + x_2 \leq 6 \\
& -x_1+2x_3 \leq 4 \\
& x_1, x_2, x_3 \geq 0.
\end{align*}$$

Note that $x_1^*=4, x_2^*=2, x_3^*=4$ is indeed feasible (all constraints are
satisfied), and indeed has objective value $14$ as expected.
