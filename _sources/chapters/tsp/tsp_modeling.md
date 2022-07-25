# Modeling with the Traveling Salesman Problem

The traveling salesman problem is an important computational model for a
variety of reasons. While the particular application of routing our poor
salesman is valid enough, this does not really constitute a real-world
application. However, it forms a  central component of more complicated models,
such as routing a fleet of vehicles for pickups and deliveries, or more
concretely, the sort of problem that a UPS depot might solve on a daily basis.
It can also be used to model a number of problems that, at first glance, do not
seem to be related.

Of course, we have already encountered one such example, the problem of
determining the order in which the radio telescope observes the set of stars
being studied. In that case, we can model our problem as a traveling salesman
problem. The set of stars to be studied corresponds to the set of cities to be
visited. The re-positioning times Focus-time[$i$,$j$] correspond directly to
the costs $C[i,j]$; a feasible solution is again any permutation $\pi$ of the
stars, and the objective is to minimize the total re-positioning time for the
telescope:

$$\sum_{i=1}^{n-1} \mbox{Focus-time}[\pi(i),\pi(i+1)] + \mbox{Focus-time}[\pi(n),\pi(1)]$$

It is important to note that this exactly captures what is needed in a 24-hour
cycle of stellar observations. Hence, we could take our data for re-positioning
the telescope, and apply a standard software package for the traveling salesman
problem (such as Concorde, which is the state of the art in this case), and be
able to interpret the optimal solution for the corresponding traveling salesman
input as an (optimal) solution to our telescope problem.

However, while modeling our telescope problem as a traveling salesman problem
seems to make sense, and might work on some data sets, it also can fail
miserably. Why?

There are, both minor and major reasons why this model does not perfectly
represent our computational problem. For minor reasons, one notable issue is
that our model of the problem views the telescope positioning problem as a
cyclical 24-hour problem. Recall that we had one week of access to the
telescope to make observations. So viewing the problem as a cyclical 24-hour
problem is nearly correct, if one focuses on the "middle" part of the week;
however, we still need to start the week (taking over from how it was used the
previous week for another astronomer, and then handing off to yet another
person for the following week). However, this is a minor discrepancy and would
have only a small effect on the selection of a regular daily pattern.

There is a more fundamental issue. That concerns the statement above: a
feasible solution is again any permutation $\pi$ of the stars.  That is not
true for our problem. The telescope cannot be positioned to observe a
particular star next if it is no longer above the horizon. Thus, to carefully
and correctly model the telescope problem, we actually need a more complicated
model that takes into account not just "travel times" and "waiting times"
(while the telescope is observing a given star), it must also have so-called
time-windows for each star, as part of the input, that indicate the period of
time (within each 24-hour cycle) that it is observable by our telescope.

Even more generally, this suggests a good rule of thumb - when trying to model
a problem in a decision-making setting: start by considering the simplest
model! But before attempting to use that model to make actual decisions, it is
important to test it, to be sure that the "simplifying assumptions" made along
the way are indeed the kind that can be put aside with minimal effect.  Hence,
the overall design process of thinking about a model might be viewed as
follows:

```{attention} Figure 2: The cyclical process of formulating and analyzing an
OR model should be here.
```
