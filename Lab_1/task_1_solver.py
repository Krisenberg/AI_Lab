import math
from datetime import datetime, timedelta
from classes import Node, Edge

MAX_DATE = datetime.strptime('02.03.2023 23:59:59','%d.%m.%Y %H:%M:%S')

def calculate_weight_time(graph: dict[str, dict[str, list[Edge]]], vertex_start, vertex_end, time, prev_line):
    connections = graph[vertex_start][vertex_end]
    min_weight = MAX_DATE
    best_connection = graph[vertex_start][vertex_end][0]
    for conn in connections:
        line = conn.line
        condition_1 = (prev_line is not None and prev_line != line and (conn.departure_time - timedelta(minutes=5)) > time and conn.arrival_time < min_weight)
        condition_2 = False
        if not condition_1:
            condition_2 = (prev_line is None or prev_line == line) and conn.departure_time >= time and conn.arrival_time < min_weight
        if condition_1 or condition_2:
            min_weight = conn.arrival_time
            best_connection = conn
        # if conn.departure_time >= time and conn.arrival_time < min_weight:
        #     min_weight = conn.arrival_time
        #     best_connection = conn
    if best_connection.departure_time < time:
        return None
    return best_connection

class Dijkstra:
    def find_vertex_min_dist(vertex_set: set, dist: list):
        vertex = next(iter(vertex_set))
        min_dist = dist[vertex]
        for v in vertex_set:
            if dist[v] < min_dist:
                min_dist = dist[v]
                vertex = v
        return vertex

    def dijkstra(graph, source, target, criteria, time):
        prev = {}
        dist = {}
        q = set()
        
        for v in graph:
            prev[v] = None
            dist[v] = MAX_DATE
            q.add(v)
        
        dist[source] = time

        while q:
            u = Dijkstra.find_vertex_min_dist(q, dist)
            if u == target:
                return prev, dist
            q.remove(u)
            if prev[u]:
                u_prev_line = prev[u].line
            else:
                u_prev_line = None
            for v in q:
                if v in graph[u]:
                    alt_conn = calculate_weight_time(graph, u, v, dist[u], u_prev_line)
                    if alt_conn and alt_conn.arrival_time < dist[v]:
                        # print(f'{v}, dist[v]={dist[v]}, alt_dist={alt_conn.arrival_time}')
                        dist[v] = alt_conn.arrival_time
                        prev_node = Node(u, alt_conn.line, alt_conn.departure_time)
                        prev[v] = prev_node                    
        return prev, dist
    
    def solve(graph, source, target, cirteria, time):
        path = []
        dijkstra_prev, dijkstra_dist = Dijkstra.dijkstra(graph, source, target, cirteria, time)
        u = target
        # if dijkstra_prev[u] or u == source:
        while dijkstra_prev[u]:
            path.insert(0, (dijkstra_prev[u], u, dijkstra_dist[u]))
            u = dijkstra_prev[u].stop_name
        if not path:
            print(f'A path {source} -> {target} does not exist.')
            return
        line = path[0][0].line
        print(f'IN: {line} [{path[0][0].departure_time}]; {path[0][0].stop_name}')
        is_new_line = False
        for i, node in enumerate(path):
            if node[0].line != line:
                print(f'OUT: {line} [{path[i-1][2]}]; {node[0].stop_name}')
                print(f'IN: {node[0].line} [{node[0].departure_time}]; {node[0].stop_name}')
                line = node[0].line
            if node[1] == target:
                print(f'OUT: {line} [{node[2]}]; {target}')

            # if is_new_line:
            #     print(f'IN: {line} [{node[0].departure_time}]; {node[0].stop_name}')
            #     is_new_line = False
            # elif node[0].line != line:
            #     is_new_line = True
            #     print(f'OUT: {line} [{node[0].departure_time}]; {node[0].stop_name}')
            #     line = node[0].line
            #     and node[1] != target:
        