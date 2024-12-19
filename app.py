from migration import Migration
from TNDP import TNDP
import time
import matplotlib.pyplot as plt

def run(network_name, num_nodes, links_file, demand_file, nodes_file, num_routes, num_population, num_of_generations, num_islands, migration_every_gen, num_migrants, min_route, max_route):
    tndp = TNDP(num_nodes)

    tndp.read_network_from_file(links_file)
    tndp.read_demand_matrix_from_file(demand_file)


    start = time.time()

    nsga = Migration(num_population=num_population, num_of_generations=num_of_generations, num_islands=num_islands, 
                        migration_every_gen=migration_every_gen, num_migrants=num_migrants, tndp=tndp, num_of_routes=num_routes,
                        num_of_tour_particips=2, tournament_prob=0.9, min_route=min_route, max_route=max_route)        

    final_population = nsga.run()


    func = [i.objectives for i in final_population]

    user_cost = [i[0] for i in func]
    operator_cost = [i[1] for i in func]


    avg_user_cost = sum(user_cost) / len(user_cost)
    avg_operator_cost = sum(operator_cost) / len(operator_cost)

    print("Costo de Usuario promedio: {}".format(avg_user_cost))
    print("Cobertura promedio: {}".format(avg_operator_cost))
    
    end = time.time()
    
    print(f"Tiempo total de ejecucion: {end - start}")

    best_sol_f1 = None
    lowest_f1 = 9999999
    for sol in final_population:
        if sol.objectives[0] < lowest_f1:
            lowest_f1 = sol.objectives[0]
            best_sol_f1 = sol
    print(lowest_f1)
    best_sol_f1.show_plot(links_file, nodes_file)

    best_sol_f2 = None
    lowest_f2 = 9999999
    for sol in final_population:
        if sol.objectives[1] < lowest_f2:
            lowest_f2 = sol.objectives[1]
            best_sol_f2 = sol
    print(lowest_f2)
    best_sol_f2.show_plot(links_file, nodes_file)

    plt.xlabel('Costo de Usuario', fontsize=15)
    plt.ylabel('Costo de Operador', fontsize=15)
    plt.scatter(user_cost, operator_cost)
    plt.savefig(f'{network_name}.png')
    plt.show()

if __name__ == "__main__":
    
    run(network_name='mandl', num_nodes=15, 
        links_file="networks/Mandl/mandl_links.csv",
        demand_file="networks/Mandl/mandl_demand.csv",
        nodes_file="networks/Mandl/mandl_nodes.csv",
        num_population=100,
        num_of_generations=300,
        num_islands=5,
        migration_every_gen=20,
        num_migrants=3,
        num_routes=6,
        min_route=2,
        max_route=8)
    
    # run(network_name='mumford0', num_nodes=30, 
    #     links_file="networks/Mumford0/mumford0_links.csv",
    #     demand_file="networks/Mumford0/mumford0_demand.csv",
    #     nodes_file="networks/Mumford0/mumford0_nodes.csv",
    #     num_population=100,
    #     num_of_generations=100,
    #     num_islands=4,
    #     migration_every_gen=8,
    #     num_migrants=4,
    #     num_routes=12,
    #     min_route=2,
    #     max_route=15)