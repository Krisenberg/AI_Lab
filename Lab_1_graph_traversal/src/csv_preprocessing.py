import os
import csv
import threading
import time
import user_communication as io
from datetime import datetime
from classes import Edge, Node
from math import sqrt
from config import TIME_HEURISTIC_AVG_FACTOR

def copy_first_n_lines(n: int, filename: str, new_filename: str):
    dirname = os.path.pardir
    path_to_file = os.path.join(dirname, 'Data', filename)
    path_to_new_file = os.path.join(dirname, 'Data', new_filename)
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


def add_line_to_graph(graph: "dict[str, Node]", line, date_time_dep, date_time_arr, start_stop_lat, start_stop_lon, end_stop_lat, end_stop_lon):
    edge = Edge(line['line'], date_time_dep, date_time_arr)
    start_stop_name = line['start_stop']
    end_stop_name = line['end_stop']
    if start_stop_name not in graph:
        graph[start_stop_name] = Node(start_stop_name, start_stop_lat, start_stop_lon)
    if end_stop_name not in graph:
        graph[end_stop_name] = Node(end_stop_name, end_stop_lat, end_stop_lon)
    graph[start_stop_name].add_connection(line['end_stop'], edge)


def count_connection_dist_time(start_lat, end_lat, start_lon, end_lon, date_time_dep: datetime, date_time_arr: datetime):
    dist = sqrt((end_lat - start_lat) ** 2 + (end_lon - start_lon) ** 2)
    time = ((date_time_arr - date_time_dep).seconds)/60
    return dist, time


def threaded_csv_loading(graph, filename, event, total_time_dist: "dict[str, float]"):
    # dirname = os.path.dirname(__file__)
    # path_to_file = os.path.join(dirname, filename)
    dirname = os.path.pardir
    path_to_file = os.path.join(dirname, 'Data', filename)
    total_dist = 0
    total_time = 0
    with open(path_to_file, newline='', encoding='utf8') as input_file:
        csv_reader = csv.DictReader(input_file, delimiter=',')
        for line in csv_reader:
            date_time_dep = parse_str_to_datetime_object(line['departure_time'])
            date_time_arr = parse_str_to_datetime_object(line['arrival_time'])
            start_lat = float(line['start_stop_lat'])
            start_lon = float(line['start_stop_lon'])
            end_lat = float(line['end_stop_lat'])
            end_lon = float(line['end_stop_lon'])
            add_line_to_graph(graph, line, date_time_dep, date_time_arr, start_lat, start_lon, end_lat, end_lon)
            dist, time = count_connection_dist_time(start_lat, end_lat, start_lon, end_lon, date_time_dep, date_time_arr)
            total_dist += dist
            total_time += time
    # print(f'Tota dist: {total_dist}')
    # print(f'Total time: {total_time}')
    # print(f'Average: {total_time / total_dist}')
    total_time_dist['time'] = total_time
    total_time_dist['dist'] = total_dist
    event.set()

def load_csv(graph, filename: str, event: threading.Event):
    total_time_dist = {}
    thread = threading.Thread(target = threaded_csv_loading, args=(graph, filename, event, total_time_dist))
    timestamp_start = time.time()
    thread.start()
    io.print_message_while_parsing_csv(event)
    thread.join()
    timestamp_end = time.time()
    number_of_entries = 0
    for val in graph.values():
        for conn in val.connections.values():
            number_of_entries += len(conn)
    # min_lat, min_lon = (100.0,) * 2
    # max_lat, max_lon = (0.0,) * 2
    # stop_min_lat, stop_min_lon, stop_max_lat, stop_max_lon = ('',) * 4
    # for val in graph.values():
    #     stop_lat, stop_lon = val.latitude, val.longitude
    #     if stop_lat < min_lat:
    #         min_lat = stop_lat
    #         stop_min_lat = val.stop_name
    #     if stop_lon < min_lon:
    #         min_lon = stop_lon
    #         stop_min_lon = val.stop_name
    #     if stop_lat > max_lat:
    #         max_lat = stop_lat
    #         stop_max_lat = val.stop_name
    #     if stop_lon > max_lon:
    #         max_lon = stop_lon
    #         stop_max_lon = val.stop_name
    #     for conn in val.connections.values():
    #         number_of_entries += len(conn)
    # print(f'Min lat: {stop_min_lat} -> {min_lat}')
    # print(f'Max lat: {stop_max_lat} -> {max_lat}')
    # print(f'Min lon: {stop_min_lon} -> {min_lon}')
    # print(f'Max lon: {stop_max_lon} -> {max_lon}')
    average_speed = total_time_dist['time'] / total_time_dist['dist']
    io.print_csv_parsing_results(number_of_entries, timestamp_start, timestamp_end)
    # check_counted_avg_speed_times_factor(filename, average_speed)
    return average_speed

def check_counted_avg_speed_times_factor(filename, avg_speed):
    dirname = os.path.dirname(__file__)
    path_to_file = os.path.join(dirname, filename)
    with open(path_to_file, newline='', encoding='utf8') as input_file:
        csv_reader = csv.DictReader(input_file, delimiter=',')
        for line in csv_reader:
            date_time_dep = parse_str_to_datetime_object(line['departure_time'])
            date_time_arr = parse_str_to_datetime_object(line['arrival_time'])
            start_lat = float(line['start_stop_lat'])
            start_lon = float(line['start_stop_lon'])
            end_lat = float(line['end_stop_lat'])
            end_lon = float(line['end_stop_lon'])
            dist, time = count_connection_dist_time(start_lat, end_lat, start_lon, end_lon, date_time_dep, date_time_arr)
            heuristic_time = avg_speed * dist * TIME_HEURISTIC_AVG_FACTOR
            if time > 0 and heuristic_time > time:
                start_stop = line['start_stop']
                end_stop = line['end_stop']
                print(f'Heuristic time not accepted in: {start_stop} -> {end_stop}, heuristic time: {heuristic_time}, real time: {time}')

# if __name__=='__main__':
#     copy_first_n_lines(10000, 'connection_graph.csv', 'con_graph.csv')