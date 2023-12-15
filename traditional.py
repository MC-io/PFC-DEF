import random
import networkx as nx
import numpy as np
from population import Population

class Route:
    def __init__(self, route_id, stops):
        self.route_id = route_id
        self.stops = stops

class RouteSet:
    def __init__(self, graph, demand_matrix, routes=None):
        self.graph = graph
        self.demand_matrix = demand_matrix
        self.routes = routes if routes else self.generate_random_routes()
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
    
    def user_cost(self):      # Reducir tiempo de viaje promedio de cada pasajero
        total_time = 0
        for route in self.routes:
            for i in range(len(route) - 1):
                nw_x = 0
                for edge in route.network.nodes[route.nodes[i]]:
                    if edge.to == route.nodes[route.nodes[i + 1]]:
                        nw_x = self.network[route.nodes[i]][route.nodes[i + 1]]
                total_time += self.demand_matrix[route.nodes[i]][route.nodes[i + 1]] * nw_x
        return total_time


    def find_coverage(self):    
        total_demand = 0
        for i in range(len(self.demand_matrix)):
            for j in range(len(self.demand_matrix)):
                total_demand += self.demand_matrix[i][j]
        coverage = 0
        for route in self.routes:
            for i in range(len(route.nodes) - 1):
                for j in range(i + 1, len(route.nodes)):
                    coverage += self.demand_matrix[i][j]

        return coverage / total_demand


    def generate_random_routes(self):
        # Generate random routes based on the graph
        num_routes = random.randint(1, len(self.graph.nodes))
        routes = []
        for i in range(num_routes):
            route_id = i + 1
            stops = random.sample(list(self.graph.nodes), random.randint(2, len(self.graph.nodes)))
            route = Route(route_id, stops)
            routes.append(route)
        return routes

    def calculate_objectives(self):
        self.objectives = [self.user_cost(), self.find_coverage()]

def generate_random_graph(num_nodes, seed=None):
    # Generate a random graph
    G = nx.erdos_renyi_graph(num_nodes, 0.3, seed=seed)
    return G

def generate_random_demand_matrix(graph, seed=None):
    # Generate a random demand matrix based on the graph
    random.seed(seed)
    np.random.seed(seed)
    nodes = list(graph.nodes)
    demand_matrix = np.random.randint(1, 10, size=(len(nodes), len(nodes)))
    np.fill_diagonal(demand_matrix, 0)  # Set diagonal elements to zero
    return demand_matrix

