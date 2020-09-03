# same imports as in Jupyter Notebook
import pandas as pd
import math, itertools
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite
from ortools.linear_solver import pywraplp as OR

# example 1 visualization
def ex1(supply,demand,cost):
    STUDENTS = list(supply.keys())
    CLASSES = list(demand.keys())
    EDGES = list(cost.keys())
    
    # graph creation
    B = nx.DiGraph()
    B.add_nodes_from(STUDENTS,bipartite=0)
    B.add_nodes_from(CLASSES,bipartite=1)
    for edge in EDGES:
        B.add_edges_from([edge], weight=cost[edge])
    edge_weight=nx.get_edge_attributes(B,'weight')
    
    # node placement
    pos = {}
    pos.update((node,(1,-index)) for index,node in list(enumerate(STUDENTS)))
    pos.update((node,(2,-1.5*(index+0.5))) for index,node in list(enumerate(CLASSES)))
    
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


# example 2 visualization
# 'students' is a list, 'edges' is a dictionary of edges : preference
def ex2(supply,demand,cost):
    STUDENTS = list(supply.keys())
    CLASSES = list(demand.keys())
    EDGES = list(cost.keys())
    
    # graph creation
    B = nx.DiGraph()
    B.add_nodes_from(STUDENTS,bipartite=0)
    B.add_nodes_from(CLASSES,bipartite=1)
    for edge in EDGES:
        B.add_edges_from([edge], weight=cost[edge])
    edge_weight=nx.get_edge_attributes(B,'weight')
    
    # node placement
    pos = {}
    pos.update((node,(1,-1.25*index)) for index,node in list(enumerate(STUDENTS)))
    pos.update((node,(2,-2*(index+0.75))) for index,node in list(enumerate(CLASSES)))
    
    options = {
    'node_color': 'lightblue',
    'node_size': 500,
    }
    edge_col = ['blue' if edge_weight[e]==1 else 'orange' if edge_weight[e]==2 else 'lightgrey' for e in EDGES]
    
    nx.draw_networkx(B, pos=pos, arrows=True, **options)
    nx.draw_networkx_edges(B, pos, edge_color= edge_col)
    plt.axis('off')
    plt.show()


# 'dataset' is the name of the datafile
def inputData(dataset):
    data = pd.read_csv(dataset)
    STUDENT = data['STUDENTS'].tolist()
    # cost
    cost = {}
    first = data['1']
    second = data['2']
    third = data['3']
    fourth = data['4']
    fifth = data['5']
    for s in STUDENT:
        cost.update({(s,str(first[s-1])):1})
        cost.update({(s,str(second[s-1])):2})
        cost.update({(s,str(third[s-1])):3})
        cost.update({(s,str(fourth[s-1])):4})
        cost.update({(s,str(fifth[s-1])):5})
    # demand
    CLASS = []
    for y in [first, second, third, fourth, fifth]:
        for x in y:
            if not x in CLASS:
                CLASS.append(x)
    demand = {}
    for d in CLASS:
        demand.update({str(d):16})
    # supply
    supply = {}
    for s in STUDENT:
        supply.update({s:1})
    supply.update({0:len(CLASS)*16})

    return supply, demand, cost

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
    plt.show()