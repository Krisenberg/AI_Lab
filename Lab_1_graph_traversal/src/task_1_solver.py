from datetime import datetime, timedelta
from classes import Node, PrevNode
from math import sqrt
import time
import config
from user_communication import print_solve_stats

def find_best_connection(graph: dict[str, Node], vertex_start, vertex_end, time, prev_line, criteria):
    connections = graph[vertex_start].get_connections(vertex_end)
    best_connection = connections[0]
    min_weight = config.MAX_DATE
    best_no_change_connection = None
    min_no_change_weight = config.MAX_DATE

    for conn in connections:
        line = conn.line
        condition_1 = ((prev_line is not None) and (prev_line != line) and (conn.departure_time - config.TIME_FOR_CHANGE >= time) and (conn.arrival_time < min_weight))
        condition_2 = ((prev_line is None) or (prev_line == line)) and (conn.departure_time >= time) and (conn.arrival_time < min_weight)
        if condition_1 or condition_2:
            min_weight = conn.arrival_time
            best_connection = conn
        if criteria == config.LINE_CHANGE_CRITERIA:
            condition_no_change_no_prev_line = (prev_line is None) and (conn.departure_time >= time) and (conn.arrival_time < min_no_change_weight)
            condition_no_change_is_prev_line = (prev_line == line) and (conn.departure_time == time) and (conn.arrival_time < min_no_change_weight)
            if condition_no_change_no_prev_line or condition_no_change_is_prev_line:
                min_no_change_weight = conn.arrival_time
                best_no_change_connection = conn
    if criteria == config.LINE_CHANGE_CRITERIA and best_no_change_connection:
        return best_no_change_connection
    if best_connection.departure_time < time:
        return None
    return best_connection

class Dijkstra:
    def find_vertex_min_dist(vertex_set: set, dist: list, criteria: str):
        vertex = next(iter(vertex_set))
        criteria_index = 0 if criteria == config.TIME_CRITERIA else 1
        min_dist = dist[vertex][criteria_index]
        for v in vertex_set:
            if dist[v][criteria_index] < min_dist:
                min_dist = dist[v][criteria_index]
                vertex = v
        return vertex

    def dijkstra(graph: dict[str, Node], source, target, criteria, time):
        prev: dict[str, PrevNode] = {}
        dist: dict[str, list[datetime, int]] = {}
        q = set()
        
        for v in graph:
            prev[v] = None
            dist[v] = [config.MAX_DATE, config.MAX_CHANGES]
            q.add(v)
        
        dist[source][0] = time
        dist[source][1] = 0

        number_of_processed_nodes = 0
        number_of_processed_connections = 0

        while q:
            u = Dijkstra.find_vertex_min_dist(q, dist, criteria)
            if u == target:
                return prev, dist, number_of_processed_nodes, number_of_processed_connections
            q.remove(u)
            u_prev_line = prev[u].line if prev[u] else None
            for v in q:
                if v in graph[u].connections:
                    alt_conn = find_best_connection(graph, u, v, dist[u][0], u_prev_line, criteria)
                    number_of_processed_nodes += 1
                    number_of_processed_connections += len(graph[u].connections[v])
                    if alt_conn:
                        alt_conn_arrival_time = alt_conn.arrival_time
                        alt_conn_changes = 1 if (u_prev_line and alt_conn.line != u_prev_line) else 0
                        if criteria == config.TIME_CRITERIA and ((dist[v][0] == config.MAX_DATE) or (alt_conn_arrival_time < dist[v][0])):
                            dist[v] = [alt_conn_arrival_time, alt_conn_changes]
                            prev_node = PrevNode(u, alt_conn.line, alt_conn.departure_time)
                            prev[v] = prev_node
                            
                        if criteria == config.LINE_CHANGE_CRITERIA and ((dist[v][1] == config.MAX_CHANGES) or (dist[u][1] + alt_conn_changes < dist[v][1])):
                            dist[v] = [alt_conn_arrival_time, dist[u][1] + alt_conn_changes]
                            prev_node = PrevNode(u, alt_conn.line, alt_conn.departure_time)
                            prev[v] = prev_node
        return prev, dist, number_of_processed_nodes, number_of_processed_connections
    
    def solve(graph, source, target, cirteria, dep_time):
        timestamp_start = time.time()
        path = []
        dijkstra_prev, dijkstra_dist, processed_nodes, processed_connections = Dijkstra.dijkstra(graph, source, target, cirteria, dep_time)
        u = target
        while dijkstra_prev[u]:
            path.insert(0, (dijkstra_prev[u], u, dijkstra_dist[u][0]))
            u = dijkstra_prev[u].stop_name
        if not path:
            print(f'A path {source} -> {target} does not exist.')
            return
        line = path[0][0].line
        print(f'IN: {line} [{path[0][0].departure_time}]; {path[0][0].stop_name}')
        for i, node in enumerate(path):
            # if node[0].line != line:
            if node[0].line != line or (i > 0 and node[0].departure_time - timedelta(minutes=1) > path[i-1][2]):
                print(f'OUT: {line} [{path[i-1][2]}]; {node[0].stop_name}')
                print(f'IN: {node[0].line} [{node[0].departure_time}]; {node[0].stop_name}')
                line = node[0].line
            if node[1] == target:
                print(f'OUT: {line} [{node[2]}]; {target}')
        timestamp_end = time.time()
        print_solve_stats(processed_nodes, processed_connections, timestamp_start, timestamp_end)
        

