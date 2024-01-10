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
                          ColumnDataSource, LabelSet, NodesOnly)

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
        # dataframes
        self.nodes_df = nodes
        self.arcs_df = arcs

        # filter trips by time window of interest
        trips = trips[(trips.start_time >= start_time) & 
                      (trips.start_time + trips.trip_time <= end_time)].copy()
        trips.start_time = trips.start_time - start_time
        self.trips_df = trips

        # instance variables
        self.L = len(self.nodes_df)
        self.T_max = int(end_time - start_time)
        self.B_max = taxi_count
        
        self.nodes = list()
        self.node_to_index = dict()
        self.arcs = list()
        self.arcs_out = dict()
        self.objective = 0
        self.unit_flows = list()
        self.model = None
        
        self.setup_network()
        self.load_model()      
    
    def setup_network(self):
        """Create the network for this taxi routing instance.""" 
        
        # nodes
        self.nodes.append('s')
        for l in range(self.L):
            for t in range(self.T_max+1):
                self.nodes.append((l,t))
        self.nodes.append('f')
        self.node_to_index = {self.nodes[i] : i for i in range(len(self.nodes))} 
        
        for node in range(len(self.nodes)):
            self.arcs_out[node] = []
                    
        def add_arc(tail, head, cap, cost, trip_arc=False):
            tail = self.node_to_index[tail]
            head = self.node_to_index[head]
            self.arcs.append({'tail' : tail, 
                              'head' : head, 
                              'trip' : trip_arc,
                              'cap' : cap, 
                              'cost' : cost, 
                              'flow' : 0})
            self.arcs_out[tail].append(len(self.arcs)-1)
        
        # source and sink arcs
        for j in range(self.L):
            add_arc('s',(j,0),self.B_max,0) # source
            add_arc((j,self.T_max),'f',self.B_max,0) # sink
        
        # static arcs
        for j in range(self.L):
            for t in range(self.T_max):
                add_arc((j,t),(j,t+1),self.B_max,0)
        
        # trips
        for index, row in self.trips_df.iterrows():
            s = row['start_node']
            t = row['end_node']
            s_t = row['start_time']
            t_t = s_t + row['trip_time']
            add_arc((s,s_t),(t,t_t),1,-row['value'], index)   
        
        # movement (non-trip) arcs
        for index, row in self.arcs_df.iterrows():
            i = row['start']
            j = row['end']
            delay = row['trip_time']
            for t in range(self.T_max + 1 - delay):
                add_arc((i,t),(j,t+delay),self.B_max,0)  
        
        self.arcs = pd.DataFrame(self.arcs)
        
    def load_model(self):
        """Load the network into the model."""  
        self.model = pywrapgraph.SimpleMinCostFlow()
        
        # arcs
        tails = list(self.arcs['tail'])
        heads = list(self.arcs['head'])
        caps = list(self.arcs['cap'])
        costs = list((self.arcs['cost']*100).astype(int))
        
        for i in range(len(tails)):
            self.model.AddArcWithCapacityAndUnitCost(tails[i], heads[i], caps[i], costs[i])
        
        # nodes
        supplies = [0]*len(self.nodes)
        supplies[0] = self.B_max
        supplies[-1] = -self.B_max
        
        for i in range(0, len(supplies)):
            self.model.SetNodeSupply(i, supplies[i])
            
        # NOTE: Gurobi implemention removed in commit #168
        # -> It is slower than OR-Tool's min-cost flow specific solver
            
    def optimize(self):   
        """Optimize this taxi routing problem and set the flows and objective value."""
        if self.model.Solve() != self.model.OPTIMAL:
            print('Something went wrong.')  
        self.objective = -self.model.OptimalCost()/100
        for i in range(len(self.arcs)):
            self.arcs.at[i,'flow'] = self.model.Flow(i)  
        self.unit_flows = self.decompose_flow()
        self.compute_taxi_stats()    
            
        # NOTE: Gurobi implemention removed in commit #168
        # -> It is slower than OR-Tool's min-cost flow specific solver
    
    def decompose_flow(self):
        """Decompose the current flow into unit flows."""
        paths = []
        tmp_flow = self.arcs['flow'].to_dict().copy()
        source = self.node_to_index['s']
        sink = self.node_to_index['f']
        for unit_flow in range(self.B_max):
            path = []
            i = source
            while not i == sink:
                index = [i for i in self.arcs_out[i] if tmp_flow[i] > 0][0]
                i = self.arcs.at[index, 'head']
                tmp_flow[index] = tmp_flow[index] - 1
                path.append(index)
            paths.append(path[1:-1])
        return paths  
    
    def compute_taxi_stats(self):
        """Compute the statisitcs for this solution."""
        paths = []
        for unit_flow in self.unit_flows:
            path = []
            for arc_index in unit_flow:
                arc = self.arcs.loc[arc_index]
                trip_arc = arc['trip'] if type(arc['trip']) is bool else True
                tail = self.nodes[arc['tail']]
                head = self.nodes[arc['head']]
                moving = (tail[0] != head[0])
                time = tail[1] - head[1]
                path.append((time,moving,trip_arc,arc['trip']))
            paths.append(path)

        taxi_stats = []
        for path in paths:
            unzipped = list(zip(*path))
            total_time = sum(np.array(unzipped[0]))
            moving_time = sum(np.array(unzipped[0])[list(unzipped[1])])
            trip_time = sum(np.array(unzipped[0])[list(unzipped[2])])

            trip_IDs = list(np.array(unzipped[3])[list(unzipped[2])])
            num_trips = len(trip_IDs)
            trips = self.trips_df.loc[trip_IDs]
            
            total_trip_distance = None if any(trips['trip_distance'].isna()) else sum(trips['trip_distance'])
            total_passengers = None if any(trips['passenger_count'].isna()) else sum(trips['passenger_count'])
            revenue = None if any(trips['revenue'].isna()) else sum(trips['revenue'])

            taxi_stats.append({'moving_pct' : moving_time / total_time,
                               'on_trip_pct' : trip_time / total_time,
                               'num_trips' : num_trips,
                               'total_trip_distance' : total_trip_distance,
                               'total_passengers' : total_passengers,
                               'revenue' : revenue})
        self.taxi_stats = taxi_stats   
        
        # aggregate 
        self.avg_moving_pct = sum([stat['moving_pct'] for stat in taxi_stats]) / self.B_max
        self.avg_trip_pct = sum([stat['on_trip_pct'] for stat in taxi_stats]) / self.B_max
        self.total_num_trips = sum([stat['num_trips'] for stat in taxi_stats])
    
        trip_distance_list = [stat['total_trip_distance'] for stat in taxi_stats]
        passengers_list = [stat['total_passengers'] for stat in taxi_stats]
        revenue_list = [stat['revenue'] for stat in taxi_stats]
        
        self.avg_total_trip_distance = sum(trip_distance_list) / self.B_max if None not in trip_distance_list else None
        self.total_passengers = sum(passengers_list) if None not in passengers_list else None
        self.avg_revenue = sum(revenue_list) / self.B_max if None not in revenue_list else None
        self.total_revenue = sum(revenue_list) if None not in revenue_list else None

    def get_stats(self):
        """Return the summary stats for this solution."""        
        print('Summary Statistics')
        print('Avg. Moving Pct.: %.2f' % (self.avg_moving_pct))
        print('Avg. On Trip Pct.: %.2f' % (self.avg_trip_pct))
        if not self.avg_total_trip_distance is None:
            print('Avg. Total Distance of Trips: %.2f' % (self.avg_total_trip_distance))
        if not self.avg_revenue is None:
            print('Avg. Revenue: %.2f' % (self.avg_revenue))
        print('Total Trips: %.2f (%.2f)' % (self.total_num_trips, 
                                            self.total_num_trips / len(self.trips_df)))
        if not self.total_passengers is None:
            print('Total Passengers: %.2f (%.2f)' % (self.total_passengers, 
                                                     self.total_passengers / sum(self.trips_df.passenger_count)))
        if not self.total_revenue is None:
            print('Total Revenue: %.2f (%.2f)' % (self.total_revenue,
                                                  self.total_revenue / sum(self.trips_df.revenue)))
    
    def plot_stats(self):
        """Plot statistics using matplotlib."""        
        fig, axs = plt.subplots(2, 3, tight_layout=True, figsize=(20,10))

        def plot_histogram(stat, title, x_label, i, j):
            x = [i[stat] for i in self.taxi_stats]
            if None in x:
                return
            unique_vals = len(set(x))
            if unique_vals < 5:
                bins = unique_vals
            else:
                bins = int(max(5,min(20,unique_vals/2)))
            axs[i,j].hist(x, bins)
            axs[i,j].set_xlabel(x_label)
            axs[i,j].set_ylabel('Frequency')
            axs[i,j].set_title(title)

        plot_histogram(stat='moving_pct',
                       title='Histogram of Moving Percentage',
                       x_label='Percent of time a taxi was moving', i=0, j=0)

        plot_histogram(stat='on_trip_pct',
                       title='Histogram of On Trip Percentage',
                       x_label='Percent of time a taxi was on a trip', i=0, j=1)

        plot_histogram(stat='num_trips',
                       title='Histogram of Trips Accommodated',
                       x_label='Number of trips given', i=0, j=2)

        plot_histogram(stat='total_trip_distance',
                       title='Histogram of Trip Distance Travelled',
                       x_label='Total Trip Distance Travelled (km)', i=1, j=0)

        plot_histogram(stat='total_passengers',
                       title='Histogram of Passenger Count',
                       x_label='Number of Passengers', i=1, j=1)

        plot_histogram(stat='revenue',
                       title='Histogram of Revenue',
                       x_label='Revenue ($)', i=1, j=2)

        plt.show(fig)    
    
    def taxi_paths(self, indices=None):
        """Returns a list of arcs travelled and indication if they were a trip arc for each taxi."""
        if indices is None:
            indices = list(range(0, len(self.unit_flows)))
        unit_flows = [self.unit_flows[i] for i in indices]
            
        paths = []
        for unit_flow in unit_flows:
            path = []
            for arc_index in unit_flow:
                arc = self.arcs.loc[arc_index]
                path.append((self.nodes[arc['tail']][0],
                             self.nodes[arc['head']][0],
                             arc['trip'] if type(arc['trip']) is bool else True))
            paths.append(path)
        return paths
     
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
            
    def draw_graph(self, draw_all=True):  
        """Draw the min-cost flow graph for this problem."""
        G = nx.DiGraph()
        edgeList = []
        for index, row in self.arcs.iterrows():
            if not draw_all and not row['trip'] and row['flow'] == 0:
                continue
            edgeList.append((row['tail'], 
                             row['head'], 
                             row['flow']))
        G.add_weighted_edges_from(edgeList, 'flow')  
        G.add_nodes_from(list(range(len(self.nodes))))
        
        loc_pos = list(np.linspace(0,1,2+self.L)[1:-1])
        loc_pos.reverse()
        time_pos = np.linspace(0,1,2+self.T_max+1)[1:-1]
        
        pos = [(0,0.5)]
        for i in range(self.L):
            for j in range(self.T_max+1):
                pos.append((time_pos[j],loc_pos[i]))      
        pos.append((1,0.5))
        plt.figure(3,figsize=(9,6)) 
        
        labels = {i: self.nodes[i] for i in range(len(self.nodes))}        
        nx.draw_networkx(G,pos,labels=labels,node_size=1200,node_color='lightblue')
        nx.draw_networkx_edge_labels(G,pos,edge_labels=nx.get_edge_attributes(G,'flow'));
        
    def plot_taxi_route(self, taxis):
        """Plot the path of every taxi in the given list on the Manhattan grid."""
        paths = self.taxi_paths(indices=taxis)  # get paths
        
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
        
        for path in paths:
            
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
                      title='Taxi Routes', width=600, height=470)
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
     
    def plot_heatmap(self):
        """Plot departing (red) and arriving (blue) locations."""
        start_nodes = list(self.trips_df.start_node)
        end_nodes = list(self.trips_df.end_node)
        node_indices = [item for sublist in list(zip(start_nodes,end_nodes)) for item in sublist]

        # parallel lists for nodes
        nodes = self.nodes_df.loc[node_indices]
        node_ids = nodes.name.values.tolist()
        x = nodes.x.values.tolist()
        y = nodes.y.values.tolist()    
        colors = ['red','blue']*int(len(node_ids)/2)

        # get plot boundaries
        min_x, max_x = min(nodes.x)-1000, max(nodes.x)+1000
        min_y, max_y = min(nodes.y)-1000, max(nodes.y)+1000

        plot = figure(x_range=(min_x, max_x), y_range=(min_y, max_y),
                      x_axis_type="mercator", y_axis_type="mercator",
                      title='Heatmap of Taxi Pickups / Dropoffs', plot_width=600, plot_height=470)
        plot.add_tile(get_provider(Vendors.CARTODBPOSITRON_RETINA))

        graph = GraphRenderer()

        # define initial location nodes
        graph.node_renderer.data_source.add(node_ids, 'index')
        graph.node_renderer.data_source.add(colors, 'colors')
        graph.node_renderer.glyph = Circle(size=7,line_width=0,fill_alpha=1/self.T_max, fill_color='colors')


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
        
        # Eliminate key error
        row['trip_distance'] = None
        row['passenger_count'] = None
        row['revenue'] = None
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

