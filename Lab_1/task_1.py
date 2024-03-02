import os
import csv
import threading
import time
import datetime

FILENAME = 'connection_graph.csv'
event = threading.Event()

class Node:
    def __init__(self, line, departure_time, arrival_time, stop_name):
        self.line = line
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.stop_name = stop_name

    def __repr__(self):
        return f' ({self.line}, {self.stop_name}, {self.departure_time} -> {self.arrival_time}) '

def threaded_csv_loading(graph):
    dirname = os.path.dirname(__file__)
    path_to_file = os.path.join(dirname, FILENAME)
    with open(path_to_file, newline='', encoding='utf8') as input_file:
        csv_reader = csv.DictReader(input_file, delimiter=',')
        for line in csv_reader:
            node = Node(line['line'], line['departure_time'],
                            line['arrival_time'], line['end_stop'])
            if line['start_stop'] not in graph:
                graph[line['start_stop']] = [node]
            else:
                graph[line['start_stop']].append(node)
    event.set()

def load_csv(graph):
    thread = threading.Thread(target = threaded_csv_loading, args=(graph,))
    thread.start()
    timestamp_start = time.time()
    print(f'Starting loading the csv file [{datetime.datetime.now().time()}]')
    counter = 1
    while not event.is_set():
        time.sleep(1)
        print(f'Loading the csv file [{counter}s]...')
        counter += 1
    thread.join()
    timestamp_end = time.time()
    number_of_entries = 0
    for _, val in graph.items():
        number_of_entries += len(val)
    print(f'--------------------------------------\n\n')
    print(f'Number of entries: {number_of_entries}')
    print(f'File has been loaded in {round(timestamp_end - timestamp_start, 2)} seconds. Returning to the main thread...')
    time.sleep(3)
    print(f'--------------------------------------\n\n')

def input_parameters(stops_names: list[str]):
    flag = True
    
    while flag:
        start = input('Start stop [A]:\t')
        if start in stops_names:
            flag = False
        else:
            print(f'This name [{start}] does not exist! Please provide a valid one.\n')

def run():
    graph = {}
    load_csv(graph)
    input_parameters(graph.keys())
    # counter = 1
    # for key, val in graph.items():
    #     if (counter <= 5):
    #         print(f'\n{key} --> ')
    #         print ([node for node in val])
    #         counter += 1
    #     else:
    #         return
            
if __name__=='__main__':
    run()
