#!/bin/bash

# make student version of a given key file
make_student_version() {
    # get path for both key and student version
    key=$1/$1_lab_key.ipynb
    student=$1/$1_lab.ipynb
    
    # only create student version if the key file has changed
    if [[ $(git diff "$key") ]]; then
        python make_student_version.py $key
        jupyter nbconvert --ClearOutputPreprocessor.enabled=True --clear-output --inplace $student
        echo $1" - student version created successfully."
    else
        echo $1" - lab key file unchanged."
    fi
}

# create a zipped distribution file for a given lab
zip () {
    cd "$1"
    echo $PWD
    python zip.py
    echo 'zipped successfully.'
    cd ..
}

make_student_version lp_formulation
make_student_version baseball_elimination
make_student_version transportation
make_student_version fws
make_student_version simplex
make_student_version tsp_integer_programming
make_student_version seat_packing
make_student_version branch_and_bound
make_student_version diet
make_student_version game_theory
make_student_version min-cost_flow
make_student_version shortest_path

zip transportation
zip tsp_integer_programming
zip maximum_flow
zip branch_and_bound
zip baseball_elimination
zip min-cost_flow
zip shortest_path
zip seat_packing
zip travelling_salesman_problem
zip fws
zip diet
zip game_theory