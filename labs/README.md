# Labs

## Distribution Files

The git repository only maintains a lab key file from which the student
version and distribution zip file can be generated. To make the distribution
files for every lab, run the following command. Be aware this takes a moment.

```
make all
```

To make the distribution files for a single lab, navigate to that lab's
directory and run `make`. Some labs may have targets in addition to `lab`
such as `demo`. For example, if you want to make the distribution file for the
shortest path lab demo, you would run

```
cd labs/shortest_path
make demo
```

If you are not familiar with the Make system, feel free to reach out to Henry
(hwr26@cornell.edu) with any questions.

## Lab Directory Structure

Every lab has a corresponding directory. These lab directories contain some
subset of the following:
- Relevant notebooks for generating data used in the labs
- Notes from Fall 2020 semester with common issues / questions regarding the lab
- `<lab_name>_lab_key.ipynb` which is the lab key file
- `data-lab` / `data-demo` for data used in the lab or demo respectively
- `images-lab` / `images-key` / `images-demo` for images used in the lab, answer key, or demo respectively
- `.py` files used by the lab and/or demo

## Development

For those interested in creating a new lab, there are a few tools provided in
the repo to ease this process. First, create a new directory called
`<lab_name>`. All dependencies for this lab:
data, images, python scripts, etc.. should be put in this directory. Build the
key Jupyter Notebook file. This should be named `<lab_name>_lab_key.ipynb`.
There are two types of supported questions: text and code. To generate the
student version correctly, the following format should be used:

TEXT
```
**Q1:** Your question here?

**A:** <font color='blue'> Your answer here.</font>
```

CODE
```
# TODO: Assign a the value 1101
# a = XXX

### BEGIN SOLUTION
a = 1101
### END SOLUTION
```

Create a `Makefile` using one from another lab as a template. The Makefile
states which files / directories should be contained in the distribution file
(reach out to Henry (hwr26@cornell.edu) if you are unfamiliar with the Make
system). The file `<lab_name>_lab.ipynb` is the student version of the lab
which is generated from the key file. It should be included in the distribution
file. Lastly, edit the main [Makefile](Makefile) to include the new lab.

## Current Table of Labs

| Lab # | Name                              | Mode             | Directory                                                  | Author(s) NetID* |
|-------|-----------------------------------|------------------|------------------------------------------------------------|------------------|
| 1     | Travelling Salesman Problem (TSP) | Web-based        | [travelling_salesman_problem](travelling_salesman_problem) | tw454 + hwr26    |
| 2     | Dijkstra's Shortest Path          | Web-based        | [shortest_path](shortest_path)                             | sea78, tw454 + hwr26, ejb284 + kkg35 |
| 3     | Minimum Spanning Tree (MST)       | Web-based        | [minimum_spanning_tree](minimum_spanning_tree)             | tw454 + hwr26    |
| 4     | Maximum Flow                      | Jupyter Notebook | [maximum_flow](maximum_flow)                               | fms9             |
| 5     | Baseball Elimination              | Jupyter Notebook | [baseball_elimination](baseball_elimination)               | qz245 + yz544    |
| 6     | Transportation I+II               | Jupyter Notebook | [transportation](transportation)                           | qz245            |
| 7     | First-Year Writing Seminar        | Jupyter Notebook | [fws](fws)                                                 | qz245 + bwc73     |
| 8     | Simplex                           | Jupyter Notebook | [simplex](simplex)                                         | hwr26            |
| 9     | LP Formulation                    | Jupyter Notebook | [lp_formulation](lp_formulation)                           | hwr26            |
| 10    | TSP and Integer Programming       | Jupyter Notebook | [tsp_integer_programming](tsp_integer_programming)         | hwr26            |
| 11    | Seat Packing                      | Jupyter Notebook | [seat_packing](seat_packing)                               | qz245            |
| 12    | Knapsack                          | Web (Figma)      | [knapsack](knapsack)                                       | qz245            |
| 13    | Branch and Bound                  | Jupyter Notebook | [branch_and_bound](branch_and_bound)                       | hwr26            |
| 14    | Diet                              | Jupyter Notebook | [diet](diet)                                               | hwr26            |
| 15    | Game Theory                       | Jupyter Notebook | [game_theory](game_theory)                                 | sea78 + hwr26 + kkg35 |
| 16    | Minimum-cost Flow                 | Jupyter Notebook | [min-cost_flow](min-cost_flow)                             | aaj54 + hwr26    |
| 17    | Redistricting                     | Jupyter Notebook | [redistricting](redistricting)                             | rwg97 + hwr26    |
| 18    | Minimum Cut                       | Jupyter Notebook | [minimum_cut](minimum_cut)                                 | kz226            |
| 19    | Project Selection                 | Jupyter Notebook | [project_selection](project_selection)                     | wpv6             |

*Authors should be listed in chronological order of their latest contribution. Hence, the right-most person should serve as the first point of contact for questions regarding the lab.