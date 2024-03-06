import os
import csv
import threading
import time
import datetime
from task_1_solver import Dijkstra
from classes import Edge
from csv_preprocessing import load_csv

# FILENAME = 'con_graph.csv'
FILENAME = 'connection_graph.csv'

# def threaded_csv_loading(graph):
#     dirname = os.path.dirname(__file__)
#     path_to_file = os.path.join(dirname, FILENAME)
#     with open(path_to_file, newline='', encoding='utf8') as input_file:
#         csv_reader = csv.DictReader(input_file, delimiter=',')
#         for line in csv_reader:
#             date = '01.03.2023 '
#             hour = int(line['departure_time'][0:2])
#             if hour >= 24:
#                 hour = hour - 24
#                 date = '02.03.2023 '
#             date = date + str(hour) + line['departure_time'][2:]
#             date_time_dep = datetime.datetime.strptime(date,'%d.%m.%Y %H:%M:%S')
#             date = '01.03.2023 '
#             hour = int(line['arrival_time'][0:2])
#             if hour >= 24:
#                 hour = hour - 24
#                 date = '02.03.2023 '
#             date = date + str(hour) + line['arrival_time'][2:]
#             date_time_arr = datetime.datetime.strptime(date,'%d.%m.%Y %H:%M:%S')
#             edge = Edge(line['line'], date_time_dep, date_time_arr)
#             # edge = Edge(line['line'], line['departure_time'], line['arrival_time'])
#             # node = Node(line['line'], datetime.datetime.strptime(line['departure_time'],'%H:%M:%S'),
#             #             datetime.datetime.strptime(line['arrival_time'],'%H:%M:%S'), line['end_stop'])
#             if line['start_stop'] not in graph:
#                 graph[line['start_stop']] = {line['end_stop'] : [edge]}
#             elif line['end_stop'] not in graph[line['start_stop']]:
#                 graph[line['start_stop']][line['end_stop']] = [edge]
#             else:
#                 (graph[line['start_stop']][line['end_stop']]).append(edge)
#     event.set()

# def load_csv(graph):
#     thread = threading.Thread(target = threaded_csv_loading, args=(graph,))
#     thread.start()
#     timestamp_start = time.time()
#     print(f'Started loading the csv file [{datetime.datetime.now().time()}]')
#     counter = 1
#     while not event.is_set():
#         time.sleep(1)
#         print(f'Loading the csv file [{counter}s]...')
#         counter += 1
#     thread.join()
#     timestamp_end = time.time()
#     number_of_entries = 0
#     for d in graph.values():
#         for _, v in d.items():
#             number_of_entries += len(v)
#     print(f'--------------------------------------')
#     print(f'Ended loading the csv file [{datetime.datetime.now().time()}]')
#     print(f'Number of entries: {number_of_entries}')
#     print(f'File has been loaded in {round(timestamp_end - timestamp_start, 2)} seconds. Returning to the main thread...')
#     time.sleep(3)
#     print(f'--------------------------------------\n\n')

def input_parameters(stops_names: list[str]):
    flag = True
    while flag:
        start = input('Start stop [A]:\t')
        if start in stops_names:
            flag = False
        else:
            print(f'This name [{start}] does not exist! Please provide a valid one.\n')
    flag = True
    while flag:
        end = input('End stop [B]:\t')
        if end in stops_names:
            flag = False
        else:
            print(f'This name [{end}] does not exist! Please provide a valid one.\n')
    criteria = input('Criteria:\t')
    dep_time = input('Time:\t')
    dep_time = datetime.datetime.strptime('01.03.2023 10:12:00','%d.%m.%Y %H:%M:%S')
    return start, end, criteria, dep_time

def run():
    graph = {}
    event = threading.Event()
    load_csv(graph, FILENAME, event)
    start, end, criteria, dep_time = input_parameters(graph.keys())
    Dijkstra.solve(graph, start, end, criteria, dep_time)
            
if __name__=='__main__':
    run()
