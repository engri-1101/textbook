# Python LP Package Report
*Henry Robbins (2020) | Based on George Frentzel's Report*

## Pyomo
### Pros
- Quick installation using terminal in conda
- Uses AMPL dat file (more or less identical)
- Abstract methods
- Syntax most similar to AMPL mod files
### Cons
- Poor syntax - does not read well
- Lengthy variables
- Objectives and constraints defined by functions
### Installation
- [Instructions](http://www.pyomo.org/installation)
- `conda install -c conda-forge pyomo`

## PuLP
### Pros
- Quick installation using terminal in conda
- Better syntax then Pyomo
### Cons
- Does not differentiate between objective and constraints well
- Does not have abstract models
- Have to write .lp file before solving
### Installation
- [Instructions](https://pypi.org/project/PuLP/)
- `pip install pulp`

## GurobiPy
### Pros
- World-class solver
- Similar syntax to open-source PySCIPOpt software
- Potential advantage to have students manipulating data not using .dat file
- Great syntax
### Cons
- Not open-source - not as useful after students graduate
- Trying to obtain academic license as a remote student
- More steps to the installation process
- Must update model after declaring variables
### Installation
- [Instructions](https://www.gurobi.com/documentation/8.1/quickstart_mac/installing_the_anaconda_py.html#section:Anaconda)
- Acquire a [Gurobi license](https://www.gurobi.com/documentation/8.1/quickstart_mac/retrieving_a_free_academic.html)
- `conda config --add channels http://conda.anaconda.org/gurobi`
- `install gurobi`

## PySCIPOpt
### Pros
- Open-source
- Potential advantage to have students manipulating data not using .dat file
- Great syntax
### Cons
- Nightmare to install
- Less reliable
- Potential issues with dual values
### Installation
Somewhat helpful: [Handout](https://imada.sdu.dk/~marco/DM871/Training/dm545_lab_scip.pdf) from University of Southern Denmark, Odense Lab
1. Download [Homebrew](https://brew.sh/)
    1. `brew install cmake`
    2. `brew install gcc`
    3. `brew install boost`
2. Download [SCIP Optimization Suite](https://scip.zib.de/index.php#download) (scipoptsuite-7.0.0.tgz)
    1. Further instructions in README Change the following lines in CMakeLists.text (double check this)
    2. option(PAPILO "should papilo library be linked" OFF)
        1. option(ZIMPL "should zimpl be linked" OFF)
        2. ption(GMP "should GMP be linked" OFF)
        3. option(GCG "should GCG be included" OFF)
        4. option(SOPLEX "should SOPLEX be included" OFF)
    3. Run the following in terminal from the unzipped scipoptsuite-7.0.0
        1. `mkdir build`
        2. `cd build`
        3. `cmake ..`
        4. `make`
        5. `make check`
        6. `make install`
4. Install the [PySCIPOpt](https://github.com/SCIP-Interfaces/PySCIPOpt/blob/master/INSTALL.md) module
    1. `export SCIPOPTDIR=<path_to_install_dir>`
    2. `pip install pyscipopt`
5. [Documentation](https://scipbook.readthedocs.io/en/latest/index.html) and [Classes](http://scip-interfaces.github.io/PySCIPOpt/docs/html/annotated.html)


## OR-Tools (Google)
### Pros
- Easy to download
- Uses open source LP optimization solver: [Glop](https://developers.google.com/optimization/lp/lp)
- Uses open source MIP optimization solver: [CBC](https://github.com/coin-or/Cbc)
- Similar syntax to both GurobiPy and PySCIPOpt
- Excellent [documentation](https://developers.google.com/optimization/reference/python/linear_solver/pywraplp#constraint)
### Cons
- No abstract models
### Installation
- [Instructions](https://developers.google.com/optimization/install)
- `python -m pip install --upgrade --user ortools`
- **NO LONGER NEED TO INSTALL FROM SOURCE TO USE GUROBI**
- From source (to use third-party solvers): [source installation](https://developers.google.com/optimization/install/python/source_mac)
    - Add to Makefile.local
        - `UNIX_GUROBI_DIR = /Library/gurobi902/`
        - `GUROBI_LIB_VERSION = 90`
- Use solver: `OR.Solver.GUROBI_MIXED_INTEGER_PROGRAMMING`
- [External solvers](https://google.github.io/or-tools/java/enumcom_1_1google_1_1ortools_1_1linearsolver_1_1MPModelRequest_1_1SolverType.html)
