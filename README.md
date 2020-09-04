ENGRI 1101 Labs
===============

**NOTE:** This git repo was created at the end of Summer 2020 after significant course development. All labs were replaced with a web-based or Jupyter Notebook equivalent. AMPL was replaced by Google's OR-Tools.

This git repo serves as the standard for ENGRI 1101 lab software / files (while [Overleaf](https://www.overleaf.com/project/5ecf1b879f37710001f9f54d) serves as the standard for lab handouts). Any updates or additional labs should be added here. Furthermore, this README contains a comprehensive list of labs as well as all necessary Python packages. They should be updated to reflect any changes made to the labs.

Lastly, the directory [public_html](public_html) contains the source code for the course site ([http://engri1101.orie.cornell.edu/](http://engri1101.orie.cornell.edu/)). It also contains the [raphael](https://github.com/DmitryBaranovskiy/raphael) JavaScript vector library used by the web-based labs. Each web-based lab directory contains a file called web_lab_source.md which contains a link to that lab's source code in [public_html](public_html). The document root of the course site is set to be [public_html](public_html). Hence, any changes within [public_html](public_html) will be reflected on the website in the next pull. For this reason, <ins> *exercise extra precaution when updating the source code of web-based labs!* </ins>

### Current Table of Labs

| Lab # | Name                              | Mode             | Directory                                                  | Author(s) NetID* |
|-------|-----------------------------------|------------------|------------------------------------------------------------|------------------|
| 1     | Travelling Salesman Problem (TSP) | Web-based        | [travelling_salesman_problem](travelling_salesman_problem) | tw454 + hwr26    |
| 2     | Dijkstra's Shortest Path          | Web-based        | [shortest_path](shortest_path)         | tw454 + hwr26    |
| 3     | Minimum Spanning Tree (MST)       | Web-based        | [minimum_spanning_tree](minimum_spanning_tree)             | tw454 + hwr26    |
| 4     | Maximum Flow                      | Jupyter Notebook | [maximum_flow](maximum_flow)                               | fms9             |
| 5     | Baseball Elimination              | Jupyter Notebook | [baseball_elimination](baseball_elimination)               | qz245            |
| 6     | Transportation I+II               | Jupyter Notebook | [transportation](transportation)                           | qz245            |
| 6     | First-Year Writing Seminar        | Jupyter Notebook | [first_year_writing_seminar](first_year_writing_seminar)   | qz245            |
| 7     | Simplex                           | Jupyter Notebook | [simplex](simplex)                                         | hwr26            |
| 8     | LP Formulation -*WIP*-            |                  |                                                            |                  |
| 9     | Seat Packing                      | Jupyter Notebook | [seat_packing](seat_packing)                               | qz245            |
| 10    | Knapsack + Branch & Bound -*WIP*- |                  |                                                            |                  |
| 11    | Game Theory                       | Jupyter Notebook | [game_theory](game_theory)                                 | sea78            |

*Authors should be listed in chronological order of their latest contribution. Hence, the right-most person should serve as the first point of contact for questions regarding the lab.

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



