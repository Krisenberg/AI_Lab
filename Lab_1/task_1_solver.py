import math
import datetime

def calculate_weight_time(graph, vertex_start, vertex_end):
    node = graph[vertex_start][vertex_end]
    return node.arrival_time - node.departure_time

class Dijkstra:
    def find_vertex_min_dist(vertex_set: set, dist: list):
        vertex = None
        min_dist = datetime.datetime.strptime('23:59:59','%H:%M:%S')
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
            dist[v] = datetime.datetime.strptime('23:59:59','%H:%M:%S')
            q.add(v)
        
        dist[source] = time

        while q:
            u = Dijkstra.find_vertex_min_dist(q, dist)
            if u == target:
                return prev    
            q.remove(u)
            for v in q:
                for node in graph[u]:
                    if v == node.stop_name:
                        alt_dist = dist[u] + (node.arrival_time - node.departure_time)
                        print(f'{v}, dist[v]={dist[v]}, alt_dist={alt_dist}')
                        if alt_dist < dist[v]:
                            dist[v] = alt_dist
                            prev[v] = u
        return prev
    
    def solve(graph, source, target, cirteria, time):
        path = []
        dijkstra_prev = Dijkstra.dijkstra(graph, source, target, cirteria, time)
        u = target
        if dijkstra_prev[u] or u == source:
            while u:
                path.insert(0, u)
                u = dijkstra_prev[u]
        if not path:
            print(f'A path {source} -> {target} does not exist.')
            return
        line = path[0]
        print(f'IN: {line} [{path[0].departure_time}]; {source}')
        for node in path:
            if node == target:
                print(f'OUT: {line} [{path[0].arrival_time}]; {node.stop_name}')
            elif node.line != line:
                print(f'OUT: {line} [{path[0].arrival_time}]; {node.stop_name}')
                line = node.line
                print(f'IN: {line} [{path[0].arrival_time}]; {node.stop_name}')
        