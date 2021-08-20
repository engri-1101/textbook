# same imports as in notebook
import pandas as pd
import numpy as np
import math, itertools
import matplotlib.pyplot as plt
import networkx as nx
from networkx.algorithms import bipartite
from ortools.linear_solver import pywraplp as OR

def visualize_clicker_sol(m):
    edges = {}
    for var in m.variables():
        if var.solution_value() > 0.0:
            nodes = var.name().strip('()').split(', ')
            edges.update({(nodes[0], nodes[1]) : var.solution_value()})

    supplies = np.unique([edge[0] for edge in edges]).tolist()
    supplies.remove('s')
    supplies.insert(0,'s')
    demands = np.unique([edge[1] for edge in edges]).tolist()
    EDGES = [*edges]

    # graph creation
    B = nx.DiGraph()
    B.add_nodes_from(supplies,bipartite=0)
    B.add_nodes_from(demands,bipartite=1)
    for edge in EDGES:
        B.add_edges_from([edge], flow = edges[edge])
    labels = nx.get_edge_attributes(B, 'flow')

    # node placement
    pos = {}
    pos.update((node,(1,-4*(index+0.5))) for index,node in list(enumerate(supplies)))
    pos.update((node,(2,-3*(index+0.5))) for index,node in list(enumerate(demands)))

    options = {
    'node_color': 'lightblue',
    'node_size': 500,
    }

    # draw nodes and edges
    nx.draw_networkx(B, pos=pos, arrows=True, **options)
    nx.draw_networkx_edges(B, pos, edge_color='gray')
    nx.draw_networkx_edge_labels(B, pos, edge_labels=labels, label_pos = 0.3)

    # draw text labels
    x,y = pos['s']
    plt.text(x-0.05, y+1.5, s='SUPPLY')

    x,y = pos['1']
    plt.text(x-0.05, y+1.5, s='DEMAND')

    plt.axis('off')
    plt.show()


def q4_graph():
    supplies = ['s','1\'','2\'','3\'']
    supply_vals = ['∞',15,12,18]
    supplies = dict(zip(supplies,supply_vals))
    demands = [1,2,3,4]
    demand_vals = [15,12,18,6]
    demands = dict(zip(demands,demand_vals))
    edges = {('s',1):20, ('s',2):20, ('s',3):20, ('s',4):20,
            ('1\'',2):10, ('1\'',3):6,
            ('2\'',3):10, ('2\'',4):6,
            ('3\'',4):10}

    EDGES = [*edges]

    # graph creation
    B = nx.DiGraph()
    B.add_nodes_from(supplies,bipartite=0)
    B.add_nodes_from(demands,bipartite=1)
    for edge in EDGES:
        B.add_edges_from([edge], weight = edges[edge])

    labels = nx.get_edge_attributes(B, 'weight')

    # node placement
    pos = {}
    pos.update((node,(1,-3*(index+0.5))) for index,node in list(enumerate(supplies)))
    pos.update((node,(2,-4*(index+0.5))) for index,node in list(enumerate(demands)))

    options = {
    'node_color': 'lightblue',
    'node_size': 500,
    }

    # draw nodes and edges
    nx.draw_networkx(B, pos=pos, arrows=True, **options)
    nx.draw_networkx_edges(B, pos, edge_color='gray')
    nx.draw_networkx_edge_labels(B, pos, edge_labels=labels, label_pos = 0.3)

    # draw text labels
    for s in supplies:
        x,y = pos[s]
        plt.text(x-0.2, y+0.1, s='s = ' + str(supplies[s]))
        if s == 's':
            plt.text(x-0.05, y+1.5, s='SUPPLY')
    for d in demands:
        x,y = pos[d]
        plt.text(x+0.08, y, s='d = ' + str(demands[d]))
        if d == 1:
            plt.text(x-0.05, y+1.75, s='DEMAND')

    plt.axis('off')
    plt.show()
