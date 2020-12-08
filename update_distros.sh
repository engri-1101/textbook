#!/bin/bash

zip () {
    cd "$1"
    echo $PWD
    python zip.py
    echo 'zipped successfully.'
    cd ..
}

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