def plot_returns(trips_df, nodes_df, arcs_df, start, end, taxi_min, taxi_max, intervals):
    """Plot the marginal returns of adding an additional taxi to the fleet.
    
    Args:
        start (int): start time of time window of interest
        end (int): end time of time window of interest
        taxi_min: minimum number of taxis to examine
        taxi_max: maximum number of taxis to examine
        intervals: number of intervals of fleet size to compute
    """
    step = int((taxi_max - taxi_min)/(intervals - 1))
    x = []
    revenue = []
    marginal_return = []
    for i in range(intervals):
        x.append(taxi_min + i*step)
        base = TaxiRouting(trips_df, nodes_df, arcs_df, start, end, taxi_min + i*step)
        base.optimize()
        base.compute_taxi_stats()
        inc = TaxiRouting(trips_df, nodes_df, arcs_df, start, end, taxi_min + i*step + 1)
        inc.optimize()
        inc.compute_taxi_stats()
        revenue.append(base.total_revenue)
        marginal_return.append(inc.total_revenue - base.total_revenue) 
        
    plt.plot(x, revenue)
    plt.xlabel('Number of Taxi Cabs')
    plt.ylabel('Revenue')
    plt.title('Number of Taxi Cabs vs. Revenue')
    plt.show()
    
    plt.plot(x, marginal_return)
    plt.xlabel('Number of Taxi Cabs')
    plt.ylabel('Marginal Return')
    plt.title('Number of Taxi Cabs vs. Marginal Return')
    plt.show()