class RouteSet:
    def __init__(self):
        self.routes = []
        self.objectives = None
        self.rank = None
        self.crowding_distance = None
        self.domination_count = None
        self.dominated_solutions = None
        self.features = None

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.features == other.features
        return False

    def dominates(self, other_individual):
        and_condition = True
        or_condition = False
        for first, second in zip(self.objectives, other_individual.objectives):
            and_condition = and_condition and first <= second
            or_condition = or_condition or first < second
        return (and_condition and or_condition)
    
    def user_cost(self, graph, demand_matrix):      # Reducir tiempo de viaje promedio de cada pasajero
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
        return coverage / total_demand * -1
    

    def find_operator_cost(self, graph, demand_matrix):
        cost_sum = 0
        for route in self.routes:
            #print(len(route))
            for i in range(len(route) - 1):
                #print("{} {}".format(route[i], route[i + 1]))
                cost_sum += graph.get_edge(route[i], route[i + 1]).value
        return cost_sum * -1

    def calculate_objectives(self, graph, demand_matrix):
        self.objectives = [self.user_cost(graph, demand_matrix), self.find_coverage(graph, demand_matrix)]