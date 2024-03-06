class Edge:
    def __init__(self, line, departure_time, arrival_time):
        self.line = line
        self.departure_time = departure_time
        self.arrival_time = arrival_time

    def __repr__(self):
        return f' ({self.line}, {self.departure_time} -> {self.arrival_time}) '
    
class Node:
    def __init__(self, stop_name, line, dep_time):
        self.stop_name = stop_name
        self.line = line
        self.departure_time = dep_time