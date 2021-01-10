#!/bin/bash

make_student_version() {
    # get path for both key and student version
    key=$1_key.ipynb
    student=$1.ipynb
    # only create student version if the key file has changed
    if [[ $(git diff "$key") ]]; then
        python make_student_version.py $key
        jupyter nbconvert --ClearOutputPreprocessor.enabled=True --clear-output --inplace $student
        echo $student" - student version created successfully."
    else
        echo $student" - lab key file unchanged."
    fi
}

zip () {
    cd "$1"
    echo $PWD
    python zip.py
    echo 'zipped successfully.'
    cd ..
}

# Make student version of key file
make_student_version lp_formulation/lp_formulation_lab
make_student_version baseball_elimination/baseball_elimination_lab
make_student_version transportation/transportation_lab
make_student_version first_year_writing_seminar/fws_lab
make_student_version simplex/simplex_lab
make_student_version tsp_integer_programming/tsp_integer_programming_lab
make_student_version seat_packing/seat_packing_lab
make_student_version branch_and_bound/branch_and_bound_lab
make_student_version diet/diet_lab
make_student_version game_theory/game_theory_lab
make_student_version min-cost_flow/min-cost_flow_lab
make_student_version shortest_path/shortest_path_lab

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