from concurrent.futures import ThreadPoolExecutor
from island import Island


class Migration:
    def __init__(self, num_islands, migration_every_gen, num_of_generations, num_of_individuals, tndp, num_of_routes, num_of_tour_particips, tournament_prob, min_route, max_route):
        self.islands = []
        for _ in range(num_islands):
            self.islands.append(Island(num_of_individuals, tndp, num_of_routes, num_of_tour_particips, tournament_prob, min_route, max_route))
        self.migration_every_gen = migration_every_gen
        self.num_of_generations = num_of_generations


    def migrate(self):
        

    def run(self):        
        with ThreadPoolExecutor(max_workers=12) as executor:
            futures = [executor.submit(island.initialize_island) for island in self.islands]
            for future in futures:
                print(future.result())
        
        for generation in range(self.num_of_generations):
            with ThreadPoolExecutor(max_workers=12) as executor:
                futures = [executor.submit(island.execute_generation) for island in self.islands]
                for future in futures:
                    print(future.result())
            if generation % self.migration_every_gen == 0:
            