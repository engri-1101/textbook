# same imports as in Jupyter Notebook
import numpy as np
import pandas as pd
import math, itertools
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite
from ortools.linear_solver import pywraplp as OR

# graph visualization for small examples (1 or 2 preferences)
# 'students' and 'classes' are lists, 'edges' is a dictionary of edges : unit costs
def small_ex(classes,students,edges):
    EDGES = [*edges]

    students_seen = []
    first_edges = {}
    second_edges = {}
    dummy_edges = {}
    for edge in EDGES:
        stud = edge[0]
        if stud == 'dummy':
            dummy_edges[edge] = edges[edge]
        elif stud not in students_seen:
            students_seen.append(stud)
            first_edges[edge] = edges[edge]
        else:
            second_edges[edge] = edges[edge]

    # graph creation
    B = nx.DiGraph()
    B.add_nodes_from(classes,bipartite=0)
    B.add_nodes_from(students,bipartite=1)
    for edge in first_edges:
        B.add_edges_from([edge], edgetype='first')
    for edge in second_edges:
        B.add_edges_from([edge], edgetype='second')
    for edge in dummy_edges:
        B.add_edges_from([edge], edgetype='dummy')
    edge_type=nx.get_edge_attributes(B,'edgetype')

    # node placement
    pos = {}
    pos.update((node,(1,-index)) for index,node in list(enumerate(students)))
    pos.update((node,(2,-1.5*(index+0.5))) for index,node in list(enumerate(classes)))

    options = {
    'node_color': 'lightblue',
    'node_size': 500,
    }

    edge_col = ['blue' if edge_type[e]=='first' else 'orange' if edge_type[e]=='second' else 'lightgrey' for e in EDGES]

    nx.draw_networkx(B, pos=pos, arrows=True, **options)
    nx.draw_networkx_edges(B, pos, edge_color= edge_col)
    plt.axis('off')
    plt.show()


# formatting function for data
# 'preferences' is a pandas DataFrame containing students and their preferences (preference column headers must be numerical)
#               Note: if a student has k feasible preferences where k < 5, the DataFrame should have zeroes as entries
#               for that student's last (5-k) preferences
# 'cost' is a dictionary of edge type : unit cost
def inputData(preferences, cost):
    # list of students
    students = list(preferences.index)

    # list of classes
    classes = []
    for c in preferences.columns:
        classes = classes + list(preferences[c].unique())
    classes = sorted(list(set(classes)))

    # check if preferences are full
    full_prefs = True
    if 0 in classes:
        full_prefs = False
        classes.remove(0)

    # dictionary of edges : edge costs
    edges = {}
    for c in preferences:
        for s in students:
            edges[(preferences.at[int(s),c], s)] = cost[int(c)]

    # add dummy if necessary
    if 'dummy' in cost.keys():
        students.append('dummy')
        # add dummy edges
        dummy_edges = list(itertools.product(['dummy'], classes))
        for edge in dummy_edges:
            edges[edge] = cost['dummy']

    # remove empty preferences if necessary
    if not full_prefs:
        edges_to_delete = []
        for i,j in edges:
            if j == 0:
                edges_to_delete.append((i,j))

        for edge in edges_to_delete:
            del edges[edge]
    print('updated')
    return classes, students, edges


# return the counts of every assigned preference for some FWS solution
# 'preferences' is a pandas DataFrame containing students and their preferences (preference column headers must be numerical)
# 'x' is a dictionary of edges (student,class) : decision variables
# 'integer' specifies whether decision variables were constrained to integral values (default: True)
def solution_summary(preferences, x, integer = True):
    if not integer:
        return integrality_summary(preferences, x)

    counts = {int(i):0 for i in list(preferences.columns)}
    unassigned = 0
    matches = {k[0] : k[1] for k,v in x.items() if v.solution_value() == 1.0}
    for index, row in preferences.iterrows():
        class_to_rank = {v:k for k,v in row.to_dict().items()}
        if index in matches:
            pref = int(class_to_rank[matches[index]])
            counts[pref] += 1
        else:
            unassigned += 1
    print('')
    print('All students assigned.' if unassigned == 0 else 'Unassigned students: ' + str(unassigned))
    return counts


