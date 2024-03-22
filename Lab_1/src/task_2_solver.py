from task_1_solver import Astar
from datetime import datetime
from math import sqrt, ceil
import config

class Tabu:
    def evaluate_solution(graph, stops: list[str], criteria: str, dep_time: datetime, average_speed: float):
        prev_paths = {}
        dist_paths = {}
        current_time = dep_time
        if (criteria == config.TIME_CRITERIA):
            for i in range(len(stops) - 1):
                current_stop = stops[i]
                next_stop = stops[i+1]
                prev, dist, _, _ = Astar.astar_dijkstra(graph, current_stop, next_stop, criteria, current_time, average_speed)
                current_time = dist[next_stop][0]
                prev_paths[next_stop] = prev
                dist_paths[next_stop] = dist
            return current_time, prev_paths, dist_paths
        
        line_changes = 0
        for i in range(len(stops) - 1):
            current_stop = stops[i]
            next_stop = stops[i+1]
            prev, dist, _, _ = Astar.astar_dijkstra(graph, current_stop, next_stop, criteria, current_time, average_speed)
            current_time = dist[next_stop][0]
            line_changes += dist[next_stop][3]
            prev_paths[next_stop] = prev
            dist_paths[next_stop] = dist
        return line_changes, prev_paths, dist_paths
    

    def generate_neighbourhood(solution: list[str]):
        neighbourhood = set()
        mid_index = ceil(len(solution) / 2)
        lower_half = solution[:mid_index]

        for i in range(1, len(lower_half)):
            similar_solution = solution[:]
            temp = similar_solution[len(similar_solution) - 1 - i]
            similar_solution[len(similar_solution) - 1 - i] = lower_half[i]
            similar_solution[i] = temp
            # similar_solution[len(similar_solution) - 2 - j] = lower_half[i]
            neighbourhood.add(tuple(similar_solution))
        return neighbourhood
    
    def shuffle_solution(solution: list[str]):
        temp = solution[1]
        for i in range(2, len(solution) - 1):
            solution[i - 1] = solution[i]
        solution[-2] = temp


    def generate_initial_solution(graph, source: str, middle_stops: list[str]):
        def calculate_distance(stop_name):
            start_lat = graph[source].latitude
            start_lon = graph[source].longitude
            end_lat = graph[stop_name].latitude
            end_lon = graph[stop_name].longitude
            return sqrt((end_lat - start_lat) ** 2 + (end_lon - start_lon) ** 2)

        sorted_middle_stops = sorted(middle_stops, key=lambda x: calculate_distance(x))
        mid_index = ceil(len(sorted_middle_stops) / 2)
        lower_half = sorted_middle_stops[:mid_index]
        upper_half = sorted_middle_stops[mid_index:]
        lower_half.reverse()
        return [source] + lower_half + upper_half + [source]
    
    def solve(graph, source: str, middle_stops: list[str], criteria: str, dep_time: datetime, average_speed: float):
        current_solution = Tabu.generate_initial_solution(graph, source, middle_stops)
        current_solution_eval, current_prev_paths, current_dist_paths = Tabu.evaluate_solution(graph, current_solution, criteria, dep_time, average_speed)
        best_solution = current_solution
        best_solution_eval, best_prev_paths, best_dist_paths = current_solution_eval, current_prev_paths, current_dist_paths
        tabu_set = set()

        k = 0
        while k < config.STEP_LIMIT:
            i = 0
            while i < config.OP_LIMIT:
                neighbourhood = Tabu.generate_neighbourhood(current_solution)
                best_neighbour_eval = config.MAX_DATE if criteria == config.TIME_CRITERIA else config.MAX_CHANGES
                best_neighbour, best_neighbourhood_prev_paths, best_neighbourhood_dist = None, None, None
                for neighbour in neighbourhood:
                    if neighbour not in tabu_set:
                        neighbour_list = list(neighbour)
                        evaluation, prev_paths, dist_paths = Tabu.evaluate_solution(graph, neighbour_list, criteria, dep_time, average_speed)
                        if evaluation < best_neighbour_eval:
                            best_neighbour_eval = evaluation
                            best_neighbour = neighbour_list
                            best_neighbourhood_prev_paths = prev_paths
                            best_neighbourhood_dist = dist_paths
                tabu_set = tabu_set.union(neighbourhood)

                if best_neighbour and best_neighbour_eval < current_solution_eval:
                    current_solution = best_neighbour
                    current_solution_eval = best_neighbour_eval
                    current_prev_paths = best_neighbourhood_prev_paths
                    current_dist_paths = best_neighbourhood_dist
                i += 1
            k += 1
            if current_solution_eval < best_solution_eval:
                best_solution = current_solution
                best_solution_eval = current_solution_eval
                best_prev_paths = current_prev_paths
                best_dist_paths = current_dist_paths
            Tabu.shuffle_solution(current_solution)

        # for target, came_from in best_prev_paths.items():
        prev_stop = source
        for target in best_solution:
            if prev_stop != source or target != source:
                print(f'\nPath from {prev_stop} to {target}:')
                node = target
                path = []
                came_from = best_prev_paths[target]
                cost = best_dist_paths[target]
                prev_stop = target
                # if dijkstra_prev[u] or u == source:
                while came_from[node]:
                    path.insert(0, (came_from[node], node, cost[node][0]))
                    node = came_from[node].stop_name
                if not path:
                    print(f'A path {node} -> {target} does not exist.')
                else:
                    line = path[0][0].line
                    print(f'IN: {line} [{path[0][0].departure_time}]; {path[0][0].stop_name}')
                    for i, node in enumerate(path):
                        if node[0].line != line:
                            print(f'OUT: {line} [{path[i-1][2]}]; {node[0].stop_name}')
                            print(f'IN: {node[0].line} [{node[0].departure_time}]; {node[0].stop_name}')
                            line = node[0].line
                        if node[1] == target:
                            print(f'OUT: {line} [{node[2]}]; {target}')
        print(f'Best solution: {best_solution}')
        # print(f'Best prev paths: {best_prev_paths}')
        # print(f'Best dist paths: {best_dist_paths}')
