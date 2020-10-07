from ortools.graph import pywrapgraph
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
from bokeh import palettes
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models import (GraphRenderer, Circle, MultiLine, StaticLayoutProvider,
                          HoverTool, TapTool, EdgesAndLinkedNodes, NodesAndLinkedEdges,
                          ColumnDataSource, LabelSet, NodesOnly
                         )
# from gurobipy import *

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
        self.arcs_in = dict()
        self.arcs_out = dict()
        self.arcs = list()
        self.start_nodes = list()
        self.end_nodes = list()
        self.capacities = list()
        self.costs = list()
        self.objective = 0
        self.flow = dict()
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
        
        for node in range(i+1):
            self.arcs_in[node] = []
            self.arcs_out[node] = []
                    
        def add_arc(tail, head, cap, cost, trip_arc=False):
            """Add arc from tail to head with given capacity and cost"""
            i = self.nodes[tail]
            j = self.nodes[head]
            self.arcs.append((i,j,trip_arc))
            self.arcs_in[j].append((i,j,trip_arc))
            self.arcs_out[i].append((i,j,trip_arc))
            self.start_nodes.append(i)
            self.end_nodes.append(j)
            self.capacities.append(cap)
            self.costs.append(cost)
            self.flow[(i,j,trip_arc)] = 0  # zero flow intially
        
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
            add_arc((s,s_t),(t,t_t),1,-row['value'], index)   
            
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
        
        supplies = [0]*len(self.nodes)
        supplies[0] = self.B_max
        supplies[-1] = -self.B_max
        
        # OR-Tools
        self.model = pywrapgraph.SimpleMinCostFlow()
        for i in range(0, len(self.start_nodes)):
            self.model.AddArcWithCapacityAndUnitCost(self.start_nodes[i], 
                                                     self.end_nodes[i],
                                                     self.capacities[i], 
                                                     int(self.costs[i]))
        for i in range(0, len(supplies)):
            self.model.SetNodeSupply(i, supplies[i])
            
#         # Gurobi
#         self.model = Model('min-cost_flow')
#         self.model_flow = self.model.addVars(self.arcs, lb=0.0, obj=self.costs, name='flow')
        
#         # Capacity constraint
#         for i in range(len(self.arcs)):
#             self.model.addConstr(self.model_flow[self.arcs[i]], 
#                                  GRB.LESS_EQUAL, 
#                                  self.capacities[i], 
#                                  "cap_(%s,%s,%s)"%self.arcs[i])
        
#         # flow conservation
#         self.model.addConstrs((self.model_flow.sum(j,'*') 
#                                - self.model_flow.sum('*',j) 
#                                == supplies[j] for j in range(len(self.nodes))), "node")
        
#         # set objective
#         self.model.modelSense = GRB.MINIMIZE
            
    def optimize(self):   
        """Optimize this taxi routing problem and set the flows and objective value."""
        # OR-Tools
        if self.model.Solve() != self.model.OPTIMAL:
            print('Something went wrong.')  
        self.objective = -self.model.OptimalCost()
        for i in range(len(self.arcs)):
            self.flow[self.arcs[i]] = self.model.Flow(i)
            
