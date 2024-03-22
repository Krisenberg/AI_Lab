import os
import csv
import threading
import time
import datetime
from task_2_solver import Tabu
from classes import Edge
from csv_preprocessing import load_csv
import config
from user_communication import input_parameters, input_stops_time, input_start_stop_dep_time, input_middle_stops, input_criteria

def run():
    graph = {}
    event = threading.Event()
    average_speed = load_csv(graph, config.FILENAME, event)
    exit_flag = False
    algorithm_criteria = {
        config.TIME_CRITERIA : 'Time criteria',
        config.LINE_CHANGE_CRITERIA : 'Line change criteria'
    }
    start, dep_time = input_start_stop_dep_time(graph.keys())
    middle_stops = input_middle_stops(graph.keys())
    while not exit_flag:
        criteria = input_criteria(algorithm_criteria)
        Tabu.solve(graph, start, middle_stops, criteria, dep_time, average_speed)
        exit_input = input('\n\nDo you want to exit? [Y]')
        if (exit_input == 'Y'):
            exit_flag = True
        else:
            stops_time_change = input('Do you want to change stops or departure time? [Y]')
            if (stops_time_change == 'Y'):
                start, dep_time = input_start_stop_dep_time(graph.keys())
                middle_stops = input_middle_stops(graph.keys())
            
if __name__=='__main__':
    run()