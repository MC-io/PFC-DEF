from concurrent.futures import ThreadPoolExecutor, as_completed
from island import Island
from population import Population

import random

class Migration:
    def __init__(self, num_islands, num_population, migration_every_gen, num_of_generations, tndp, num_of_routes, num_of_tour_particips, tournament_prob, min_route, max_route, num_migrants):
        self.islands = []
        for i in range(num_islands):
            num_of_individuals = num_population // num_islands
            if i < num_population % num_islands:
                num_of_individuals += 1
            island = Island(num_of_individuals, tndp, num_of_routes, num_of_tour_particips, tournament_prob, min_route, max_route)
            self.islands.append(island)
        for island in self.islands:
            print(island.num_of_individuals)
        self.migration_every_gen = migration_every_gen
        self.num_of_generations = num_of_generations
        self.num_migrants = num_migrants

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


    def migrate(self):
        redistribution_plan = [[] for _ in range(len(self.islands))]

        for i in range(len(self.islands)):
            migrants = self.islands[i].exile_migrants(self.num_migrants)
            for migrant in migrants:
                target_islands_index = random.choice([x for x in range(len(self.islands)) if x != i])
                redistribution_plan[target_islands_index].append(migrant)

        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(self.islands[i].receive_migrants, redistribution_plan[i]) for i in range(len(redistribution_plan))]
            for future in as_completed(futures):
                future.result()

    def run(self):
        with ThreadPoolExecutor(max_workers=12) as executor:
            futures = [executor.submit(island.initialize_island) for island in self.islands]
            for future in as_completed(futures) :
                    future.result()

        for generation in range(self.num_of_generations):
            print(f"Generacion {generation}")
            with ThreadPoolExecutor(max_workers=12) as executor:
                futures = [executor.submit(island.execute_generation, ind) for ind, island in enumerate(self.islands)]
                for future in as_completed(futures) :
                    future.result()
            if generation + 1 % self.migration_every_gen == 0:
                self.migrate()
        
        
        final_population = Population()

        for future in futures:
            final_population.extend(future.result())
    
        self.fast_non_dominated_sort(final_population)
        for front in final_population.fronts:
            self.calculate_crowding_distance(front)

        return final_population.fronts[0]

        

        