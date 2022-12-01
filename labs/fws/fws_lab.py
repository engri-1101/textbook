# same imports as in Jupyter Notebook
import numpy as np
import pandas as pd
import math, itertools
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite
from ortools.linear_solver import pywraplp as OR

def ex0(data):
    STUDENTS = list(data.index)
    CLASSES = []
    for c in data.columns:
        CLASSES = CLASSES + list(data[c].unique())
    CLASSES = sorted(list(set(CLASSES)))
    # graph creation
    B = nx.DiGraph()
    B.add_nodes_from(STUDENTS,bipartite=0)
    B.add_nodes_from(CLASSES,bipartite=1)
    for s in STUDENTS:
        for c in data:
            B.add_edge(data.at[int(s),c],s)
    
    # node placement
    pos = {}
    pos.update((node,(1,-index*2)) for index,node in list(enumerate(CLASSES)))
    pos.update((node,(2,-1.5*(index+0.5))) for index,node in list(enumerate(STUDENTS)))
    
    options = {
    'node_color': 'lightblue',
    'node_size': 500,
    }


    nx.draw_networkx(B, pos=pos, arrows=False, **options)
    nx.draw_networkx_edges(B, pos, arrows=False)
    plt.axis('off')
    plt.show()


# example 1 visualization
# 'students' and 'classes' are lists, 'edges' is a dictionary of edges : preference
def ex1(classes,students,edges):
    EDGES = [*edges]
    
    # graph creation
    B = nx.DiGraph()
    B.add_nodes_from(classes,bipartite=0)
    B.add_nodes_from(students,bipartite=1)
    for edge in EDGES:
        B.add_edges_from([edge], weight=edges[edge])
    edge_weight=nx.get_edge_attributes(B,'weight')
    
    # node placement
    pos = {}
    pos.update((node,(1,-1.5*(index+0.5))) for index,node in list(enumerate(classes)))
    pos.update((node,(2,-index)) for index,node in list(enumerate(students)))
    
    options = {
    'node_color': 'lightblue',
    'node_size': 500,
    }
    costs = []
    for e in EDGES:
        if not edge_weight[e] in costs:
            costs.append(edge_weight[e])
    edge_col = ['blue' if edge_weight[e]==costs[0] else 'orange' if edge_weight[e]==costs[1] else 'lightgrey' for e in B.edges]

    nx.draw_networkx(B, pos=pos, arrows=False, **options)
    nx.draw_networkx_edges(B, pos, edge_color= edge_col)
    plt.axis('off')
    plt.show()

# example 2 visualization
# 'students' is a list, 'edges' is a dictionary of edges : preference
def ex2(students,edges):
    STUDENT = []
    STUDENT.extend(students)
    STUDENT.append(0)
    CLASS = []
    EDGES = [*edges]
    for edge in EDGES:
        if not edge[1] in CLASS:
            CLASS.append(edge[1])
    CLASS = sorted(CLASS)
    newedges = list(itertools.product([0], CLASS))
    EDGES.extend(newedges)
    c = edges.copy()     # c[i,j] = rank
    for edge in newedges:
        c.update({edge : 3})
    
    # graph creation
    B = nx.DiGraph()
    B.add_nodes_from(STUDENT,bipartite=0)
    B.add_nodes_from(CLASS,bipartite=1)
    for edge in EDGES:
        B.add_edges_from([edge], weight=c[edge])
    edge_weight=nx.get_edge_attributes(B,'weight')
    
    # node placement
    pos = {}
    pos.update((node,(1,-2*(index+0.75))) for index,node in list(enumerate(STUDENT)))
    pos.update((node,(2,-1.25*index)) for index,node in list(enumerate(CLASS)))
    
    options = {
    'node_color': 'lightblue',
    'node_size': 500,
    }
    edge_col = ['blue' if edge_weight[e]==1 else 'orange' if edge_weight[e]==2 else 'lightgrey' for e in B.edges]
    
    nx.draw_networkx(B, pos=pos, arrows=True, **options)
    nx.draw_networkx_edges(B, pos, edge_color= edge_col)
    plt.axis('off')
    plt.show()


# 'dataset' is the name of the datafile
def inputData(dataset):
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


# show histogram of preferences
# 'match' is a dictionary preference:count, 'margin' is to adjust position of label
def Histo(match,margin):
    keys = list(match.keys())
    values = list(match.values())
    plt.bar(match.keys(), match.values())
    plt.xlabel('Preference')
    plt.ylabel('Number of Students')
    plt.title('Histogram of Received Preferences')
    for i in match.keys():
        plt.annotate(str(values[i-1]), xy=(keys[i-1],values[i-1]+margin), ha='center')
    return plt.show()