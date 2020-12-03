ENGRI 1101 Labs
===============

**NOTE:** This git repo was created at the end of Summer 2020 after significant course development. All labs were replaced with a web-based or Jupyter Notebook equivalent. AMPL was replaced by Google's OR-Tools.

This git repo serves as the standard for ENGRI 1101 lab software / files (while [Overleaf](https://www.overleaf.com/project/5ecf1b879f37710001f9f54d) serves as the standard for lab handouts). Some labs have lab / prelab tex files with generated pdfs in their directory. The time stamp indicates the day they were pulled from [Overleaf](https://www.overleaf.com/project/5ecf1b879f37710001f9f54d). The [tex](tex) directory stores some files needed to generate the pdfs.
Any updates or additional labs should be added here. Furthermore, this README contains a comprehensive list of labs as well as all necessary Python packages. They should be updated to reflect any changes made to the labs.

Lastly, the directory [public_html](public_html) contains the source code for the course site ([http://engri1101.orie.cornell.edu/](http://engri1101.orie.cornell.edu/)). It also contains the [raphael](https://github.com/DmitryBaranovskiy/raphael) JavaScript vector library used by the web-based labs. Each web-based lab directory contains a file called web_lab_source.md which contains a link to that lab's source code in [public_html](public_html). The document root of the course site is set to be [public_html](public_html). Hence, any changes within [public_html](public_html) will be reflected on the website in the next pull. For this reason, <ins> *exercise extra precaution when updating the source code of web-based labs!* </ins>

### Current Table of Labs

| Lab # | Name                              | Mode             | Directory                                                  | Author(s) NetID* |
|-------|-----------------------------------|------------------|------------------------------------------------------------|------------------|
| 1     | Travelling Salesman Problem (TSP) | Web-based        | [travelling_salesman_problem](travelling_salesman_problem) | tw454 + hwr26    |
| 2     | Dijkstra's Shortest Path          | Web-based        | [shortest_path](shortest_path)                             | sea78, tw454 + hwr26    |
| 3     | Minimum Spanning Tree (MST)       | Web-based        | [minimum_spanning_tree](minimum_spanning_tree)             | tw454 + hwr26    |
| 4     | Maximum Flow                      | Jupyter Notebook | [maximum_flow](maximum_flow)                               | fms9             |
| 5     | Baseball Elimination              | Jupyter Notebook | [baseball_elimination](baseball_elimination)               | qz245            |
| 6     | Transportation I+II               | Jupyter Notebook | [transportation](transportation)                           | qz245            |
| 6     | First-Year Writing Seminar        | Jupyter Notebook | [first_year_writing_seminar](first_year_writing_seminar)   | qz245            |
| 7     | Simplex                           | Jupyter Notebook | [simplex](simplex)                                         | hwr26            |
| 8     | LP Formulation                    | Jupyter Notebook | [lp_formulation](lp_formulation)                           | hwr26            |
| 9     | TSP and Integer Programming       | Jupyter Notebook | [tsp_integer_programming](tsp_integer_programming)         | hwr26            |
| 9     | Seat Packing                      | Jupyter Notebook | [seat_packing](seat_packing)                               | qz245            |
| 10    | Knapsack                          | Web (Figma)      | [knapsack](knapsack)                                       | qz245            |
| 10    | Branch and Bound                  | Jupyter Notebook | [branch_and_bound](branch_and_bound)                       | hwr26            |
| 11    | Diet                              | Jupyter Notebook | [diet](diet)                                               | hwr26            |
| 12    | Game Theory                       | Jupyter Notebook | [game_theory](game_theory)                                 | sea78            |
| 13    | Minimum-cost Flow                 | Jupyter Notebook | [min-cost_flow](min-cost_flow)                             | aaj54 + hwr26    |

*Authors should be listed in chronological order of their latest contribution. Hence, the right-most person should serve as the first point of contact for questions regarding the lab.

### Fall 2020 Schedule

| Lab # | Name                              | Prelab                                                                                 | Lab |
|-------|-----------------------------------|----------------------------------------------------------------------------------------|-----|
| 1     | Travelling Salesman Problem (TSP) | [tsp_prelab.pdf](travelling_salesman_problem/tsp_prelab_tex_2020-12-3/tsp_prelab.pdf)  | [tsp_lab.pdf](travelling_salesman_problem/tsp_lab_tex_2020-12-3/tsp_lab.pdf) |
| 2     | Shortest Path                     | [shortest_path_prelab.pdf](shortest_path/shortest_path_prelab_tex_2020-12-3/shortest_path_prelab.pdf) |[shortest_path_lab.pdf](shortest_path/shortest_path_lab_tex_2020-12-3/shortest_path_lab.pdf) |
| 3     | Software Installation             |   |    |
| 4     | Minimum Spanning Tree (MST)       | [mst_prelab.pdf](minimum_spanning_tree/mst_prelab_tex_2020-12-3/mst_prelab.pdf) | [mst_lab.pdf](minimum_spanning_tree/mst_lab_tex_2020-12-3/mst_lab.pdf) |
| 5     | Maximum Flow (1-2)                | [max_flow_prelab.pdf](maximum_flow/max_flow_prelab_tex_2020-12-3/max_flow_prelab.pdf) | [max_flow_lab.zip](maximum_flow/max_flow_lab/max_flow_lab.zip) |
| 6     | Maximum Flow (3-4)                | | [max_flow_lab_part3-4.zip](maximum_flow/max_flow_lab_part3-4/max_flow_lab_part3-4.zip) |
| 7     | Baseball Elimination              | [baseball_elimination_prelab.pdf](baseball_elimination/baseball_elimination_prelab_tex_2020-12-3/baseball_elimination_prelab.pdf) | [baseball_elimination_lab.zip](baseball_elimination/baseball_elimination_lab/baseball_elimination_lab.zip) |
| 8     | Transportation I+II               | [transportation_prelab.pdf](transportation/transportation_prelab_tex_2020-12-3/transportation_prelab.pdf) | [transportation_lab.zip](transportation/transportation_lab/transportation_lab.zip) |
| 9     | First-Year Writing Seminar + Simplex (1) | [simplex_prelab.pdf](simplex/simplex_prelab_tex_2020-12-3/simplex_prelab.pdf) | [fws_lab.zip](first_year_writing_seminar/fws_lab/fws_lab.zip) <br/> [simplex_lab.ipynb](simplex/simplex_lab.ipynb) |
| 10    | Simplex (2-4)                     | | [simplex_lab.ipynb](simplex/simplex_lab.ipynb) |
| 11    | LP Formulation & Seat Packing     | [lp_formulation_prelab.pdf](lp_formulation/lp_formulation_prelab_tex_2020-12-3/lp_formulation_prelab.pdf) | [lp_formulation_lab.ipynb](lp_formulation/lp_formulation_lab.ipynb) <br/> [seat_packing_lab.zip](seat_packing/seat_packing_lab/seat_packing_lab.zip) |
| 12    | Branch and Bound & Knapsack       | [bnb_prelab.pdf](branch_and_bound/bnb_prelab_tex_2020-12-3/bnb_prelab.pdf) | [branch_and_bound_lab.zip](branch_and_bound/branch_and_bound_lab/branch_and_bound_lab.zip) |
| 13    | Diet  | | |
| 14    | Game Theory  | | |

### Comprehensive List of Python Packages

| Package                                                      | Description                                                            |
|--------------------------------------------------------------|------------------------------------------------------------------------|
| [gilp](https://github.com/henryrobbins/gilp)                 | Visualize the simplex algorithm and solve linear programs              |
| [ortools](https://github.com/google/or-tools)                | Google's optimization suite                                            |
| [networkx](https://github.com/networkx/networkx)             | Create and manipulate complex networks                                 |
| [matplotlib](https://github.com/matplotlib/matplotlib)       | Publication quality figures in python                                  |
| [pandas](https://github.com/pandas-dev/pandas)               | High-performance, easy-to-use data structures and data analysis tools  |
| [bokeh](https://github.com/bokeh/bokeh)                      | Statistical and novel interactive html plots for python                |
| [shapely](https://github.com/Toblerity/Shapely)              | Maniipulation and analysis of geometric objects in the cartesian plane |
| [scipy](https://github.com/scipy/scipy)                      | Scientific library for python                                          |
| [scikit-image](https://github.com/scikit-image/scikit-image) | Image processing routines for scipy                                    |
| [numpy](https://github.com/numpy/numpy)                      | Array processing for numbers, strings, records, and objects            |



