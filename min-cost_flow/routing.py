from ortools.graph import pywrapgraph
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd

class TaxiRouting(object):
    """Maintain a min-cost representation of NYC taxi routing problem."""
    
    def __init__(self, trips, nodes, arcs, start_time, end_time, taxi_count):
        """Create the min-cost representation of this instance.
        
        Args:
            trips (DataFrame): A dataframe containing all trips.
            nodes (DataFrame): A dataframe containing all locations.
            arcs (DataFrame): A dataframe containing travel times between locations.
            start_time (float): Starting hour of interest.
            end_time (float): Ending hour of interest.
            taxi_count (int): The number of taxis to service rides.
        """
        #Set dataframes
        self.nodes_df = nodes
        self.arcs_df = arcs

        # Filter trips by time window of interest
        trips = trips[(trips.start_time >= start_time) & 
                      (trips.start_time + trips.trip_time <= end_time)].copy()
        trips.start_time = trips.start_time - start_time
        self.trips_df = trips

        self.L = len(self.nodes_df)
        self.T_max = int(end_time - start_time)
        self.B_max = taxi_count
        
        self.nodes = dict()
        self.arcs = list()
        self.start_nodes = list()
        self.end_nodes = list()
        self.capacities = list()
        self.costs = list()
        self.objective = 0
        self.flow = list()
        self.model = None
        
        self.setup_network()
        self.load_model()      
    
    def setup_network(self):
        """Create the network for this taxi routing instance."""  
        # source node
        self.nodes['source'] = 0
        
        # location x time nodes
        i = 1
        for l in range(self.L):
            for t in range(self.T_max+1):
                self.nodes[(l,t)] = i
                i += 1
        
        # sink node
        self.nodes['sink'] = i
                    
        def add_arc(tail, head, cap, cost):
            """Add arc from tail to head with given capacity and cost"""
            i = self.nodes[tail]
            j = self.nodes[head]
            self.arcs.append((i,j))
            self.start_nodes.append(i)
            self.end_nodes.append(j)
            self.capacities.append(cap)
            self.costs.append(cost)
            self.flow.append(0)  # zero flow intially
        
        # Taxi source arcs
        for j in range(self.L):
            add_arc('source',(j,0),self.B_max,0)
            
        # Taxi sink arcs
        for j in range(self.L):
            add_arc((j,self.T_max),'sink',self.B_max,0)
            
        # Stay in location arcs
        for j in range(self.L):
            for t in range(self.T_max):
                add_arc((j,t),(j,t+1),self.B_max,0)
                
        # Customer trips
        for index, row in self.trips_df.iterrows():
            s = row['start_node']
            t = row['end_node']
            s_t = row['start_time']
            t_t = s_t + row['trip_time']
            add_arc((s,s_t),(t,t_t),1,-row['value'])   
            
        # Movement (non-trip) arcs
        for index, row in self.arcs_df.iterrows():
            for t in range(self.T_max):
                i = row['start']
                j = row['end']
                delay = row['trip_time']
                if t + delay <= self.T_max:
                    add_arc((i,t),(j,t+delay),self.B_max,0)     
            
    def load_model(self):
        """Load the network into the model."""  
        self.model = pywrapgraph.SimpleMinCostFlow()
        for i in range(0, len(self.start_nodes)):
            self.model.AddArcWithCapacityAndUnitCost(self.start_nodes[i], 
                                                     self.end_nodes[i],
                                                     self.capacities[i], 
                                                     int(self.costs[i]))
        supplies = [0]*len(self.nodes)
        supplies[0] = self.B_max
        supplies[-1] = -self.B_max
        for i in range(0, len(supplies)):
            self.model.SetNodeSupply(i, supplies[i])
            
    def optimize(self):
        if self.model.Solve() != self.model.OPTIMAL:
            print('Something went wrong.')
        self.objective = -self.model.OptimalCost()
        for i in range(len(self.arcs)):
            self.flow[i] = self.model.Flow(i)
            
    def draw_graph(self):  
        
        G = nx.DiGraph()
        edgeList = []
        for i in range(len(self.start_nodes)):
            edgeList.append((self.start_nodes[i], 
                             self.end_nodes[i], 
                             self.capacities[i]))
        G.add_weighted_edges_from(edgeList, 'cap')  
                
        for i in range(len(self.arcs)):
            G.edges[self.arcs[i][0], self.arcs[i][1]]['flow'] = self.flow[i]
        
        loc_pos = list(np.linspace(0,1,2+self.L)[1:-1])
        loc_pos.reverse()
        time_pos = np.linspace(0,1,2+self.T_max+1)[1:-1]
        
        pos = [(0,0.5)]
        for i in range(self.L):
            for j in range(self.T_max+1):
                pos.append((time_pos[j],loc_pos[i]))      
        pos.append((1,0.5))
        plt.figure(3,figsize=(9,6)) 
        nx.draw_networkx(G,pos,node_size=500,node_color='lightblue')
        nx.draw_networkx_edge_labels(G,pos,edge_labels=nx.get_edge_attributes(G,'flow'));
        
def create_dataframes(trips, arcs, L):
    """Create input dataframes.
    
    Args:
        trips (List[Tuple]): (start, end, start_time, trip_time, value) representing trip
        arcs (List[Tuple]): (start, end, trip_time) representing arc
        L (int): Number of locations
    """
    
    trips_df = pd.DataFrame(columns=['start_node', 'end_node', 'start_time', 'trip_time', 'value'])
    for trip in trips:
        row = {}
        row['start_node'] = trip[0]
        row['end_node'] = trip[1]
        row['start_time'] = trip[2]
        row['trip_time'] = trip[3]
        row['value'] = trip[4]
        trips_df = trips_df.append(pd.DataFrame(row, index=[0]))

    nodes_df = pd.DataFrame(columns=['name'])
    for i in range(L):
        row = {}
        row['name'] = i
        nodes_df = nodes_df.append(pd.DataFrame(row, index=[0]))

    arcs_df = pd.DataFrame(columns=['start', 'end', 'trip_time'])
    for arc in arcs:
        row = {}
        row['start'] = arc[0]
        row['end'] = arc[1]
        row['trip_time'] = arc[2]
        arcs_df = arcs_df.append(pd.DataFrame(row, index=[0]))
    return trips_df, nodes_df, arcs_df    