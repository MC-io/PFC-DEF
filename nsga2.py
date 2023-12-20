import random
import numpy as np
from population import Population
from routeset import RouteSet
import copy

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
        max_length = random.randrange(11, 25) + 1
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
            individual.calculate_objectives(self.graph, self.demand_matrix)
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
            print(len(front))
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
            print(len(front))
            
    
    def crowding_operator(self, individual, other_individual):
        if (individual.rank < other_individual.rank) or \
                ((individual.rank == other_individual.rank) and (
                        individual.crowding_distance > other_individual.crowding_distance)):
            return 1
        else:
            return -1
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
            child1.calculate_objectives(self.graph, self.demand_matrix)
            child2.calculate_objectives(self.graph, self.demand_matrix)
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

        self.fast_non_dominated_sort(self.population)
        for front in self.population.fronts:
            self.calculate_crowding_distance(front)
        children = self.create_children(self.population)
        returned_population = None


        for _ in range(self.generations):
            print("Generacion {}".format(_))
            self.population.extend(children)
            self.fast_non_dominated_sort(self.population)
            new_population = Population()
            front_num = 0
            print(len(self.population.fronts))
            while len(new_population) + len(self.population.fronts[front_num]) <= self.num_of_individuals:
                self.calculate_crowding_distance(self.population.fronts[front_num])
                for rs in self.population.fronts[front_num]:
                    new_population.append(copy.deepcopy(rs))
                front_num += 1

            self.calculate_crowding_distance(self.population.fronts[front_num])
            self.population.fronts[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)
            new_population.extend(self.population.fronts[front_num][0:self.num_of_individuals - len(new_population)])
            returned_population = self.population
            self.population = new_population
            self.fast_non_dominated_sort(self.population)
            for front in self.population.fronts:
                self.calculate_crowding_distance(front)
            children = self.create_children(self.population)

            for routeset in returned_population.fronts[0]:
                print("part:")
                for route in routeset.routes:
                    for a in route:
                        print("{} - ".format(a), end="")
                    print("")
        return returned_population.fronts[0]
            
