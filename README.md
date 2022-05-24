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

- **Website:** The directory [public_html](public_html) contains the source code for the course site ([http://engri1101.orie.cornell.edu/](http://engri1101.orie.cornell.edu/)). It also contains the [raphael](https://github.com/DmitryBaranovskiy/raphael) JavaScript vector library used by the web-based labs. Each web-based lab directory contains a file called web_lab_source.md which contains a link to that lab's source code in [public_html](public_html). The document root of the course site is set to be [public_html](public_html). Hence, any changes within [public_html](public_html) will be reflected on the website in the next pull. For this reason, <ins> *exercise extra precaution when updating the source code of web-based labs!* </ins>
- [software_install](software_install) contains software installation instructions and a notebook to test the installation.
- [tutorials](tutorials) contains tutorials for OR-Tools (aimed at those coming
  from AMPL).
- [lp_package_testing](lp_package_testing) contains analysis of potential Python-based LP packages (Summer 2020).
- [gilp_lab_submissions](gilp_lab_submissions) contains parsed student lab submissions (Fall 2020) for labs using the `gilp` python package.
- [make_student_version.py](make_student_version.py) is a python script for creating a student version of a lab from a  key file.
- [update_distros.sh](update_distros.sh) is a bash script for updating distribution files in all labs (run with `bash update_distros.sh`)
- [tex](tex) contains files needed to generate the pdfs.

### Archive

Archives of distribution files (including both pre-lab and lab files) can
be found on [box](https://cornell.box.com/s/t3f8yntntr8z265decbkjzhz2fdbd6t9).
The archive currently includes the Fall 2020 and Spring 2022 semesters. If you
need access to this archive, please email hwr26@cornell.edu.

### **TODO**

| Link                                           | TODO                                          | Assigned |
|------------------------------------------------|-----------------------------------------------|----------|
| [minimum_spanning_tree](minimum_spanning_tree) | Review clustering application to NYC taxi data | |
| [redistricting](redistricting)                 | Optimize the redistricting 5x10 example <br/> Tetrominoes Tetris completion example | scs293 |
| [vinal](https://github.com/henryrobbins/vinal) package| Make bottom text more visible (highlight / color) | hwr26 |
| [baseball_elimination](baseball_elimination)   | ECAC Cornell Hockey | |
| N/A                                            | Github [Markup rendering](https://github.com/github/markup/issues/369) | hwr26 |
| [project_selection](labs/project_selection)    | Review and standardize                        | |
| [minimum_cut](labs/minimum_cut)                | Review and standardize                        | |
| [fws](labs/fws)                                | Review and standardize                        | |
| [game_theory](labs/game_theory)                | Review and standardize                        | |
| [game_theory](labs/game_theory)                | Verify correctness of penalty kick game       | |
| [shortest_path](labs/shortest_path)            | Port line break demo GUI to Bokeh             | |
| [shortest_path](labs/shortest_path)            | Port inventory demo GUI to Bokeh              | |