from datetime import datetime
import time
import config

def print_csv_parsing_results(entries_count, timestamp_start, timestamp_end):
    print(f'--------------------------------------')
    print(f'Ended loading the csv file [{datetime.now().time()}]')
    print(f'Number of entries: {entries_count}')
    print(f'File has been loaded in {round(timestamp_end - timestamp_start, 2)} seconds. Returning to the main thread...')
    print(f'--------------------------------------')
    print('\tINPUT PARAMETERS\n')

def print_message_while_parsing_csv(event):
    print(f'Started loading the csv file [{datetime.now().time()}]')
    counter = 1
    while not event.is_set():
        time.sleep(1)
        print(f'Loading the csv file [{counter}s]...')
        counter += 1

def input_stop_name(stop_names: list[str], message: str):
    while True:
        stop = input(f'{message}: ')
        if stop in stop_names:
            return stop
        else:
            print(f'This name [{stop}] does not exist! Please provide a valid one.\n')

def input_algorithm(algorithm_criteria: dict[str, tuple[str,dict[str,str]]]):
    print('Select algorithm')
    for alg_code, alg_data in algorithm_criteria.items():
        print(f'\t[{alg_code}]\t{alg_data[0]}')
    while True:
        alg = input(f'Choice: ')
        if alg in algorithm_criteria:
            return alg
        else:
            print(f'This [{alg}] is not a valid selection!\n')

def input_criteria(available_criteria: dict[str,str]):
    print('Select criteria')
    for abbrev, full_name in available_criteria.items():
        print(f'\t[{abbrev}]: [{full_name}]')
    while True:
        criteria = input(f'Choice: ')
        if criteria in available_criteria:
            return criteria
        else:
            print(f'This [{criteria}] is not a valid criteria!\n')

def input_time_single_value(lower_bound, upper_bound, name):
    while True:
        value = input(f'{name} [{lower_bound} - {upper_bound}]: ')
        casted_value = 0
        try:
            casted_value = int(value)
            if casted_value in range(lower_bound, upper_bound + 1):
                return casted_value
            print(f'This [{value}] is not a value from range [{lower_bound} - {upper_bound}].\n')
        except ValueError:
            print(f'This [{value}] is not a valid integer.\n')

def input_time():
    print('\nSelect a departure time')
    day = input_time_single_value(1, 2, 'Day')
    hour = input_time_single_value(0, 23, 'Hour')
    minutes = input_time_single_value(0, 59, 'Minutes')
    return datetime.strptime(f'0{day}.03.2023 {hour}:{minutes}:00','%d.%m.%Y %H:%M:%S')

def input_parameters(algorithm_criteria: dict[str, tuple[str,dict[str,str]]]):
    algorithm = input_algorithm(algorithm_criteria)
    criteria = input_criteria(algorithm_criteria[algorithm][1])
    return algorithm, criteria

def input_stops_time(stop_names: list[str]):
    start_stop = input_stop_name(stop_names, 'Start stop [A]')
    end_stop = input_stop_name(stop_names, 'End stop [B]')
    dep_time = input_time()
    return start_stop, end_stop, dep_time

def input_start_stop_dep_time(stop_names: list[str]):
    start_stop = input_stop_name(stop_names, 'Start stop [A]')
    dep_time = input_time()
    return start_stop, dep_time

def input_middle_stops(stop_names: list[str]):
    middle_stops: list[str] = []
    while True:
        stop_name = input_stop_name(stop_names, 'Stop')
        middle_stops.append(stop_name)
        exit_flag = input('Finish? [Y]: ')
        if exit_flag == 'Y':
            return middle_stops

def print_solve_stats(processed_nodes, processed_connections, timestamp_start, timestamp_end):
    print(f'--------------------------------------')
    print(f'Processed nodes: [{processed_nodes}]')
    print(f'Processed connections: [{processed_connections}]')
    print(f'Solution has been found in {round(timestamp_end - timestamp_start, 2)} seconds.')
    print(f'--------------------------------------')