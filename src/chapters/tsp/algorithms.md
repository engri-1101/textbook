# Solving a Problem -- Algorithms

Let us return to the definition of operations research given in the previous
handout. One aspect that we did not touch upon is that we required that the
mathematical model be *it analyzed* so it can provide guidance in the given
decision-making setting. For an optimization model, the element is thereby an
algorithm, a computation procedure that can solve the task at hand. And just as
we have described a generic computational task, there should also be a generic
procedure that can handle all possible inputs. So, one can think of this as a
sufficiently robust software package that can handle any of the inputs you
might "reasonably" want to solve.

For the traveling salesman problem, there is a quite simple algorithm that is
guaranteed to produce an optimal solution. One might "simply" enumerate all
possible permutations, one after the other, evaluate the cost associated with
each permutation, and then output the permutation with the cheapest cost. This
certainly works correctly for any input.  So are we done? Actually, no. The
problem is that there are too many permutations for this to be of much
practical use.  For $n=100$, how many permutations are there? There are 100
choices for the first city, and for each of those there are 99 choices for the
second, and then 98 for the third and so forth. So it seems like there are 100!
(100 factorial). In fact, that is a bit overdone, because recall that it
doesn't matter which city we start at, so in fact the same tour is counted 100
times. But 99! is big enough. It is more than $10^{155}$, more than the number
of atoms in our universe.

So the simple algorithm is too slow. There are a few options to consider. One
approach, is to develop much more sophisticated algorithms. Throughout this
course, you will learn many of the elements used by the best solver for the
traveling salesman problem, a package called Concorde (which you can install on
your iPhone - you are encouraged to do so). Concorde can easily solve inputs
with 1000's or even 10,000 cities, but even that code has its limits.

Another approach is to design simple algorithms that don't necessarily produce
an optimal solution, but instead produce good solutions. One natural one is
called the *it nearest neighbor rule*: start at one city, and iteratively
choose the next city as the one not yet visited that is currently nearest.
There are a number of simple algorithms such as this one, and you will be
introduced to several during the first lab in the course.
