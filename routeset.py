from TNDP import Graph

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
        routeset_graph = self.convert_to_graph(graph)
        total_demand = 0
        dt = 0
        count = 0
        for i in range(len(demand_matrix)):
            for j in range(i, len(demand_matrix)):
                if i != j:
                    t = routeset_graph.get_shortest_path_length(i, j)
                    if t is not None:
                        total_demand += demand_matrix[i][j]
                        dt += demand_matrix[i][j] * t
                    else:
                        count += 1
        if total_demand == 0:
            return 5 + count / (len(demand_matrix) / 2)
        return dt / total_demand + count / (len(demand_matrix) / 2)

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
            for i in range(len(route) - 1):
                cost_sum += graph.get_edge(route[i], route[i + 1]).value
        return cost_sum

    def calculate_objectives(self, graph, demand_matrix):
        self.objectives = [self.user_cost(graph, demand_matrix), self.find_operator_cost(graph, demand_matrix)]


    def convert_to_graph(self, graph):
        routeset_graph = Graph(len(graph.nodes))
        for route in self.routes:
            for i in range(len(route) - 1):
                value = graph.get_edge(route[i], route[i + 1]).value
                routeset_graph.add_edge(route[i], route[i + 1], value)
                routeset_graph.add_edge(route[i + 1], route[i], value)
        return routeset_graph