# show histogram of preferences
# 'match' is a dictionary preference:count, 'margin' is to adjust position of label
def Histo(match, margin=15):
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


# helper function to print results of min-cost flow formulation
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


# print classes not run (IP section)
def print_not_run(solver):
    not_run = []
    for var in solver.variables():
        name = str(var)
        if 'y_' in name and var.solution_value() == 0.0:
             not_run.append(name[name.index('_') + 1:])

    if not_run:
        print('Classes not run: ')
        print(*not_run, sep=', ')


def minimizeNumClassesAssign(preferences, costs, minstudents, csize):
    """Identical to function modifiedAssign, but with the objective function changed to minimize the number of classes that run.

    Args:
        preferences (pd.DataFrame): Preferred classes for each student.
        costs (Dict): Dictionary from edge types to unit costs.
        minstudents (int): Minimum number of students in the classroom.
        csize (int): Capacity of the classroom.
    """
    students, classes, edges = inputData(preferences, costs)
    EDGES = list(edges.keys())      # create edge list

    c = edges.copy()                # define c[i,j]

    # define model
    m = OR.Solver('FWS', OR.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    # decision variables
    x = {}
    for i,j in EDGES:
        # define x(i,j) here
        x[i,j] = m.IntVar(0, m.infinity(), ('(%s, %s)' % (i,j)))

    y = {}
    for j in classes:
        # define y_j here
        y[j] = m.BoolVar('y_%s' % j) # A BoolVar or Boolean variable is similar to an integer variable,
                                     # except that it can only take on values in {0,1}, where 0 represents "false"
                                     # and 1 represents "true." We could have also used an IntVar ranging from 0 to 1.

    # define objective function here
    m.Minimize(sum(y[j] for j in classes))

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

    classes_run = int(sum(y[j].solution_value() for j in classes))
    print(str(classes_run) + ' of ' + str(len(classes)) + ' classes run.')

    return m,x


def modifiedAssignWithNumClasses(preferences, costs, minstudents, csize, numclasses):
    """Identical to function modifiedAssign, but with additional parameter 'numclasses' to specify how many class sections run.

    Args:
        preferences (pd.DataFrame): Preferred classes for each student.
        costs (Dict): Dictionary from edge types to unit costs.
        minstudents (int): Minimum number of students in the classroom.
        csize (int): Capacity of the classroom.
        numclasses (int): Number of class sections to run.
    """
    students, classes, edges = inputData(preferences, costs)
    EDGES = list(edges.keys())      # create edge list

    if numclasses < 0 or numclasses > len(classes):
        raise ValueError('Error: numclasses must be in the range [0,len(classes)].')

    c = edges.copy()                # define c[i,j]

    # define model
    m = OR.Solver('FWS', OR.Solver.CBC_MIXED_INTEGER_PROGRAMMING)

    # decision variables
    x = {}
    for i,j in EDGES:
        # define x(i,j) here
        x[i,j] = m.IntVar(0, m.infinity(), ('(%s, %s)' % (i,j)))

    y = {}
    for j in classes:
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

    # add constraint that exactly 'numclasses' classes are open
    m.Add(sum(y[j] for j in classes) == numclasses)

    # solve
    status = m.Solve()

    if status == OR.Solver.INFEASIBLE:
        print('Infeasible')
        return

    classes_run = int(sum(y[j].solution_value() for j in classes))
    print(str(classes_run) + ' of ' + str(len(classes)) + ' classes run.')

    return m,x


# gives preference counts of a solution with (potentially) non-integral decision variables
def integrality_summary(preferences, x):
    counts = {int(i):0 for i in list(preferences.columns)}
    unassigned = 0
    matches = {}
    for k,v in x.items():
        if v.solution_value() > 0.0:
            s,c = k
            matches[s] = [c] + (matches[s] if s in matches else [])
    for s, s_prefs in preferences.iterrows():
        class_to_rank = {v:k for k,v in s_prefs.to_dict().items()}
        if s in matches:
            for c in matches[s]:
                pref = int(class_to_rank[c])
                counts[pref] += round(x[s,c].solution_value(), 2)
        else:
            unassigned += 1
    print('')
    print('All students assigned.' if unassigned == 0 else 'Unassigned students: ' + str(unassigned))
    return counts
