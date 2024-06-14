import threading
from task_1_solver import Dijkstra, Astar
from csv_preprocessing import load_csv
import config
from user_communication import input_parameters, input_stops_time

def run():
    graph = {}
    event = threading.Event()
    average_speed = load_csv(graph, config.FILENAME, event)
    exit_flag = False
    algorithm_criteria = {
        '1' : ('Dijkstra', {config.TIME_CRITERIA : 'Time criteria', config.LINE_CHANGE_CRITERIA : 'Line change criteria'}),
        '2' : ('A*', {config.TIME_CRITERIA : 'Time criteria', config.LINE_CHANGE_CRITERIA : 'Line change criteria'})
    }
    algorithm_solvers = {
        '1' : Dijkstra.solve,
        '2' : Astar.solve
    }
    start, end, dep_time = input_stops_time(graph.keys())
    while not exit_flag:
        algorithm, criteria = input_parameters(algorithm_criteria)
        if algorithm == '2':
            algorithm_solvers[algorithm](graph,start,end,criteria,dep_time,average_speed)
        else:
            algorithm_solvers[algorithm](graph,start,end,criteria,dep_time)
        exit_input = input('\n\nDo you want to exit? [Y]')
        if (exit_input == 'Y'):
            exit_flag = True
        else:
            stops_time_change = input('Do you want to change stops or departure time? [Y]')
            if (stops_time_change == 'Y'):
                start, end, dep_time = input_stops_time(graph.keys())
            
if __name__=='__main__':
    run()
