# same imports as in Jupyter Notebook
import numpy as np
import pandas as pd
import math, itertools
import matplotlib.pyplot as plt
import networkx as nx
from ortools.linear_solver import pywraplp as OR
from ortools.graph import pywrapgraph as ORMC

# Visualization for a small input graph to the assignment problem (code taken directly from FWS lab .py file)
# 'students' and 'classes' are lists, 'edges' is a dictionary of edges : preference
def small_ex(students,classes,edges):
    EDGES = [*edges]

    # graph creation
    B = nx.DiGraph()
    B.add_nodes_from(students,bipartite=0)
    B.add_nodes_from(classes,bipartite=1)
    for edge in EDGES:
        B.add_edges_from([edge], weight=edges[edge])
    edge_weight=nx.get_edge_attributes(B,'weight')

    # node placement
    pos = {}
    pos.update((node,(1,-index)) for index,node in list(enumerate(students)))
    pos.update((node,(2,-1.5*(index+0.5))) for index,node in list(enumerate(classes)))

    options = {
    'node_color': 'lightblue',
    'node_size': 500,
    }
    costs = []
    for e in EDGES:
        if not edge_weight[e] in costs:
            costs.append(edge_weight[e])
    edge_col = ['blue' if edge_weight[e]==costs[0] else 'orange' if edge_weight[e]==costs[1] else 'lightgrey' for e in EDGES]

    nx.draw_networkx(B, pos=pos, arrows=True, **options)
    nx.draw_networkx_edges(B, pos, edge_color= edge_col)
    plt.axis('off')
    plt.show()


# Helper function to print results of min-cost flow formulation
# 'min_cost_flow' is the solver object returned by the function mincostflow
def printmcf(min_cost_flow):
    # solve instance
    status = min_cost_flow.Solve()

    # print results
    if status == min_cost_flow.OPTIMAL:
        print('Success')
        print('')

        prefs = {}
        for i in range(min_cost_flow.NumArcs()):
            if(min_cost_flow.Tail(i) != 0): # exclude dummy
                flow = min_cost_flow.Flow(i)
                if flow > 0:
                    cost = flow * min_cost_flow.UnitCost(i)
                    if not cost in prefs.keys():
                        prefs[cost] = 1
                    else:
                        prefs.update({cost : prefs[cost]+1})

        print('Preferences received:')
        for i in sorted(prefs):
            print('%1s: %1s' % (i,prefs[i]))
    elif status == min_cost_flow.INFEASIBLE:
        print('Infeasible')
    elif status == min_cost_flow.UNBALANCED:
        print('Unbalanced input')
    else:
        print('Error, see https://google.github.io/or-tools/cpp_graph/min__cost__flow_8h_source.html')


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


# Same as modifiedAssign, but with objective function that seeks to minimize the number of classes run
def minimizeNumClassesAssign(students, classes, edges, minstudents, csize, solver):
    STUDENT = students              # create student list
    CLASS = classes                 # create class list
    EDGES = list(edges.keys())      # create edge list

    c = edges.copy()                # define c[i,j]

    # define model
    m = OR.Solver('assignFWS', solver)

    # decision variables
    x = {}
    for i,j in EDGES:
        # define x(i,j) here
        x[i,j] = m.IntVar(0, m.infinity(), ('(%d, %s)' % (i,j)))

    y = {}
    for j in CLASS:
        # define y_j here
        y[j] = m.BoolVar('y_%s' % j) # A BoolVar or Boolean variable is similar to an integer variable,
                                     # except that it can only take on values in {0,1}, where 0 represents "false"
                                     # and 1 represents "true." We could have also used an IntVar ranging from 0 to 1.

    # define objective function here
    m.Minimize(sum(y[j] for j in CLASS))

    # add constraint to ensure each student is assigned exactly one class
    for k in students:
        m.Add(sum(x[i,j] for i,j in EDGES if i==k) == 1)

    # add constraint to ensure each class that runs satisfies minimum and maximum class size
    for k in classes:
        m.Add(sum(x[i,j] for i,j in EDGES if j==k) <= csize*y[k])
        m.Add(sum(x[i,j] for i,j in EDGES if j==k) >= minstudents*y[k])

    # solve
    status = m.Solve()

    if status == OR.Solver.INFEASIBLE:
        print('Infeasible')
        return

    unmatched = []
    for k in STUDENT:
        if (sum(x[i,j].solution_value() for i,j in EDGES if i==k) == 0):
            unmatched.append(k)
    if len(unmatched) != 0:
        print("Unmatched students:",len(unmatched))
    else:
        print("All students matched.")

    matched = {}
    for i,j in EDGES:
        if x[i,j].solution_value() == 1:
            if c[i,j] in matched:
                matched[c[i,j]] += 1
            else:
                matched.update({c[i,j] : 1})

    return matched


# Same as modifiedAssign, but with additional parameter 'numclasses' to specify how many class sections run
def modifiedAssignWithNumClasses(students, classes, edges, minstudents, csize, numclasses, solver):
    if numclasses < 0 or numclasses > len(classes):
        raise ValueError('Error: numclasses must be in the range [0,len(classes)].')

    STUDENT = students              # create student list
    CLASS = classes                 # create class list
    EDGES = list(edges.keys())      # create edge list

    c = edges.copy()                # define c[i,j]

    # define model
    m = OR.Solver('assignFWS', solver)

    # decision variables
    x = {}
    for i,j in EDGES:
        # define x(i,j) here
        x[i,j] = m.IntVar(0, m.infinity(), ('(%d, %s)' % (i,j)))

    y = {}
    for j in CLASS:
        # define y_j here
        y[j] = m.BoolVar('y_%s' % j) # A BoolVar or Boolean variable is similar to an integer variable,
                                     # except that it can only take on values in {0,1}, where 0 represents "false"
                                     # and 1 represents "true." We could have also used an IntVar ranging from 0 to 1.

    # define objective function here
    m.Minimize(sum(c[i,j]*x[i,j] for i,j in EDGES))

    # add constraint to ensure each student is assigned exactly one class
    for k in students:
        m.Add(sum(x[i,j] for i,j in EDGES if i==k) == 1)

    # add constraint to ensure each class that runs satisfies minimum and maximum class size
    for k in classes:
        m.Add(sum(x[i,j] for i,j in EDGES if j==k) <= csize*y[k])
        m.Add(sum(x[i,j] for i,j in EDGES if j==k) >= minstudents*y[k])

    # add constraint that exactly numclasses classes are open
    m.Add(sum(y[j] for j in CLASS) == numclasses)

    # solve
    status = m.Solve()

    if status == OR.Solver.INFEASIBLE:
        print('Infeasible')
        return

    unmatched = []
    for k in STUDENT:
        if (sum(x[i,j].solution_value() for i,j in EDGES if i==k) == 0):
            unmatched.append(k)
    if len(unmatched) != 0:
        print("Unmatched students:",len(unmatched))
    else:
        print("All students matched.")

    matched = {}
    for i,j in EDGES:
        if x[i,j].solution_value() == 1:
            if c[i,j] in matched:
                matched[c[i,j]] += 1
            else:
                matched.update({c[i,j] : 1})

    return matched


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
