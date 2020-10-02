import numpy as np
import pandas as pd
from gurobipy import *


class Trip(object):
    """docstring for Trip"""
    def __init__(self, start, end, start_time, trip_time, battery_cost, value, capacity):
        self.start = start
        self.end = end
        self.start_time = start_time
        self.trip_time = trip_time
        self.end_time = start_time + trip_time
        self.battery_cost = battery_cost  # TODO: Should be removed.
        self.value = value
        self.capacity = capacity
        self.price = None
        self.completed = None
        self.total_flow = 0
        # print(self)

    def __str__(self):
        return str(self.start) + ', ' + str(self.end) + ', ' + str(self.start_time) + ', ' + str(self.end_time) + ', ' + str(self.battery_cost) + ', ' + str(self.capacity)



class Path(object):
    """docstring for Path"""
    def __init__(self, arcs, flow):
        self.arcs = arcs
        self.flow = flow
        self.trips_completed = 0
        self.parse_path()

    def parse_path(self):
        for arc in self.arcs:
            if 'bike' in arc[0]:
                continue
            elif arc[1] == 'sink':
                continue
            else:
                l_start, t_start, b_start = parse_node(arc[0])
                l_end, t_end, b_end = parse_node(arc[1])
                if l_start != l_end:
                    self.trips_completed += 1


class Problem(object):
    """docstring for Problem"""
    def __init__(self, params_dict):
        self.num_bikes = params_dict['bikes']
        self.locations = params_dict['L']
        self.T_max = params_dict['T_max']
        self.B_max = params_dict['B_max']
        self.trips = params_dict['trips']

        if 'capacity' in params_dict.keys():
            self.capacity = params_dict['capacity']
        else:
            self.capacity = None
        self.process_capacity()

        self.check_valid_entries()

    def process_capacity(self):
        capacity_dict = dict()
        if self.capacity == None:
            for location in self.locations:
                capacity_dict[location] = GRB.INFINITY
        elif type(self.capacity) == int:
            for location in self.locations:
                capacity_dict[location] = self.capacity
        elif type(self.capacity) == list:
            assert len(self.capacity) == len(self.locations)
            for location, capacity in zip(self.locations, self.capacity):
                capacity_dict[location] = capacity
        elif type(self.capacity) == dict:
            for location in self.locations:
                assert location in self.capacity.keys()
                capacity_dict = self.capacity
        else:
            raise TypeError

        self.capacity = capacity_dict
        return

    def check_valid_entries(self):
        assert type(self.num_bikes) == int
        assert type(self.locations) == list
        assert type(self.T_max) == int
        assert type(self.B_max) == int
        assert type(self.trips) == list
        # for trip in self.trips:
        # 	assert isinstance(type(trip), Trip)
        for location in self.locations:
            assert location in self.capacity.keys()
        return


class OptParams(object):
    """docstring for OptParams"""
    def __init__(self, params_dict):
        self.sub_formulation = params_dict['formulation']
        self.epsilon_perturb = params_dict['epsilon-perturb']
        # self.flow_decomposition = params_dict['flow-decomposition']
        self.verbose = params_dict['verbose']
        self.simplex = params_dict['simplex']
        self.time_limit = params_dict['time_limit']
        self.MIPGap = params_dict['MIPGap']
        self.first_stage_formulation = params_dict['first-stage-formulation']

    def check_valid_entries(self):
        assert self.sub_formulation in ['LP', 'MCF', 'IP']
        assert self.epsilon_perturb in [True, False]
        assert self.flow_decomposition in [True, False]
        assert self.verbose in [True, False]
        assert self.simplex in [True, False]
        if self.time_limit != None:
            assert type(self.time_limit) == int
        if self.MIPGap != None:
            assert type(self.MIPGap) == float
        assert self.first_stage_formulation in ['LP', 'IP']

        return

    def sub_problem_opt_params(self):
        return_dict = dict()
        return_dict['formulation'] = self.sub_formulation
        return_dict['epsilon-perturb'] = self.epsilon_perturb
        # return_dict['flow-decomposition'] = self.flow_decomposition
        return_dict['verbose'] = self.verbose
        return_dict['simplex'] = self.simplex
        return_dict['time_limit'] = self.time_limit
        return_dict['MIPGap'] = self.MIPGap
        return return_dict

    def first_stage_opt_params(self):
        return_dict = dict()
        return_dict['formulation'] = self.first_stage_formulation
        return_dict['verbose'] = self.verbose
        return return_dict


def is_int(number, threshold=0.000001):
    return min(number - np.floor(number), np.ceil(number) - number) < threshold


def find_capacity(capacity, station):
    if capacity == None:
        return GRB.INFINITY
    elif type(capacity) != dict:
        return capacity
    else:
        return capacity[station]


def node_name(l,t):
    return 'L'+str(l)+'_T'+str(t)

