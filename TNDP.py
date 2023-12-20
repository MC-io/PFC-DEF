import csv

class Edge:
    def __init__(self, value, to):
        self.value = value
        self.to = to
        
class Graph:
    def __init__(self, size):
        self.nodes = []
        for _ in range(size):
            self.nodes.append([])

    def add_edge(self, a, b, value):
        self.nodes[a].append(Edge(value, b))

class TNDP:
    def __init__(self, size):
        self.size = size
        self.network = Graph(self.size)
        self.demand_matrix = []
        for i in range(size):
            self.network.nodes.append([])
            self.demand_matrix.append([])
            for _ in range(size):
                self.demand_matrix[i].append(0)
        self.total_demand = 0

    def read_network_from_file(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.network.add_edge(int(row["from"]) - 1, int(row["to"]) - 1, int(row["travel_time"]))

    def read_demand_matrix_from_file(self, filename):
        self.total_demand  = 0
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                i = int(row["from"]) - 1
                j = int(row["to"]) - 1
                self.demand_matrix[i][j] = int(row["demand"])
                self.total_demand += self.demand_matrix[i][j]

            
                

    
    