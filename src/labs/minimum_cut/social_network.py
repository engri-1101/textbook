import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

from max_flow import *

def generate_fb(show = True):
    """
    Returns a tuple (fb, edge_list) such that the first element is the graph of the network and the second element is a list of all the edges in the network.

    If [show] is true, then it will also print the graph to the screen before returning.
    """
    fb = nx.read_edgelist('data-lab/facebook-combined.txt', create_using = nx.Graph(), nodetype = int)
    print(nx.info(fb))

    #find the list of edges in the graph
    edge_list = []
    for line in nx.generate_edgelist(fb, delimiter=',', data=False):
        edge_list.append(eval(line))

    #display the social network
    if show:
        plt.figure(figsize=(15,10), tight_layout=True)
        pos = nx.spring_layout(fb)
        nx.draw_networkx(fb, pos, with_labels = False, node_size = 20)
        plt.show()

    return (fb, edge_list)

def generate_marvel(min_weight, show = True):
    """
    Returns a tuple (marvel, edge_list) such that the first element is the graph of the network and the second element is a list of all the edges in the network.

    [min_weight] is the minimum weight for an edge to be included in the graph.
    If [show] is true, then it will also print the graph to the screen before returning.
    """
    df = pd.read_csv('data-lab/marvel-edges.csv')

    edge_list = []
    for index, row in df.iterrows():
        if row['Weight'] > min_weight:
            edge_list.append((row['Source'], row['Target']))

    marvel = nx.Graph()
    marvel.add_edges_from(edge_list)
    print(nx.info(marvel))
    #display the social network
    if show:
        plt.figure(figsize=(15,10), tight_layout=True)
        pos = nx.spring_layout(marvel)
        nx.draw_networkx(marvel, pos, with_labels = False, node_size = 20)
        plt.show()

    return (marvel, edge_list)

def generate_erdos(show = True):
    """
    Returns a tuple (erdos, edge_list) such that the first element is the graph of the network and the second element is a list of all the edges in the network.

    If [show] is true, then it will also print the graph to the screen before returning.
    """
    file = open('data-lab/erdos2.txt', 'r')
    # lines = file.readlines()
    lines = file.read().splitlines()

    edge_list = []
    for i in range(6932, len(lines)):
        line = lines[i].split(' ')
        author = line[0]
        for j in range(1, len(line)):
            edge_list.append((author, line[j]))

    erdos = nx.Graph()
    erdos.add_edges_from(edge_list)
    print(nx.info(erdos))

    #display the social network
    if show:
        plt.figure(figsize=(15,10), tight_layout=True)
        pos = nx.spring_layout(erdos)
        nx.draw_networkx(erdos, pos, with_labels = False, node_size = 20)
        plt.show()

    return (erdos, edge_list)

def erdos_dict():
    """
    Returns a dictionary mapping author ids to author names in the Erdos network.
    """
    file = open('data-lab/erdos2.txt', 'r')
    # lines = file.readlines()
    lines = file.read().splitlines()

    #lines 3-6929 = authors
    #lines 6932- = edges with start node as first number of each line
    authors = {}
    for i in range(3, 6930):
        line = lines[i]
        fst = line.index('"')
        snd = line.index('"', fst+1)
        authors[str(i-2)] = line[fst+1:snd].upper()
        
    return authors


def solve_network(G, edge_list, density, display_color = True, display_community = False):
    """
    Creates and solves the densest subgraph problem on the given graph G. Returns the list of nodes in the community.

    [density] is the density of the subgraph we are looking for.
    If [display_color] is true, it will print the graph to the screen with all the selected vertices in red.
    If [display_community] is true, it will print the community itself to the screen.
    """
    #create a min-cut instance
    dirG = create_max_density(G, edge_list, density, custom_pos = False)
    print('solving...')
    #solve for a minimum cut
    value, cut = nx.minimum_cut(dirG, 's', 't', capacity = 'cap')
    s_cut, t_cut = cut
    vertex_nodes = []   #list of people in the cut
    edge_nodes = [] #list of edges/connections in the cut
    for node in s_cut:
        if str(node)[0] != '(' and str(node) != 's':
            vertex_nodes.append(node)
        elif str(node) != 's':
            edge_nodes.append(node)

    print('Community size: ' + str(len(vertex_nodes)))
    print('Number of connections: ' + str(len(edge_nodes)))
    print(vertex_nodes)

    #display the community as a part of the whole network
    if display_color:
        colors = {}
        for node in list(G.nodes()):
            colors[node] = 'lightblue'
        for node in vertex_nodes:
            colors[node] = '#F54343'
        colors_list = [colors[i] for i in G.nodes]
        nx.draw_networkx(G, with_labels = False, node_color = colors_list, node_size = 20)
        plt.show()

    #display the community only
    if display_community:
        com = nx.Graph()
        com.add_edges_from(edge_nodes)
        plt.figure(figsize=(15,10), tight_layout=True)
        nx.draw_networkx(com, with_labels = False, node_size = 40)
        plt.show()
        
    return vertex_nodes
