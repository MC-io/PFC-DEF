import random
import numpy as np
from population import Population
from routeset import RouteSet
import copy
import time

class Island:
    def __init__(self, num_of_individuals, tndp, num_of_routes, num_of_tour_particips, tournament_prob, min_route, max_route):
        self.num_of_individuals = num_of_individuals
        self.graph = tndp.network
        self.demand_matrix = tndp.demand_matrix
        self.population = None
        self.num_of_routes = num_of_routes
        self.network_size = tndp.size
        self.num_of_tour_particips = num_of_tour_particips
        self.tournament_prob = tournament_prob
        self.min_route = min_route
        self.max_route = max_route

    def absorption(self, routeset):
        routes_to_absorb = []
        for i in range(len(routeset.routes) - 1, -1, -1):
            for j in range(len(routeset.routes)):
                if i != j and j not in routes_to_absorb and i not in routes_to_absorb and len(routeset.routes[i]) <= len(routeset.routes[j]):
                    for k in range(len(routeset.routes[j]) - len(routeset.routes[i]) + 1):
                        possible_subroute = routeset.routes[j][k:k + len(routeset.routes[i])]
                        possible_subroute_reverse = possible_subroute[::-1]
                        if possible_subroute == routeset.routes[i] or possible_subroute_reverse == routeset.routes[i]:
                            routes_to_absorb.append(i)
        for index in routes_to_absorb:
            del routeset.routes[index]

    def explore(self, visited, node, node_from, route, max_length):
        if node not in visited:
            visited.append(node)
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

    def generate_random_route(self, not_elected_nodes=None):
        random_start_point = random.randrange(0, self.network_size)
        if not_elected_nodes is not None and len(not_elected_nodes) > 0:
            random_start_point = random.choice(not_elected_nodes)
            not_elected_nodes.remove(random_start_point)
        max_length = random.randrange(self.min_route - 1, self.max_route) + 1
        visited = []
        random_route = [random_start_point]
        self.explore(visited, random_start_point, -1, random_route, max_length)
        return random_route
    
    def get_not_elected_nodes(self, routeset):
        elected_nodes = set()
        for route in routeset.routes:
            for a in route:
                elected_nodes.add(a)

        elected_nodes_list = list(elected_nodes)
        elected_nodes_list.sort()

        not_elected_nodes = []
        for i in range(self.network_size):
            if i not in elected_nodes_list:
                not_elected_nodes.append(i)

        return not_elected_nodes;
    
    def add_node_to_closest_end_terminal(self, node):
        pass

    def add_not_connected_nodes(self, routeset):
        not_connected = self.get_not_elected_nodes(routeset)

        for node in not_connected:
            self.add_node_to_closest_end_terminal(node)



    def generate_individual(self):
        random_routeset = RouteSet()
        while len(random_routeset.routes) < self.num_of_routes:
            not_elected_nodes = None
            # Si al menos ya se hizo una iteracion y absorcion
            if len(random_routeset.routes) > 0:
                not_elected_nodes = self.get_not_elected_nodes(random_routeset)
            while len(random_routeset.routes) < self.num_of_routes:
                random_route = self.generate_random_route(not_elected_nodes=not_elected_nodes)
                random_routeset.routes.append(random_route)
            self.absorption(random_routeset)

        return random_routeset
    
    def create_individual(self):
        individual = self.generate_individual()
        individual.calculate_objectives(self.graph, self.demand_matrix)
            
    def initialize_population(self):
        start = time.time()
        population = Population()
        
        for _ in range(self.num_of_individuals):
            individual = self.generate_individual()
            individual.calculate_objectives(self.graph, self.demand_matrix)
            population.population.append(individual)

        obj_1 = 0
        obj_2 = 0
        for routeset in population.population:
            obj_1 += routeset.objectives[0]
            obj_2 += routeset.objectives[1]

        end = time.time()
        print("Tiempo de inicializacion: {}".format(end - start))
        print("Promedio F1 en Inicializacion: {}".format(obj_1 / len(population.population)))
        print("Promedio F2 en Inicializacion: {}".format(obj_2 / len(population.population)))
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
            #print(len(front))
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
            #print(len(front))
            
    
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

    def initialize_island(self):
        self.population = self.initialize_population()
        self.fast_non_dominated_sort(self.population)
        for front in self.population.fronts:
            self.calculate_crowding_distance(front)

    def exile_migrants(self, num_migrants):
        if num_migrants > len(self.population):
            num_migrants = len(self.population)
        migrants = random.sample(self.population.population, num_migrants)
        self.population.population = [ind for ind in self.population.population if ind not in migrants]
        return migrants
    
    def receive_migrants(self, migrants):
        self.population.extend(migrants)
        self.fast_non_dominated_sort(self.population)
        for front in self.population.fronts:
            self.calculate_crowding_distance(front)

    def execute_generation(self, num):
        children = self.create_children(self.population)
        self.population.extend(children)
        self.fast_non_dominated_sort(self.population)
        new_population = Population()

        front_num = 0
        while len(new_population) + len(self.population.fronts[front_num]) <= self.num_of_individuals:
            self.calculate_crowding_distance(self.population.fronts[front_num])
            #print(len(self.population.fronts[front_num]), ' ', num)
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
        return returned_population