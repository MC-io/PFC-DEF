import csv
import heapq
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

    def get_edge(self, a, b):
        for edge in self.nodes[a]:
            if edge.to == b:
                return edge
        return None
    
    def get_shortest_path_length(self, start, end):
        distances = [float('inf')] * len(self.nodes)
        distances[start] = 0
        
        priority_queue = [(0, start)]
        
        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)
            if current_node == end:
                return current_distance
            if current_distance > distances[current_node]:
                continue
            for edge in self.nodes[current_node]:
                distance = current_distance + edge.value
                if distance < distances[edge.to]:
                    distances[edge.to] = distance
                    heapq.heappush(priority_queue, (distance, edge.to))
        return None

class TNDP:
    def __init__(self, size):
        self.size = size
        self.network = Graph(self.size)
        self.demand_matrix = []
        for i in range(size):
            self.demand_matrix.append([])
            for _ in range(size):
                self.demand_matrix[i].append(0)
        self.total_demand = 0

    def read_network_from_file(self, filename):
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.network.add_edge(int(row["from"]) - 1, int(row["to"]) - 1, int(row["travel_time"]))

        for i in range(len(self.network.nodes)):
            print("{} -> ".format(i), end="")
            for edge in self.network.nodes[i]:
                print(edge.to, end=" ")
            print("")



    def read_demand_matrix_from_file(self, filename):
        self.total_demand  = 0
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                i = int(row["from"]) - 1
                j = int(row["to"]) - 1
                self.demand_matrix[i][j] = int(row["demand"])
                self.total_demand += self.demand_matrix[i][j]

            
                

    
    