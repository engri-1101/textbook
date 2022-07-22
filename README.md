ENGRI 1101 Labs
===============

**NOTE:** This repo was created at the end of Summer 2020 after significant
course development. All labs were replaced with a web-based or Jupyter Notebook
equivalent. AMPL was replaced by Google's OR-Tools.

This repo serves as the standard for ENGRI 1101 lab software / files.
[Overleaf](https://www.overleaf.com/project/5ecf1b879f37710001f9f54d) serves as
the standard for pre-lab/lab handouts. Archives of distribution files
(including both pre-lab and lab handouts) can be found on
[box](https://cornell.box.com/s/t3f8yntntr8z265decbkjzhz2fdbd6t9).
The archive currently includes the Fall 2020 and Spring 2022 semesters. If you
need access to this archive, please email Henry (hwr26@cornell.edu).

## Installation

To clone the repo and create distribution files for the latest versions of
these labs, run the following commands. Be aware this takes a moment.

```
git clone https://github.coecis.cornell.edu/hwr26/engri-1101-labs.git
cd engri-1101-labs/labs
make all
```

This will create a distribution file called `<lab_name>_lab.zip` within each
lab directory. Note that this distribution file does not include any
pre-lab or lab handouts.

## Development

To work on developing these labs, you will need to run an additional command
after cloning the repository. If you are new to using Git, see the
[Git Tutorial](tutorials/git/git.md).

```
git clone https://github.coecis.cornell.edu/hwr26/engri-1101-labs.git
cd engri-1101-labs
git config --local include.path ../.gitconfig
```

Here, the last command configures git to filter out Jupyter Notebook output and
metadata. This makes version control of Jupyter Notebooks more pleasant. See
the labs [README](labs/README.md) for instructions on creating a new lab.

## Directory Structure

- [public_html](public_html) contains the source code for the course site
  ([http://engri1101.orie.cornell.edu/](http://engri1101.orie.cornell.edu/)).
  It also contains the [raphael](https://github.com/DmitryBaranovskiy/raphael)
  JavaScript vector library used by the web-based labs. Each web-based lab
  directory contains a file called web_lab_source.md which contains a link to
  that lab's source code in [public_html](public_html). The document root of
  the course site is set to be [public_html](public_html). Hence, any changes
  within [public_html](public_html) will be reflected on the website in the
  next pull. For this reason, <ins> *exercise extra precaution when updating
  the source code of web-based labs!* </ins>
- [labs](labs) contains all lab directories and a [README](labs/README.md)
  summarizing how to build labs, lab directory structure, and a list of labs.
- [software_install](software_install) contains software installation
  instructions and a notebook to test the installation.
- [tutorials](tutorials) contains tutorials for OR-Tools (aimed at teaching
  assistants who come from an AMPL background).
- [lp_models_and_examples](lp_models_and_examples) contains a large selection
  of example LP and IP models written in OR-Tools.
- [lp_package_testing](lp_package_testing) contains analysis of potential
  Python-based LP packages (Summer 2020).
- [gilp_lab_submissions](gilp_lab_submissions) contains parsed student lab
  submissions (Fall 2020) for labs using the `gilp` python package.

## TODO

| Link                                           | TODO                                          | Assigned |
|------------------------------------------------|-----------------------------------------------|----------|
| [minimum_spanning_tree](labs/minimum_spanning_tree) | Review clustering application to NYC taxi data | |
| [redistricting](labs/redistricting)                 | Optimize the redistricting 5x10 example <br/> Tetrominoes Tetris completion example | scs293 |
| [vinal](https://github.com/henryrobbins/vinal) package| Make bottom text more visible (highlight / color) | hwr26 |
| [baseball_elimination](labs/baseball_elimination)   | Finish incorporating ECAC Cornell Hockey | |
| N/A                                            | Github [Markup rendering](https://github.com/github/markup/issues/369) | hwr26 |
| N/A                                            | Build labs from parts in separate notebooks   | hwr26 |
| [make_student_version.py](labs/make_student_version.py) | Make this script more robust | hwr26 |
| [project_selection](labs/project_selection)    | Review and standardize                        | |
| [minimum_cut](labs/minimum_cut)                | Review and standardize                        | |
| [fws](labs/fws)                                | Review and standardize                        | |
| [game_theory](labs/game_theory)                | Review and standardize                        | |
| [game_theory](labs/game_theory)                | Verify correctness of penalty kick game       | |
| [shortest_path](labs/shortest_path)            | Port line break demo GUI to Bokeh             | |
| [shortest_path](labs/shortest_path)            | Port inventory demo GUI to Bokeh              | |