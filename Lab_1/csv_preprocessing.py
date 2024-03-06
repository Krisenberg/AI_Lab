import os
import csv
import threading
import time
from datetime import datetime
from classes import Edge

def copy_first_n_lines(n: int, filename: str, new_filename: str):
    dirname = os.path.dirname(__file__)
    path_to_file = os.path.join(dirname, filename)
    path_to_new_file = os.path.join(dirname, new_filename)
    with open(path_to_file, encoding='utf8') as input_file:
        head = [next(input_file) for _ in range(n)]
    with open(path_to_new_file, 'w', encoding='utf8') as output_file:
        for line in head:
            output_file.write(line)

def parse_str_to_datetime_object(date_time: str):
    day = 1
    hour = int(date_time[0:2])
    if hour >= 24:
        hour = hour - 24
        day = 2
    date = f'{day}.03.2023 {str(hour)}{date_time[2:]}'
    return datetime.strptime(date,'%d.%m.%Y %H:%M:%S')

def add_line_to_graph(graph, line):
    date_time_dep = parse_str_to_datetime_object(line['departure_time'])
    date_time_arr = parse_str_to_datetime_object(line['arrival_time'])
    edge = Edge(line['line'], date_time_dep, date_time_arr)
    if line['start_stop'] not in graph:
        graph[line['start_stop']] = {line['end_stop'] : [edge]}
    elif line['end_stop'] not in graph[line['start_stop']]:
        graph[line['start_stop']][line['end_stop']] = [edge]
    else:
        (graph[line['start_stop']][line['end_stop']]).append(edge)

def threaded_csv_loading(graph, filename, event):
    dirname = os.path.dirname(__file__)
    path_to_file = os.path.join(dirname, filename)
    with open(path_to_file, newline='', encoding='utf8') as input_file:
        csv_reader = csv.DictReader(input_file, delimiter=',')
        for line in csv_reader:
            add_line_to_graph(graph, line)
    event.set()

def load_csv(graph, filename, event):
    thread = threading.Thread(target = threaded_csv_loading, args=(graph, filename, event))
    thread.start()
    timestamp_start = time.time()
    print(f'Started loading the csv file [{datetime.now().time()}]')
    counter = 1
    while not event.is_set():
        time.sleep(1)
        print(f'Loading the csv file [{counter}s]...')
        counter += 1
    thread.join()
    timestamp_end = time.time()
    number_of_entries = 0
    for d in graph.values():
        for _, v in d.items():
            number_of_entries += len(v)
    print(f'--------------------------------------')
    print(f'Ended loading the csv file [{datetime.now().time()}]')
    print(f'Number of entries: {number_of_entries}')
    print(f'File has been loaded in {round(timestamp_end - timestamp_start, 2)} seconds. Returning to the main thread...')
    time.sleep(3)
    print(f'--------------------------------------\n\n')

# if __name__=='__main__':
#     copy_first_n_lines(10000, 'connection_graph.csv', 'con_graph.csv')