class Astar:
    def find_vertex_min_dist(vertex_set: set, dist: list, criteria: str):
        vertex = next(iter(vertex_set))
        criteria_index = 1 if criteria == config.TIME_CRITERIA else 2
        min_dist = dist[vertex][criteria_index]
        for v in vertex_set:
            if dist[v][criteria_index] < min_dist:
                min_dist = dist[v][criteria_index]
                vertex = v
        return vertex
    
    def heuristic_time(graph: dict[str, Node], node: str, target: str, average_speed: float):
        if node == target:
            return timedelta(minutes=0)
        start_lat = graph[node].latitude
        start_lon = graph[node].longitude
        end_lat = graph[target].latitude
        end_lon = graph[target].longitude
        dist = sqrt((end_lat - start_lat) ** 2 + (end_lon - start_lon) ** 2)
        return timedelta(minutes=(dist * average_speed * config.TIME_HEURISTIC_AVG_FACTOR))
    
    def cosinus_between_two_vectors(graph: dict[str, Node], current: str, next: str, target: str):
        x_current, y_current = graph[current].latitude, graph[current].longitude
        x_next, y_next = graph[next].latitude, graph[next].longitude
        x_target, y_target = graph[target].latitude, graph[target].longitude
        current_next = sqrt((x_next - x_current) ** 2 + (y_next - y_current) ** 2)
        current_target = sqrt((x_target - x_current) ** 2 + (y_target - y_current) ** 2)
        next_target = sqrt((x_target - x_next) ** 2 + (y_target - y_next) ** 2)
        return ((next_target ** 2 - current_next ** 2 - current_target ** 2)) / (-2.0 * current_next * current_target)

    def heuristic_line_change(graph: dict[str, Node], was_change: bool, current: str, next: str, target: str):
        cosinus = Astar.cosinus_between_two_vectors(graph, current, next, target)
        if was_change and cosinus < 0.5:
            scaled_cos = cosinus + 1.0
            return (1.5 - scaled_cos)
        return 0

    def astar_dijkstra(graph: dict[str, Node], source, target, criteria, time, average_speed):
        prev: dict[str, PrevNode] = {}
        dist: dict[str, list[datetime, datetime, int, int]] = {}
        q = set()
        
        for v in graph:
            prev[v] = None
            dist[v] = [config.MAX_DATE, config.MAX_DATE, config.MAX_CHANGES, config.MAX_CHANGES]
            q.add(v)
        
        dist[source] =  [ time, time, 0, 0]

        number_of_processed_nodes = 0
        number_of_processed_connections = 0

        while q:
            u = Astar.find_vertex_min_dist(q, dist, criteria)
            if u == target:
                return prev, dist, number_of_processed_nodes, number_of_processed_connections
            q.remove(u)
            u_prev_line = prev[u].line if prev[u] else None
            for v in q:
                if v in graph[u].connections:
                    alt_conn = find_best_connection(graph, u, v, dist[u][0], u_prev_line, criteria)
                    number_of_processed_nodes += 1
                    number_of_processed_connections += len(graph[u].connections[v])
                    if alt_conn:
                        alt_conn_arrival_time = alt_conn.arrival_time
                        alt_conn_changes = 1 if (u_prev_line and (alt_conn.line != u_prev_line or alt_conn.departure_time > dist[u][0])) else 0
                        if criteria == config.TIME_CRITERIA and ((dist[v][0] == config.MAX_DATE) or (alt_conn_arrival_time < dist[v][0])):
                            dist[v] = [alt_conn_arrival_time, alt_conn_arrival_time  + Astar.heuristic_time(graph, v, target, average_speed), alt_conn_changes, alt_conn_changes]
                            prev_node = PrevNode(u, alt_conn.line, alt_conn.departure_time)
                            prev[v] = prev_node
                            
                        if criteria == config.LINE_CHANGE_CRITERIA and ((dist[v][2] == config.MAX_CHANGES) or (dist[u][2] + alt_conn_changes < dist[v][2])):
                            was_change = True if alt_conn_changes == 1 else False
                            dist[v] = [alt_conn_arrival_time, alt_conn_arrival_time, dist[u][2] + alt_conn_changes + Astar.heuristic_line_change(graph, was_change, u, v, target), dist[u][2] + alt_conn_changes]
                            prev_node = PrevNode(u, alt_conn.line, alt_conn.departure_time)
                            prev[v] = prev_node
                        if v == target:
                            return prev, dist, number_of_processed_nodes, number_of_processed_connections
        return prev, dist, number_of_processed_nodes, number_of_processed_connections


    def solve(graph, source, target, cirteria, dep_rime, average_speed):
        timestamp_start = time.time()
        path = []
        came_from, cost, processed_nodes, processed_connections = Astar.astar_dijkstra(graph, source, target, cirteria, dep_rime, average_speed)
        node = target

        while came_from[node]:
            path.insert(0, (came_from[node], node, cost[node][0]))
            node = came_from[node].stop_name
        if not path:
            print(f'A path {source} -> {target} does not exist.')
            return
        line = path[0][0].line
        print(f'IN: {line} [{path[0][0].departure_time}]; {path[0][0].stop_name}')
        for i, node in enumerate(path):
            if node[0].line != line or (i > 0 and node[0].departure_time - timedelta(minutes=1) > path[i-1][2]):
                print(f'OUT: {line} [{path[i-1][2]}]; {node[0].stop_name}')
                print(f'IN: {node[0].line} [{node[0].departure_time}]; {node[0].stop_name}')
                line = node[0].line
            if node[1] == target:
                print(f'OUT: {line} [{node[2]}]; {target}')
        timestamp_end = time.time()
        print_solve_stats(processed_nodes, processed_connections, timestamp_start, timestamp_end)
        