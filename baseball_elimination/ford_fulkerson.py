import matplotlib.pyplot as plt
import networkx as nx
import math
import re

class max_flow:
    """Maintains a max flow instance."""
    
    def __init__(self, G):
        """Initialize a max flow instance.
        
        Args:
            G (nx.DiGraph): Directed graph with capacities cap and positions pos
        """
        self.G = G
        self.set_initial_flow() # set intial flow
        self.create_residual_graph() # create the residual graph
        self.pos = nx.get_node_attributes(self.G,'pos')

    def set_initial_flow(self):
        """Set the intial flow on the graph G."""
        for i, j in self.G.edges:
            self.G.edges[i,j]['flow'] = 0

    def plot_flow(self, colors = None):
        """Plot the flow graph."""
        label = {}
        for i, j in self.G.edges:
            label[(i,j)] = str( self.G.edges[i,j]["flow"] ) + " / " + str( self.G.edges[i,j]["cap"] )
        plt.figure()
        if colors is None:
            nx.draw_networkx(self.G,self.pos,node_size=500,node_color='lightblue')
        else:
            colors = [colors[i] for i in self.G.nodes]
            nx.draw_networkx(self.G,self.pos,node_size=500,node_color=colors)
        nx.draw_networkx_edge_labels(self.G,self.pos,edge_labels=label);

    def create_residual_graph(self):
        """Create the flow graph for the current flow."""
        residualGraph = nx.DiGraph()
        for i, j in self.G.edges:
            c = self.G.edges[ i,j ]['cap']
            f = self.G.edges[ i,j ]['flow'] 
            if( c > f ):
                residualGraph.add_edge( i, j )
                residualGraph.edges[i,j]['residual capacity'] = c - f
                residualGraph.edges[i,j]['forward edge'] = True 
            if ( f > 0 ):
                residualGraph.add_edge( j, i )
                residualGraph.edges[j,i]['residual capacity'] = f
                residualGraph.edges[j,i]['forward edge'] = False 
        self.residual = residualGraph

    def plot_residual_graph(self, colors = None):
        """Plot the residual graph."""
        self.create_residual_graph()
        plt.figure()
        if colors is None:
            nx.draw_networkx(self.residual,self.pos,node_size=500,node_color='lightblue',connectionstyle='arc3, rad=0.1')
        else:
            colors = [colors[i] for i in self.residual.nodes]
            nx.draw_networkx(self.residual,self.pos,node_size=500,node_color=colors,connectionstyle='arc3, rad=0.1')
        residualcap = nx.get_edge_attributes( self.residual, 'residual capacity' )        
        nx.draw_networkx_edge_labels(self.residual,self.pos,edge_labels=residualcap,label_pos=0.66);

    def label(self, auto=False, show=False):
        """Label and check nodes."""
        for i in self.G.nodes:
            self.G.nodes[i]["check"] = False
        self.G.nodes['s']["check"] = True
        list = { 's' }
        if show:
            self.plot_checked(residual=True)
        while len(list) > 0:
            i = list.pop()
            if auto:
                print('Node',i,'is explored next.')
                usr_input = input('What are the neighbors?: ')
                input_neighbors = []
                for string in re.split('([\'].[\'])', usr_input):
                    node = string.strip(',\'')
                    if len(node):
                        input_neighbors.append(node)
                if set(self.residual.neighbors(i)) == set(input_neighbors):
                    neighbors = input_neighbors
                else:
                    neighbors = self.residual.neighbors(i)
                    print('Wrong. The neighbors were',list(neighbors))
            else:
                neighbors = self.residual.neighbors(i)
                
            for j in neighbors:  
                if not self.G.nodes[j]["check"]:
                    self.G.nodes[j]["check"] = True
                    self.G.nodes[j]["prev"] = i
                    list.add(j)  
            if show:
                self.plot_checked(residual=True)
        if show:
                self.plot_checked()
    
    def plot_checked(self, residual=False):
        checked = nx.get_node_attributes(self.G,'check')
        colors = {}
        for node in checked:
            colors[node] = {True : '#F54343', False : 'lightblue'}[checked[node]]
        if residual:
            self.plot_residual_graph(colors)
        else:
            self.plot_flow(colors)
    
    def find_augmenting_path(self):
        """Return an augmenting path in the residual graph and delta"""
        self.label()
        j = 't'
        flowpath = []
        while j != 's':
            i = self.G.nodes[j]["prev"]
            flowpath.insert( 0, (i,j) )
            j = i
        delta = math.inf
        for i, j in flowpath:
            delta = min( delta, self.residual.edges[i,j]['residual capacity'] )
        return flowpath, delta

    def update_flow(self, flowpath, delta):
        """Update the flow using the given flowpath and delta."""
        for i, j in flowpath:
            if self.residual.edges[i,j]['forward edge']:
                self.G.edges[i,j]['flow'] = self.G.edges[i,j]['flow'] + delta
            else:
                self.G.edges[j,i]['flow'] = self.G.edges[j,i]['flow'] - delta

    def ford_fulkerson(self, show=False):
        """Run all of Ford Fulkerson on this max flow insance."""
        self.set_initial_flow()
        if show:
            self.plot_residual_graph()
        else:
            self.create_residual_graph()
        self.label()  # run the labeling algorithm to find a s-t path in the residual graph
        while self.G.nodes['t']["check"]: # while there is an s-t path in the residual graph
            path, delta = self.find_augmenting_path()
            self.update_flow(path, delta)  # update the flow
            if show:
                self.plot_residual_graph()
            else:
                self.create_residual_graph()
            self.label()  # run the labeling algorithm to find a s-t path in the new residual graph

def add_infinite_capacities(G):
    for i,j in G.edges:
        if 'capacity' in G.edges[i,j]:
            G.edges[i,j]['cap'] = G.edges[i,j]['capacity']
        else:
            G.edges[i,j]['cap'] = math.inf
    return G