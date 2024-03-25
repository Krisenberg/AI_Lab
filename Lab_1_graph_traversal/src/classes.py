import datetime

class Edge:
    def __init__(self, line: str, departure_time: datetime, arrival_time: datetime):
        self.line = line
        self.departure_time = departure_time
        self.arrival_time = arrival_time

    def __repr__(self):
        return f' ({self.line}, {self.departure_time} -> {self.arrival_time}) '

class Node:
    def __init__(self, stop_name: str, latitude: float, longitude: float):
        self.stop_name = stop_name
        self.latitude = latitude
        self.longitude = longitude
        self.connections: dict[str, list[Edge]] = {}
    
    def add_connection(self, stop_name: str, edge: Edge):
        if stop_name not in self.connections:
            self.connections[stop_name] = [edge]
            return
        self.connections[stop_name].append(edge)
    
    def get_connections(self, end_stop):
        return self.connections[end_stop]
    
class PrevNode:
    def __init__(self, stop_name, line, dep_time):
        self.stop_name = stop_name
        self.line = line
        self.departure_time = dep_time