class NSGAII:
    def __init__(self, generations, population_size, crossover_prob, mutation_prob, tndp, num_of_routes):
        self.generations = generations
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.graph = tndp.network
        self.demand_matrix = tndp.demand_matrix
        self.population = None
        self.on_generation_finished = []
        self.population_size = population_size
        self.num_pf_routes = num_of_routes
        self.network_size = len(graph.nodes)

    def generate_individual(self):
        random_routeset = RouteSet(self.graph, self.demand_matrix)
        for i in range(self.num_of_routes):
            random_start_point = random.randrange(0, self.network_size)
            random_routeset.routes.append(random_start_point)
            c = 1
            max_c = random.randrange(4, 10)
            aux = random_start_point
            while c < max_c:
                next = random.randrange(0, len(self.graph.nodes[aux]))
                random_routeset.routes.append(next)
                aux = next                
                c += 1
        return random_routeset
            
    def initialize_population(self):
        population = Population()
        for _ in range(self.num_of_individuals):
            individual = self.generate_individual()
            individual.calculate_objectives()
            population.append(individual)
        return population

    def fast_non_dominated_sort(self, population):
        population.fronts = [[]]
        for individual in population:
            individual.domination_count = 0
            individual.dominated_solutions = []
            for other_individual in population:
                if individual.dominates(other_individual):
                    individual.dominated_solutions.append(other_individual)
                elif other_individual.dominates(individual):
                    individual.domination_count += 1
            if individual.domination_count == 0:
                individual.rank = 0
                population.fronts[0].append(individual)
        i = 0
        while len(population.fronts[i]) > 0:
            temp = []
            for individual in population.fronts[i]:
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i + 1
                        temp.append(other_individual)
            i = i + 1
            population.fronts.append(temp)

    
    def calculate_crowding_distance(self, front):
        if len(front) > 0:
            solutions_num = len(front)
            for individual in front:
                individual.crowding_distance = 0

            for m in range(len(front[0].objectives)):
                front.sort(key=lambda individual: individual.objectives[m])
                front[0].crowding_distance = 10 ** 9
                front[solutions_num - 1].crowding_distance = 10 ** 9
                m_values = [individual.objectives[m] for individual in front]
                scale = max(m_values) - min(m_values)
                if scale == 0: scale = 1
                for i in range(1, solutions_num - 1):
                    front[i].crowding_distance += (front[i + 1].objectives[m] - front[i - 1].objectives[m]) / scale

    def create_children(self, population):
        children = []
        while len(children) < len(population):
            parent1 = self.tournament(population)
            parent2 = parent1
            while parent1 == parent2:
                parent2 = self.tournament(population)
            child1, child2 = self.crossover(parent1, parent2)
            self.mutate(child1)
            self.mutate(child2)
            self.problem.calculate_objectives(child1)
            self.problem.calculate_objectives(child2)
            children.append(child1)
            children.append(child2)

        return children

    def tournament(self, population):
        participants = random.sample(population.population, self.num_of_tour_particips)
        best = None
        for participant in participants:
            if best is None or (
                    self.crowding_operator(participant, best) == 1 and self.choose_with_prob(self.tournament_prob)):
                best = participant

        return best

    def choose_with_prob(self, prob):
        if random.random() <= prob:
            return True
        

    def crossover(self, parent1, parent2):
        child1 = parent1.copy()
        child2 = parent2.copy()

        longest_route_ind1 = child1.routes[0]
        pos_longest_route_ind1 = 0
        for i in range(len(child1.routes)):
            if child1.routes[i].size > longest_route_ind1:
                longest_route_ind1 = child1.routes[i].size
                pos_longest_route_ind1 = i

        child1.routes.pop(pos_longest_route_ind1)

        longest_route_ind2 = child2.routes[0]
        pos_longest_route_ind2 = 0
        for i in range(len(child2.routes)):
            if child2.routes[i].size > longest_route_ind2:
                longest_route_ind2 = child2.routes[i].size
                pos_longest_route_ind2 = i

        child2.routes.pop(pos_longest_route_ind2)

        child1.routes.append(longest_route_ind2)
        child2.routes.append(longest_route_ind1)
        return child1, child2

    def mutate(self, route_set):
        for node in route_set.routes[0].nodes:   
            for i in range(1,len(route_set.routes)):
                end_point = len(route_set.routes[i].nodes) - 1
                if node == route_set.routes[i].nodes[0]:
                    if route_set.routes[i].nodes.size > 2:
                        route_set.routes[i].nodes.pop(0)
                elif node == route_set.routes[i].nodes[end_point]:
                    if route_set.routes[i].nodes.size > 2:
                        route_set.routes[i].nodes.pop(end_point)



    def run(self):
        self.population = self.initialize_population()

        self.fast_non_dominated_sort(self.population)
        for front in self.population.fronts:
            self.calculate_crowding_distance(front)

        children = self.create_children(self.population)
        returned_population = None

        for _ in range(self.generations):
            self.population.extend(children)
            self.fast_non_dominated_sort(self.population)
            new_population = Population()
            front_num = 0

            while len(new_population) + len(self.population.fronts[front_num]) <= self.num_of_individuals:
                self.calculate_crowding_distance(self.population.fronts[front_num])
                new_population.extend(self.population.fronts[front_num])
                front_num += 1

            self.calculate_crowding_distance(self.population.fronts[front_num])
            self.population.fronts[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)
            new_population.extend(self.population.fronts[front_num][0:self.num_of_individuals - len(new_population)])
            returned_population = self.population
            self.population = new_population
            self.fast_nondominated_sort(self.population)
            for front in self.population.fronts:
                self.calculate_crowding_distance(front)
            children = self.create_children(self.population)
        return returned_population.fronts[0]
            

# Example usage:
num_nodes = 10
graph = generate_random_graph(num_nodes, seed=42)
demand_matrix = generate_random_demand_matrix(graph, seed=42)

nsga = NSGAII(population_size=10, generations=50, crossover_prob=0.8, mutation_prob=0.2, graph=graph, demand_matrix=demand_matrix)
final_population = nsga.run()

# Access objectives of solutions in the final Pareto front
for solution in final_population:
    print("Objectives:", solution.objectives)
    print("Routes:", [(route.route_id, route.stops) for route in solution.routes])
    print()