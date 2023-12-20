class RouteSet:
    def __init__(self):
        self.routes = []
        self.fitness = None
        self.rank = None
        self.crowding_distance = None
        self.domination_count = None
        self.dominated_solutions = None
        self.features = None
        self.objectives = None

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.features == other.features
        return False
    
    def user_cost(self, graph, demand_matrix):
        total_time = 0
        for route in self.routes:
            for i in range(len(route) - 1):
                nw_x = 0
                for edge in graph.nodes[route[i]]:
                    if edge.to == route[i + 1]:
                        nw_x = edge.value
                total_time += demand_matrix[route[i]][route[i + 1]] * nw_x
        return total_time

    def find_coverage(self, graph, demand_matrix):    
        total_demand = 0
        for i in range(len(demand_matrix)):
            for j in range(len(demand_matrix)):
                total_demand += demand_matrix[i][j]
        coverage = 0
        for route in self.routes:
            for i in range(len(route) - 1):
                for j in range(i + 1, len(route)):
                    coverage += demand_matrix[i][j]
        return coverage / total_demand

    def calculate_fitness(self, graph, demand_matrix):
        self.fitness = self.user_cost(graph, demand_matrix) + self.find_coverage(graph, demand_matrix)
        self.objectives = [self.user_cost(graph, demand_matrix), self.find_coverage(graph, demand_matrix)]