#         # Gurobi
#         self.model.optimize()
#         self.objective = -self.model.objVal
#         for arc in self.arcs:
#              self.flow[arc] = int(self.model_flow[arc].x)
            
    def compute_taxi_stats(self):
        """"Compute the statisitcs for this solution."""
        taxi_arcs = []
        tmp_flow = self.flow.copy()
        node_map = {v: k for k, v in self.nodes.items()}
        source = self.nodes['source']
        sink = self.nodes['sink']
        for taxi in range(self.B_max):
            taxi_arc = []
            i = source
            while not i == sink:
                arcs_out = self.arcs_out[i]
                for arc in arcs_out:
                    if tmp_flow[arc] > 0:
                        tmp_flow[arc] = tmp_flow[arc] - 1
                        start_node = node_map[arc[0]]
                        end_node = node_map[arc[1]]
                        if start_node != 'source' and end_node != 'sink':
                            moving = (start_node[0] != end_node[0])
                            time = end_node[1] - start_node[1]
                            trip_arc = arc[2] if type(arc[2]) is bool else True
                            taxi_arc.append((time,moving,trip_arc,arc[2]))
                        i = arc[1]
                        break
            taxi_arcs.append(taxi_arc)

        taxi_stats = []
        for arcs in taxi_arcs:
            unzipped = list(zip(*arcs))
            total_time = sum(np.array(unzipped[0]))
            moving_time = sum(np.array(unzipped[0])[list(unzipped[1])])
            trip_time = sum(np.array(unzipped[0])[list(unzipped[2])])

            trip_IDs = list(np.array(unzipped[3])[list(unzipped[2])])
            num_trips = len(trip_IDs)
            trips = self.trips_df.loc[trip_IDs]
            total_trip_distance = sum(trips['trip_distance'])
            total_passengers = sum(trips['passenger_count'])
            revenue = sum(trips['value'])/100


            taxi_stats.append({'moving_pct' : moving_time/total_time,
                               'on_trip_pct' : trip_time/total_time,
                               'num_trips' : num_trips,
                               'total_trip_distance' : total_trip_distance,
                               'total_passengers' : total_passengers,
                               'revenue' : revenue})
            
        self.taxi_stats = taxi_stats    
        self.avg_moving_pct = sum([stat['moving_pct'] for stat in taxi_stats])/self.B_max
        self.avg_trip_pct = sum([stat['on_trip_pct'] for stat in taxi_stats])/self.B_max
        self.avg_num_trips = sum([stat['num_trips'] for stat in taxi_stats])/self.B_max
        self.avg_total_trip_distance = sum([stat['total_trip_distance'] for stat in taxi_stats])/self.B_max
        self.total_passengers = sum([stat['total_passengers'] for stat in taxi_stats])
        self.avg_revenue = sum([stat['revenue'] for stat in taxi_stats])/self.B_max

    def get_stats(self):
        """Return the summary stats for this solution."""
        self.compute_taxi_stats()
        
        print('Summary Statistics')
        print('Avg. Moving Pct.: ',self.avg_moving_pct)
        print('Avg. On Trip Pct.: ',self.avg_trip_pct)
        print('Avg. Total Distance of Trips: ',self.avg_total_trip_distance)
        print('Total Passengers: ',self.total_passengers)
        print('Avg. Revenue: ',self.avg_revenue)
        
    
    def taxi_paths(self):
        """Returns a list of arcs travelled and indication if they were a trip arc for each taxi."""
        taxi_paths = []
        tmp_flow = self.flow.copy()
        node_map = {v: k for k, v in self.nodes.items()}
        source = self.nodes['source']
        sink = self.nodes['sink']
        for taxi in range(self.B_max):
            path = []
            i = source
            while not i == sink:
                arcs_out = self.arcs_out[i]
                for arc in arcs_out:
                    if tmp_flow[arc] > 0:
                        tmp_flow[arc] = tmp_flow[arc] - 1
                        is_trip_arc = arc[2] if type(arc[2]) is bool else True
                        path.append((node_map[arc[0]][0],node_map[arc[1]][0],is_trip_arc))
                        i = arc[1]
                        break
            taxi_paths.append(path[1:-1])
        return taxi_paths
     
      # TODO: Implement a method to get locations of taxis at each time interval
