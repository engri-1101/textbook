#!/bin/bash

clear_output() {
    jupyter nbconvert --ClearOutputPreprocessor.enabled=True --clear-output --inplace "$1"
    echo 'cleared successfully.'
}

zip () {
    cd "$1"
    echo $PWD
    python zip.py
    echo 'zipped successfully.'
    cd ..
}

# Make student version of file from key
python make_student_version.py

# Clear output of all student versions
clear_output lp_formulation/lp_formulation_lab.ipynb
clear_output baseball_elimination/baseball_elimination_lab.ipynb
clear_output transportation/transportation_lab.ipynb
clear_output first_year_writing_seminar/fws_lab.ipynb
clear_output simplex/simplex_lab.ipynb
clear_output tsp_integer_programming/tsp_integer_programming_lab.ipynb

# Create zipped distribution files
zip transportation
zip tsp_integer_programming
zip maximum_flow
zip branch_and_bound
zip baseball_elimination
zip min-cost_flow
zip shortest_path
zip seat_packing
zip travelling_salesman_problem
zip first_year_writing_seminar
zip diet
zip game_theory