import random
import numpy as np
from population import Population
from TNDP import TNDP, Graph, Edge
import matplotlib.pyplot as plt
import copy

class Route:
    def __init__(self, route_id, stops):
        self.route_id = route_id
        self.stops = stops

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

class NSGAII:
    def __init__(self, generations, num_of_individuals, tndp, num_of_routes, num_of_tour_particips, tournament_prob):
        self.generations = generations
        self.num_of_individuals = num_of_individuals
        self.graph = tndp.network
        self.demand_matrix = tndp.demand_matrix
        self.population = None
        self.num_of_routes = num_of_routes
        self.network_size = tndp.size
        self.num_of_tour_particips = num_of_tour_particips
        self.tournament_prob = tournament_prob


    def explore(self, visited, node, node_from, route, max_length):
        if node not in visited:
            cand_nodes = []
            for x in self.graph.nodes[node]:
                if x.to != node_from and x.to not in visited:
                    cand_nodes.append(x.to)

            if len(cand_nodes) == 0:
                return
            
            neighbour = random.randrange(0, len(cand_nodes))
            route.append(cand_nodes[neighbour])

            if len(route) < max_length:
                self.explore(visited, cand_nodes[neighbour], node, route, max_length)
                    


    def generate_random_route(self):
        random_start_point = random.randrange(0, self.network_size)
        max_length = random.randrange(12, 25)
        visited = []
        random_route = [random_start_point]
        self.explore(visited, random_start_point, -1, random_route, max_length)
        return random_route
    
    def generate_individual(self):
        random_routeset = RouteSet()
        for i in range(self.num_of_routes):
            random_route = self.generate_random_route()
            random_routeset.routes.append(random_route)
        return random_routeset
            
    def initialize_population(self):
        population = Population()
        for _ in range(self.num_of_individuals):
            individual = self.generate_individual()
            individual.calculate_fitness(self.graph, self.demand_matrix)
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


    def create_children(self, population):
        children = []
        while len(children) < len(population):
            parent1 = self.tournament(population)
            parent2 = self.tournament(population)

            while parent1.routes == parent2.routes:
                parent2 = self.tournament(population)
            
            child1, child2 = self.crossover(parent1, parent2)
            self.mutate(child1)
            self.mutate(child2)
            child1.calculate_fitness(self.graph, self.demand_matrix)
            child2.calculate_fitness(self.graph, self.demand_matrix)
            children.append(child1)
            children.append(child2)

        return children

    def tournament(self, population):
        participants = random.sample(population.population, self.num_of_tour_particips)
        best = None
        for participant in participants:
            if best is None or (participant.fitness < best.fitness):
                best = participant

        return best

    def choose_with_prob(self, prob):
        if random.random() <= prob:
            return True
        

    def crossover(self, parent1, parent2):
        child1 = copy.deepcopy(parent1)
        child2 = copy.deepcopy(parent2)

        longest_route_ind1 = len(child1.routes[0])
        pos_longest_route_ind1 = 0
        for i in range(len(child1.routes)):
            if len(child1.routes[i]) > longest_route_ind1:
                longest_route_ind1 = len(child1.routes[i])
                pos_longest_route_ind1 = i

        parent1_longest_route = child1.routes[pos_longest_route_ind1]
        child1.routes.pop(pos_longest_route_ind1)

        longest_route_ind2 = len(child2.routes[0])
        pos_longest_route_ind2 = 0
        for i in range(len(child2.routes)):
            if len(child2.routes[i]) > longest_route_ind2:
                longest_route_ind2 = len(child2.routes[i])
                pos_longest_route_ind2 = i


        parent2_longest_route = child2.routes[pos_longest_route_ind2]

        child2.routes.pop(pos_longest_route_ind2)

        child1.routes.append(parent2_longest_route)
        child2.routes.append(parent1_longest_route)
        return child1, child2

    def mutate(self, route_set):
        for node in route_set.routes[0]:   
            for i in range(1,len(route_set.routes)):
                end_point = len(route_set.routes[i]) - 1
                if node == route_set.routes[i][0]:
                    if len(route_set.routes[i]) > 2:
                        route_set.routes[i].pop(0)
                elif node == route_set.routes[i][end_point]:
                    if len(route_set.routes[i]) > 2:
                        route_set.routes[i].pop(end_point)



    def run(self):
        self.population = self.initialize_population()
        returned_population = None

        for _ in range(self.generations):
            print("Generacion {}".format(_))
            children = self.create_children(self.population)
            self.population = Population()
            self.population.extend(children)
            returned_population = self.population
        return returned_population
            


if __name__ == "__main__":
    num_nodes = 127

    tndp = TNDP(num_nodes)

    tndp.read_network_from_file("networks\\Mumford3\\mumford3_links.csv")
    tndp.read_demand_matrix_from_file("networks\\Mumford3\\mumford3_demand.csv")

    nsga = NSGAII(num_of_individuals=50, generations=20, tndp=tndp, num_of_routes=60, num_of_tour_particips=2, tournament_prob=0.9)

    final_population = nsga.run()

    func = [i.objectives for i in final_population]

    user_cost = [i[0] for i in func]
    coverage = [i[1] for i in func]
    plt.xlabel('Costo de Usuario', fontsize=15)
    plt.ylabel('Cobertura', fontsize=15)
    plt.scatter(user_cost, coverage)
    plt.show()