#     def taxi_locations(self):
#         taxi_paths = self.taxi_paths()
#         taxi_time_dict = []
#         for taxi in range(self.B_max):
#             locations, times = list(zip(*taxi_paths[taxi]))
#             time_dict = {}
#             for i in range(len(times)):
#                 time_dict[times[i]] = locations[i]
#                 if i < len(times) - 1:
#                     for t in range(times[i+1]-times[i]-1):
#                         time_dict[times[i]+t+1] = (locations[i],locations[i+1])
#             taxi_time_dict.append(time_dict)
#         return taxi_time_dict
            
    def draw_graph(self):  
        """Draw the min-cost flow graph for this problem."""
        G = nx.DiGraph()
        edgeList = []
        for i in range(len(self.start_nodes)):
            edgeList.append((self.start_nodes[i], 
                             self.end_nodes[i], 
                             self.capacities[i]))
        G.add_weighted_edges_from(edgeList, 'cap')  
                
        for (i,j,trip_arc) in self.arcs:
            G.edges[(i,j)]['flow'] = self.flow[(i,j,trip_arc)]
        
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
        
    def plot_taxi_route(self, taxis):
        """Plot the path of every taxi in the given list on the Manhattan grid."""
        paths = self.taxi_paths()  # get paths
        
        # parallel lists for every arc
        start = []  # start node
        end = []  # end node
        color = []  # color code by taxi
        alpha = []  # opacity lower on trip arcs
        
        # parallel lists for initial location nodes
        start_nodes = []
        start_colors = []
        
        colors = palettes.Category10[10]
        c = 0
        
        for i in taxis:
            path = paths[i]
            
            # add start node information for this taxi
            start_nodes.append(path[0][0])
            start_colors.append(colors[c])
            
            for comp in path:
                start.append(comp[0])
                end.append(comp[1])
                alpha.append({True : 0.3, False : 1}[comp[2]])
                color.append(colors[c])
                
            c = c + 1 if c < len(colors)-1 else 0

        # parallel lists for nodes
        nodes = self.nodes_df.loc[list(set(start + end))]
        node_ids = nodes.name.values.tolist()
        x = nodes.x.values.tolist()
        y = nodes.y.values.tolist()

        # get plot boundaries
        min_x, max_x = min(nodes.x)-1000, max(nodes.x)+1000
        min_y, max_y = min(nodes.y)-1000, max(nodes.y)+1000

        plot = figure(x_range=(min_x, max_x), y_range=(min_y, max_y),
                      x_axis_type="mercator", y_axis_type="mercator",
                      title='Taxi Routes', plot_width=600, plot_height=470)
        plot.add_tile(get_provider(Vendors.CARTODBPOSITRON_RETINA))

        graph = GraphRenderer()

        # define initial location nodes
        graph.node_renderer.data_source.add(start_nodes, 'index')
        graph.node_renderer.data_source.add(start_colors, 'start_colors')
        graph.node_renderer.glyph = Circle(size=7,line_width=0,fill_alpha=1, fill_color='start_colors')

         # define network edges
        graph.edge_renderer.data_source.data = dict(start=list(start),
                                                    end=list(end),
                                                    color=list(color),
                                                    alpha=list(alpha))
        graph.edge_renderer.glyph = MultiLine(line_color='color', line_alpha='alpha',
                                             line_width=3,line_cap='round')

        # set node locations
        graph_layout = dict(zip(node_ids, zip(x, y)))
        graph.layout_provider = StaticLayoutProvider(graph_layout=graph_layout)
        
        plot.renderers.append(graph)
        show(plot)
        
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
    trips_df = trips_df.reset_index().drop(columns='index')

    nodes_df = pd.DataFrame(columns=['name'])
    for i in range(L):
        row = {}
        row['name'] = i
        nodes_df = nodes_df.append(pd.DataFrame(row, index=[0]))
    nodes_df = nodes_df.reset_index().drop(columns='index')

    arcs_df = pd.DataFrame(columns=['start', 'end', 'trip_time'])
    for arc in arcs:
        row = {}
        row['start'] = arc[0]
        row['end'] = arc[1]
        row['trip_time'] = arc[2]
        arcs_df = arcs_df.append(pd.DataFrame(row, index=[0]))
    arcs_df = arcs_df.reset_index().drop(columns='index')
    return trips_df, nodes_df, arcs_df    