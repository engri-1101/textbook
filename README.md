ENGRI 1101 Labs
===============

**NOTE:** This git repo was created at the end of Summer 2020 after significant course development. All labs were replaced with a web-based or Jupyter Notebook equivalent. AMPL was replaced by Google's OR-Tools.

This git repo serves as the standard for ENGRI 1101 lab software / files (while [Overleaf](https://www.overleaf.com/project/5ecf1b879f37710001f9f54d) serves as the standard for lab handouts). Any updates or additional labs should be added here. Furthermore, this README contains a comprehensive list of labs as well as all necessary Python packages. They should be updated to reflect any changes made to the labs.

### Installation

For those interested in using these labs or developing them further, we provide
a breif introduction. The following commands clone the repo and apply the given
git configuration.

```
git clone https://github.coecis.cornell.edu/hwr26/engri-1101-labs.git
cd engri-1101-labs
git config --local include.path ../.gitconfig
```

Some labs have distribution files which are too large to upload to GitHub
(300.00 MB size limit). To generate the distribution files for these labs, run
the following bash script.

```
bash update_distros.sh
```

The last line will create zipped distribution files for all the labs. Each distribution file will be placed in the corresponding directory for the lab (See Directory Structure).

For those interested in developing a new lab, there are a few tools provided in the repo to ease this process. First, create a directory for the new lab called `lab_name`. All dependencies for this lab: data, images, python scripts, etc.. should be put in this directory. Build the key Jupyter Notebook file. This should be named `lab_name_key.ipynb`. There are two types of supported questions: text and code. To generate the student version correctly, the following format should be used:

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

Create a python script called `zip.py` using one from another lab as a template. State which files / directories should be contained in the distribution file. The file `lab_name.ipynb` is the student version of the lab file which is automatically generated. It should be included in the distribution file. Lastly, edit the bash script `update_distros.sh` to include `make_student_version lab_name` and `zip lab_name`. Run `bash update_distros.sh` to generate the student version and distribution file!

### Directory Structure

- **Labs:** Each lab has a corresponding directory in the repo. Lab directories contain some subset of the following:
    - Tex files / pdfs for the prelab and/or lab (time stamp indicates the day they were pulled from [Overleaf](https://www.overleaf.com/project/5ecf1b879f37710001f9f54d))
    - Relevant notebooks for generating data used in the labs
    - Notes from Fall 2020 semester with common issues / questions regarding the lab
    - `data-lab` / `data-demo` for data used in the lab or demo respectively
    - `images-lab` / `images-key` / `images-demo` for images used in the lab, answer key, or demo respectively
    - `.py` files used by the lab and/or demo
    - Jupyter notebooks for lab, answer key, and demos (`_colab` indicates compatibility with [Google Colab](https://colab.research.google.com/notebooks/intro.ipynb))
    - `.zip` files used to distribute the lab and demos to students
    - `zip.py` for generating the distribution files from other files in the directory
- **Website:** The directory [public_html](public_html) contains the source code for the course site ([http://engri1101.orie.cornell.edu/](http://engri1101.orie.cornell.edu/)). It also contains the [raphael](https://github.com/DmitryBaranovskiy/raphael) JavaScript vector library used by the web-based labs. Each web-based lab directory contains a file called web_lab_source.md which contains a link to that lab's source code in [public_html](public_html). The document root of the course site is set to be [public_html](public_html). Hence, any changes within [public_html](public_html) will be reflected on the website in the next pull. For this reason, <ins> *exercise extra precaution when updating the source code of web-based labs!* </ins>
- [software_install](software_install) contains software installation instructions and a notebook to test the installation.
- [tutorials](tutorials) contains tutorials for OR-Tools (aimed at those coming
  from AMPL).
- [lp_package_testing](lp_package_testing) contains analysis of potential Python-based LP packages (Summer 2020).
- [gilp_lab_submissions](gilp_lab_submissions) contains parsed student lab submissions (Fall 2020) for labs using the `gilp` python package.
- [make_student_version.py](make_student_version.py) is a python script for creating a student version of a lab from a  key file.
- [update_distros.sh](update_distros.sh) is a bash script for updating distribution files in all labs (run with `bash update_distros.sh`)
- [tex](tex) contains files needed to generate the pdfs.


### Fall 2020 Schedule

| Lab # | Name                              | Prelab                                                                                 | Lab |
|-------|-----------------------------------|----------------------------------------------------------------------------------------|-----|
| 1     | Travelling Salesman Problem (TSP) | [tsp_prelab.pdf](travelling_salesman_problem/tsp_prelab_tex_2020-12-3/tsp_prelab.pdf)  | [tsp_lab.pdf](travelling_salesman_problem/tsp_lab_tex_2020-12-3/tsp_lab.pdf) |
| 2     | Shortest Path                     | [shortest_path_prelab.pdf](shortest_path/shortest_path_prelab_tex_2020-12-3/shortest_path_prelab.pdf) |[shortest_path_lab.pdf](shortest_path/shortest_path_lab_tex_2020-12-3/shortest_path_lab.pdf) |
| 3     | Software Installation             |   |  [software_install.pdf](software_install/software_install_tex/software_install.pdf) <br/> [test_install.ipynb](software_install/test_install.ipynb) <br/> [shortest_path_demo.zip](shortest_path/shortest_path_demo.zip) |
| 4     | Minimum Spanning Tree (MST)       | [mst_prelab.pdf](minimum_spanning_tree/mst_prelab_tex_2020-12-3/mst_prelab.pdf) | [mst_lab.pdf](minimum_spanning_tree/mst_lab_tex_2020-12-3/mst_lab.pdf) |
| 5     | Maximum Flow (1-2)                | [max_flow_prelab.pdf](maximum_flow/max_flow_prelab_tex_2020-12-3/max_flow_prelab.pdf) | [max_flow_lab.zip](maximum_flow/max_flow_lab.zip) |
| 6     | Maximum Flow (3-4)                | | [max_flow_lab_part3-4.zip](maximum_flow/max_flow_lab_part3-4.zip) |
| 7     | Baseball Elimination              | [baseball_elimination_prelab.pdf](baseball_elimination/baseball_elimination_prelab_tex_2020-12-3/baseball_elimination_prelab.pdf) | [baseball_elimination_lab.zip](baseball_elimination/baseball_elimination_lab.zip) |
| 8     | Transportation I+II               | [transportation_prelab.pdf](transportation/transportation_prelab_tex_2020-12-3/transportation_prelab.pdf) | [transportation_lab.ipynb](transportation/transportation_lab.ipynb) |
| 9     | First-Year Writing Seminar + Simplex (1) | [simplex_prelab.pdf](simplex/simplex_prelab_tex_2020-12-3/simplex_prelab.pdf) | [fws_lab.zip](fws/fws_lab.zip) <br/> [simplex_lab.ipynb](simplex/simplex_lab.ipynb) |
| 10    | Simplex (2-4)                     | | [simplex_lab.ipynb](simplex/simplex_lab.ipynb) |
| 11    | LP Formulation & Seat Packing     | [lp_formulation_prelab.pdf](lp_formulation/lp_formulation_prelab_tex_2020-12-3/lp_formulation_prelab.pdf) | [lp_formulation_lab.ipynb](lp_formulation/lp_formulation_lab.ipynb) <br/> [seat_packing_lab.zip](seat_packing/seat_packing_lab.zip) |
| 12    | Branch and Bound & Knapsack       | [bnb_prelab.pdf](branch_and_bound/bnb_prelab_tex_2020-12-3/bnb_prelab.pdf) | [branch_and_bound_lab.zip](branch_and_bound/branch_and_bound_lab.zip) |
| 13    | Diet                              |  [diet_prelab.pdf](diet/diet_prelab_tex_2020-12-8/diet_prelab.pdf) | [diet_lab.zip](diet/diet_lab.zip) |
| 14    | Game Theory                       | | [game_theory_lab.zip](game_theory/game_theory_lab.zip)  |

### Comprehensive List of Python Packages

| Package                                                      | Description                                                            |
|--------------------------------------------------------------|------------------------------------------------------------------------|
| [gilp](https://github.com/henryrobbins/gilp)                 | Visualize the simplex algorithm and solve linear programs              |
| [ortools](https://github.com/google/or-tools)                | Google's optimization suite                                            |
| [networkx](https://github.com/networkx/networkx)             | Create and manipulate complex networks                                 |
| [matplotlib](https://github.com/matplotlib/matplotlib)       | Publication quality figures in python                                  |
| [pandas](https://github.com/pandas-dev/pandas)               | High-performance, easy-to-use data structures and data analysis tools  |
| [bokeh](https://github.com/bokeh/bokeh)                      | Statistical and novel interactive html plots for python                |
| [shapely](https://github.com/Toblerity/Shapely)              | Manipulation and analysis of geometric objects in the cartesian plane  |
| [scipy](https://github.com/scipy/scipy)                      | Scientific library for python                                          |
| [scikit-image](https://github.com/scikit-image/scikit-image) | Image processing routines for scipy                                    |
| [numpy](https://github.com/numpy/numpy)                      | Array processing for numbers, strings, records, and objects            |
| [descartes](https://pypi.org/project/descartes/)             | Use geometric objects as matplotlib paths and patches                  |
| [geopandas](https://pypi.org/project/geopandas/)             | Geographic pandas extensions                                           |

### **TODO**

| Link                                           | TODO                                          |
|------------------------------------------------|-----------------------------------------------|
| [minimum_spanning_tree](minimum_spanning_tree) | Clustering application to NYC taxi data <br/> Some at scale visualization |
| [game_theory](game_theory)                     | Verify correctness of penalty kick game        |
| [fws](fws)                                     | Add section minimum constraint for IP example |
| [redistricting](redistricting)                 | Optimize the redistricting 5x10 example <br/> Tetrominoes Tetris completion example |
| [shortest_path](shortest_path)                 | Modeling example of text splitting (past HW)  |
| [vinal](https://github.com/henryrobbins/vinal) package| Make bottom text more visible (highlight / color) |
| [baseball_elimination](baseball_elimination)   | ECAC Cornell Hockey |
| N/A                                            | Github [Markup
rendering](https://github.com/github/markup/issues/369) |
