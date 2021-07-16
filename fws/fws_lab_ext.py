# same imports as in Jupyter Notebook
import numpy as np
import pandas as pd
import math, itertools
import matplotlib.pyplot as plt
from ortools.linear_solver import pywraplp as OR
from ortools.graph import pywrapgraph as ORMC


# ORTools min-cost flow implementation
# Based off of https://developers.google.com/optimization/flow/mincostflow
#
# 'dataset' is the name of the datafile
# 'csize' is the desired class size, filled with a combination of real and 'filler' students
# 'minstudents' is the minimum number of (real) students that must be assigned to each section (between 0 and 16)
# 'dcost' is the cost of not assigning a student to one of their top 5 preferences (i.e., cost of dummy edge)
def mincostflow(dataset='s21_fws_ballots.csv', csize=17, minstudents=0, dcost=100000):

    if minstudents > csize or minstudents < 0:
        raise ValueError('Error: minstudents must be in [0,class size].')

    students, classes, edges = inputData(dataset)

    m = len(students) # number of students
    n = len(classes) # number of class sections
    dcapacity = csize - minstudents # number of dummy students we can send to each class

    # define supply b[i] at each node i
    # ORTools spec says nodes must be nonnegative integers indexed starting at 0 (dummy supply node),
    # so class numbers are indexed from (m + 1) to (m + n), where
    # m is the number of students and n is the number of class sections
    supplies = []
    supplies.append(n*csize - m) # dummy supply node (see lab extension for formula explanation)
    for s in students:
        supplies.append(1) # each student node has supply 1
    for c in classes:
        supplies.append(-1*csize) # each class node has supply -csize (i.e., demand csize)

    # define parallel arrays, one index per arc in the min-cost flow graph
    start_nodes = []
    end_nodes = []
    capacities = []
    unit_costs = []

    # add student edges
    for i,j in edges:
        start_nodes.append(i) # start at student node
        end_nodes.append(j+m) # end at class node
        capacities.append(1)
        unit_costs.append(edges[i,j])

    # add dummy edges
    for j in classes:
        start_nodes.append(0)
        end_nodes.append(j+m)
        capacities.append(dcapacity)
        unit_costs.append(dcost)

    # create solver
    min_cost_flow = ORMC.SimpleMinCostFlow()

    # add arcs, capacities, unit costs to graph
    for i in range(0, len(start_nodes)):
        min_cost_flow.AddArcWithCapacityAndUnitCost(int(start_nodes[i]), int(end_nodes[i]), capacities[i], unit_costs[i])

    # add node supplies to graph
    for i in range(0,len(supplies)):
        min_cost_flow.SetNodeSupply(i, supplies[i])

    # solve instance
    status = min_cost_flow.Solve()

    # print results
    if status == min_cost_flow.OPTIMAL:
        print('Success')
        print('Minimum cost:', min_cost_flow.OptimalCost())
        print('')

        prefs = {}
        for i in range(len(edges)):
            flow = min_cost_flow.Flow(i)
            if flow > 0:
                cost = flow * min_cost_flow.UnitCost(i)
                if not cost in prefs.keys():
                    prefs[cost] = 1
                else:
                    prefs.update({cost : prefs[cost]+1})
            # To see the detailed flow/capacity for arc i, use following methods:
            # print([min_cost_flow.Tail(i), min_cost_flow.Head(i) - m, min_cost_flow.Flow(i), min_cost_flow.Capacity(i), cost])

        print('Student cost:', sum(i*prefs[i] for i in prefs.keys()))

        print('Preferences received:')
        for i in sorted(prefs):
            print('%1s: %1s' % (i,prefs[i]))
    elif status == min_cost_flow.INFEASIBLE:
        print('Infeasible')
    elif status == min_cost_flow.UNBALANCED:
        print('Unbalanced input')
    else:
        print('Other issue, see https://google.github.io/or-tools/cpp_graph/min__cost__flow_8h_source.html')


# 'dataset' is the name of the datafile.
# Note: if a student has k feasible preferences where k < 5, the datafile should have zeroes as entries
#       for their last (5-k) preferences
def inputData(dataset):
    data = pd.read_csv(dataset)
    # list of students
    students = data['STUDENTS'].tolist()
    # list of classes
    classes = list(np.unique(data[['1','2','3','4','5']].values))

    # check if preferences are full
    fullPrefs = True
    if 0 in classes:
        fullPrefs = False
        classes.remove(0)

    # dictionary of edges
    edges = {}
    first = data['1']
    second = data['2']
    third = data['3']
    fourth = data['4']
    fifth = data['5']
    for s in students:
        edges.update({(s,first[s-1]):1})
        edges.update({(s,second[s-1]):2})
        edges.update({(s,third[s-1]):3})
        edges.update({(s,fourth[s-1]):4})
        edges.update({(s,fifth[s-1]):5})

    if not fullPrefs:
        edges_to_delete = []
        for i,j in edges:
            if j==0:
                edges_to_delete.append((i,j))

        for edge in edges_to_delete:
            del edges[edge]

    return students, classes, edges


# 'dataset' is the name of the datafile
def inputDataBackup(dataset):
    data = pd.read_csv(dataset)
    # list of students
    students = data['STUDENTS'].tolist()
    # list of classes
    classes = list(np.unique(data[['1','2','3','4','5']].values))
    # dictionary of edges
    edges = {}
    first = data['1']
    second = data['2']
    third = data['3']
    fourth = data['4']
    fifth = data['5']
    for s in students:
        edges.update({(s,first[s-1]):1})
        edges.update({(s,second[s-1]):2})
        edges.update({(s,third[s-1]):3})
        edges.update({(s,fourth[s-1]):4})
        edges.update({(s,fifth[s-1]):5})
    return students, classes, edges


# Takes a dictionary of edge costs and returns a new dictionary with updated edge costs for each preference type
# 'oldedges' is the original dictionary of edge costs, 'newcosts' is a dictionary with new edge costs for each preference type
def updated_edge_costs(oldedges,newcosts):
    if len(np.unique(list(newcosts.values()))) != len(newcosts):
        print('WARNING: usage of non-unique edge costs for each preference type is not recommended '
              + 'if you wish to print detailed results.')

    newedges = oldedges.copy() # creates new dictionary (so we don't overwrite the old one)

    count = 1
    restart = len(newcosts) # loop around if len(newcosts) < len(oldedges)

    studentno = 0
    for edge in newedges.keys():
        cur_student = edge[0]
        if cur_student != studentno: # new student
            count = 1
            studentno = cur_student
        elif count == restart: # loop around
            count = 1
        else:
            count += 1
        newedges[edge] = newcosts[count] # update edge cost

    return newedges # return new dictionary of edges : edge costs


# show histogram of preferences
# 'match' is a dictionary preference:count, 'margin' is to adjust position of label
def Histo(match,margin):
    matches = match.copy()
    for i in range(1,6):
        if i not in matches.keys():
            matches[i] = 0
    matches = dict(sorted(matches.items()))
    keys = list(matches.keys())
    values = list(matches.values())
    plt.bar(matches.keys(), matches.values())
    plt.xlabel('Preference')
    plt.ylabel('Number of Students')
    plt.title('Histogram of Received Preferences')
    for i in matches.keys():
        plt.annotate(str(values[i-1]), xy=(keys[i-1],values[i-1]+margin), ha='center')
    plt.show()  
