import matplotlib.pyplot as plt
import networkx as nx
import math

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
        self.labels = nx.get_node_attributes(self.G, 'label')

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
            nx.draw_networkx(self.G,self.pos,node_size=500,node_color='lightblue', labels=self.labels, with_labels=True)
        else:
            colors = [colors[i] for i in self.G.nodes]
            nx.draw_networkx(self.G,self.pos,node_size=500,node_color=colors, labels=self.labels, with_labels=True)
        nx.draw_networkx_edge_labels(self.G,self.pos,edge_labels=label);
        plt.show()

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
            nx.draw_networkx(self.residual,self.pos,node_size=500,node_color='lightblue',connectionstyle='arc3, rad=0.1', labels=self.labels, with_labels=True)
        else:
            colors = [colors[i] for i in self.residual.nodes]
            nx.draw_networkx(self.residual,self.pos,node_size=500,node_color=colors,connectionstyle='arc3, rad=0.1', labels=self.labels, with_labels=True)
        residualcap = nx.get_edge_attributes( self.residual, 'residual capacity' )
        nx.draw_networkx_edge_labels(self.residual,self.pos,edge_labels=residualcap,label_pos=0.66);
        plt.show()

    def label(self, s='s', auto=True, show=False):
        """Label and check nodes."""
        for i in self.G.nodes:
            self.G.nodes[i]["check"] = False
        self.G.nodes[s]["check"] = True
        unexplored = {s}
        if show:
            self.plot_checked(residual=True)
        while len(unexplored) > 0:
            if not auto:
                print('Unexplored nodes:',unexplored)
                nxt = int(input('Choose next node to explore: '))
                if nxt not in unexplored:
                    raise ValueError('Node not in the list of unexplored nodes.')
                i = nxt
                unexplored.remove(i)
            else:
                i = unexplored.pop()

            neighbors = list(self.residual.neighbors(i))
            if show:
                print("Looking at node '%s'. Its neighbors are %s."%(i,str(neighbors)))
            for j in neighbors:
                if not self.G.nodes[j]["check"]:
                    self.G.nodes[j]["check"] = True
                    self.G.nodes[j]["prev"] = i
                    unexplored.add(j)
                    if show:
                        print("Node '%s' now checked and prev set to '%s'."%(j,i))
                else:
                    if show:
                        print("Node '%s' already checked."%(j))
            if show:
                self.plot_checked(residual=True)

    def plot_checked(self, residual=False):
        """Plot the graph with checked nodes marked."""
        checked = nx.get_node_attributes(self.G,'check')
        colors = {}
        for node in checked:
            colors[node] = {True : '#F54343', False : 'lightblue'}[checked[node]]
        if residual:
            self.plot_residual_graph(colors)
        else:
            self.plot_flow(colors)

    def find_augmenting_path(self, s='s', t='t'):
        """Return an augmenting path in the residual graph and delta"""
        self.label(s=s)
        j = t
        flowpath = []
        while j != s:
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

    def ford_fulkerson(self, s='s', t='t', show=False):
        """Run all of Ford Fulkerson on this max flow instance."""
        self.set_initial_flow()
        if show:
            self.plot_residual_graph()
        else:
            self.create_residual_graph()
        self.label(s=s)  # run the labeling algorithm to find a s-t path in the residual graph
        while self.G.nodes[t]["check"]: # while there is an s-t path in the residual graph
            path, delta = self.find_augmenting_path(s=s, t=t)
            self.update_flow(path, delta)  # update the flow
            if show:
                self.plot_residual_graph()
            else:
                self.create_residual_graph()
            self.label(s=s)  # run the labeling algorithm to find a s-t path in the new residual graph

    def get_flow_value(self, t = 't'):
        """Returns the value of the current flow."""
        flow = 0
        for i,j in self.G.edges:
            if j == t:
                flow += self.G.edges[i,j]['flow']
        return flow

    def get_checked_nodes(self):
        """Returns a list of the nodes that are on the s-side of the min cut, using their labels."""
        checked = []
        for i in self.G.nodes:
            if self.G.nodes[i]["check"]:
                checked.append(self.G.nodes[i]['label'])
        return checked


def add_infinite_capacities(G):
    """Add infinite capacities on the arcs with no capacity given."""
    for i,j in G.edges:
        if 'capacity' in G.edges[i,j]:
            G.edges[i,j]['cap'] = G.edges[i,j]['capacity']
        else:
            G.edges[i,j]['cap'] = math.inf
    return G

def max_density(G, edges, d):
    """Formulate and solve the min cut instance of the maximum density problem with the given graph [G], graph edges [edges] and given density [d]."""
    dirG = nx.DiGraph()
    sink_edges = []
    #sink will be node 0
    t=0
    labels = {t: 't'}
    #add vertex nodes
    for i in range(1, G.number_of_nodes()+1):
        sink_edges.append((i, t, d))
        labels[i] = str(i)
    source_edges = []
    #edge to vertex edges
    etv_edges = []
    #source will be node (num of vertices + 1)
    s = G.number_of_nodes()+1
    labels[s] = 's'
    count = s+1
    #total number of edges in the original graph that are not self loops
    total_edges = 0
    for e in edges:
        if e[0] != e[1]:
            source_edges.append((s,count, 1))
            etv_edges.append((count, e[0], math.inf))
            etv_edges.append((count, e[1], math.inf))
            labels[count] = str(e)
            count += 1
            total_edges += 1
    dirG.add_weighted_edges_from(sink_edges, 'cap' )
    dirG.add_weighted_edges_from(source_edges, 'cap' )
    dirG.add_weighted_edges_from(etv_edges, 'cap' )
    #assign labels to nodes
    for k in labels:
        dirG.nodes[k]['label'] = labels[k]
    #assign positions to nodes
    for i in range(1, G.number_of_nodes()+1):
        dirG.nodes[i]['pos'] = (40, 100-i*10)
    #last node index in the graph (index of last edge node)
    edge_length = s+1+total_edges
    for i in range(s+1, edge_length):
        dirG.nodes[i]['pos'] = (20, 100-(i-(s+1))*10)
    dirG.nodes[t]['pos'] = (60, edge_length*10//2)
    dirG.nodes[s]['pos'] = (0, edge_length*10//2)

    #solve the min cut instance
    ex= max_flow(dirG)
    ex.ford_fulkerson(s=s, t=t, show=False)
    print("Max flow value: " + str(ex.get_flow_value(t=t)))
    ex.plot_flow()
    ex.label(s=s, auto=True, show=False)
    print("Minimum s-t cut: " + str(ex.get_checked_nodes()))
    ex.plot_checked(residual=True)
