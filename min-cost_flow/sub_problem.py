from utility_functions import *
from ortools.graph import pywrapgraph
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

class BikeRouting(object):
    """docstring for BikeRouting"""
    def __init__(self, problem):
        # Problem Parameters
        self.num_bikes = problem.num_bikes
        self.locations = problem.locations
        self.T_max = problem.T_max
        self.B_max = problem.B_max
        self.trips = problem.trips
        self.capacity = problem.capacity

        # Other variables
        self.model = None
        self.arcs = None
        self.arc_names = None
        self.flow = dict()
        self.solution = None
        self.constrs = None
        self.objective = None
        self.arcs_entering = dict()
        self.arcs_leaving = dict()
        self.all_trip_arcs = list()

        self.flow_constrs = None
        self.recharge_arcs = dict()
        self.recharge_constrs = dict()
        self.trip_constrs = list()
        self.recharge_stations = list()

        self.setup_network()


    def setup_network(self):
        # Generate list of all nodes
        self.nodes = list()
        # Source Node
        self.nodes.append('source')
        
        print('start')
        # Location, Time
        for location in self.locations:
            for time in range(self.T_max + 1):
                self.nodes.append(node_name(location, time))
        # Sink Node
        self.nodes.append('sink')
              
        print('finish')

        for node in self.nodes:
            self.arcs_entering[node] = list()
            self.arcs_leaving[node] = list()

        # Genearate all arcs
        self.arcs = list()
        capacity = list()
        obj = list()
        self.arc_names = list()

        # Bike Source Arcs
        for j in self.locations:
            self.arcs.append(('source', node_name(j,0)))
            capacity.append(self.num_bikes)
            obj.append(0)
            self.arc_names.append('allocation_' + node_name(j,0))

        # Bikes to sink
        for location in self.locations:
            self.arcs.append((node_name(location,self.T_max), 'sink'))
            capacity.append(self.num_bikes)
            obj.append(0)
            self.arc_names.append('collection_'+node_name(location,self.T_max))

        # Stay arcs (bikes not rented)
        for location in self.locations:
            for time in range(self.T_max):
                self.arcs.append((node_name(location, time), node_name(location, time+1)))
                capacity.append(self.num_bikes)
                obj.append(0)
                self.arc_names.append('stay_'+node_name(location, time))

        # Customer trips
        all_trips_cap = list()
        for index, trip in enumerate(self.trips):
            # manually set this for now
            if False:
                epsilon = np.random.uniform()/100000
            else:
                epsilon = 0
            self.arcs.append((node_name(trip.start, trip.start_time), 
                              node_name(trip.end, trip.end_time)))
            capacity.append(trip.capacity)
            obj.append((-1+epsilon)*trip.value)
            self.arc_names.append('Customer_trip_num_'+str(index))
            self.all_trip_arcs.append([(node_name(trip.start, trip.start_time), 
                                        node_name(trip.end, trip.end_time))])
            all_trips_cap.append(trip.capacity)


        dictionary = {}
        for i in range(len(self.arcs)):
            dictionary[self.arcs[i]] = [capacity[i], obj[i], self.arc_names[i]]
            self.flow[self.arcs[i]] = 0

        self.arcs, capacity, obj, self.arc_names = multidict(dictionary)

        inflow = {}
        for node in self.nodes:
            if 'source' == node:
                inflow[node] = self.num_bikes
            elif 'sink' == node:
                inflow[node] = -1*self.num_bikes
            else:
                inflow[node] = 0
                
        # Create a dictionary from node names to node indices
        self.nodes_to_index = {}
        for i in range(len(self.nodes)):
            self.nodes_to_index[self.nodes[i]] = i
            
        print('define input for making ortools network.')
                    
        # Define four parallel arrays: start_nodes, end_nodes, capacities, and unit costs
        self.start_nodes = []
        self.end_nodes   = []
        self.capacities  = []
        self.unit_costs  = []
        for arc in self.arcs:
            self.start_nodes.append(self.nodes_to_index[arc[0]])
            self.end_nodes.append(self.nodes_to_index[arc[1]])
            self.capacities.append(capacity[arc])
            self.unit_costs.append(obj[arc])
            
        # Define an array of supplies at each node.
        supplies = list(inflow.values())
        
        # DEFINE NETWORK FOR ORTOOLS
        
        print('making ortools network.')
            
        # Instantiate a SimpleMinCostFlow solver.
        self.model = pywrapgraph.SimpleMinCostFlow()

        # Add each arc.
        for i in range(0, len(self.start_nodes)):
            self.model.AddArcWithCapacityAndUnitCost(self.start_nodes[i], 
                                                     self.end_nodes[i],
                                                     self.capacities[i], 
                                                     self.unit_costs[i])

        # Add node supplies.
        for i in range(0, len(supplies)):
            self.model.SetNodeSupply(i, supplies[i])
            
        print('finished making ortools network.')
            
    
    def draw_graph(self):  
        
        G = nx.DiGraph()
        edgeList = []
        for i in range(len(self.arcs)):
            edgeList.append((self.start_nodes[i], 
                             self.end_nodes[i], 
                             self.capacities[i]))
        G.add_weighted_edges_from(edgeList, 'cap')   
        for i, j in G.edges:
            tail = self.nodes[i]
            head = self.nodes[j]
            G.edges[i,j]['flow'] = self.flow[tail,head]
        
        loc_pos = list(np.linspace(0,1,2+len(self.locations))[1:-1])
        loc_pos.reverse()
        time_pos = np.linspace(0,1,2+self.T_max+1)[1:-1]
        
        pos = [(0,0.5)]
        for i in range(len(self.locations)):
            for j in range(self.T_max+1):
                pos.append((time_pos[j],loc_pos[i]))      
        pos.append((1,0.5))
        plt.figure(3,figsize=(9,6)) 
        nx.draw_networkx(G,pos,node_size=500,node_color='lightblue')
        nx.draw_networkx_edge_labels(G,pos,edge_labels=nx.get_edge_attributes(G,'flow'));
              
       
    def optimize(self):
        if self.model.Solve() != self.model.OPTIMAL:
            print('Something went wrong.')
        self.objective = -self.model.OptimalCost()
        
        # Update flow 
        for i in range(len(self.arcs)):
            self.flow[self.arcs[i]] = self.model.Flow(i)
        
#         self.get_solution()

    def get_solution(self):
        # TODO: Need to implement this
        self.solution = self.model.getAttr('x', self.flow)
        if self.verbose:
            for i,j in self.arcs:
                if self.solution[i,j] > 0:
                    print(i,j, self.solution[i,j])

