from migration import Migration
from TNDP import TNDP
from nsga2 import NSGAII
import time

import matplotlib.pyplot as plt
import numpy as np

def get_reference_point(pareto_front):
    worst_f1 = 0
    for sol in pareto_front:
        if sol.objectives[0] > worst_f1:
            worst_f1 = sol.objectives[0]

    worst_f2 = 0
    for sol in pareto_front:
        if sol.objectives[1] > worst_f2:
            worst_f2 = sol.objectives[1]

    return [worst_f1 * 1.2, worst_f2 * 1.2]

def calculate_hypervolume(pareto_front_list):

    reference_point = get_reference_point(pareto_front_list)

    func = [i.objectives for i in pareto_front_list]

    pareto_front = [[i[0], i[1]] for i in func]
    
    pareto_front = np.array(pareto_front)
    reference_point = np.array(reference_point)

    if pareto_front.shape[1] != len(reference_point):
        raise ValueError("The dimensions of the Pareto front and reference point do not match.")

    pareto_front = pareto_front[np.argsort(-pareto_front[:, 0])]

    hypervolume = 0.0
    previous_point = reference_point.copy()

    for point in pareto_front:
        volume = np.prod(previous_point - point)
        hypervolume += volume

        previous_point = point

    return hypervolume

def run_parallel(network_name, num_nodes, links_file, demand_file, nodes_file, num_routes, num_population, num_of_generations, num_islands, migration_every_gen, num_migrants, min_route, max_route):
    tndp = TNDP(num_nodes)

    tndp.read_network_from_file(links_file)
    tndp.read_demand_matrix_from_file(demand_file)


    start = time.time()

    nsga = Migration(num_population=num_population, num_of_generations=num_of_generations, num_islands=num_islands, 
                        migration_every_gen=migration_every_gen, num_migrants=num_migrants, tndp=tndp, num_of_routes=num_routes,
                        num_of_tour_particips=2, tournament_prob=0.9, min_route=min_route, max_route=max_route)        

    final_population = nsga.run()
    hypervolume = calculate_hypervolume(final_population)
    print(f"Hipervolumen: {hypervolume}")
    func = [i.objectives for i in final_population]

    user_cost = [i[0] for i in func]
    operator_cost = [i[1] for i in func]


    avg_user_cost = sum(user_cost) / len(user_cost)
    avg_operator_cost = sum(operator_cost) / len(operator_cost)

    print("Costo de Usuario promedio: {}".format(avg_user_cost))
    print("Costo de operador promedio: {}".format(avg_operator_cost))
    
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


def run_sequential(network_name, num_nodes, links_file, demand_file, nodes_file, num_routes, num_of_individuals, generations, min_route, max_route, all_hv=[]):
    tndp = TNDP(num_nodes)

    tndp.read_network_from_file(links_file)
    tndp.read_demand_matrix_from_file(demand_file)


    start = time.time()

    nsga = NSGAII(num_of_individuals=num_of_individuals, generations=generations,
                   tndp=tndp, num_of_routes=num_routes, num_of_tour_particips=2,
                tournament_prob=0.9, min_route=min_route, max_route=max_route)        

    final_population = nsga.run(all_hv)
    hypervolume = calculate_hypervolume(final_population)
    print(f"Hipervolumen: {hypervolume}")
    func = [i.objectives for i in final_population]

    user_cost = [i[0] for i in func]
    operator_cost = [i[1] for i in func]


    avg_user_cost = sum(user_cost) / len(user_cost)
    avg_operator_cost = sum(operator_cost) / len(operator_cost)

    print("Costo de Usuario promedio: {}".format(avg_user_cost))
    print("Costo de Operador promedio: {}".format(avg_operator_cost))
    
    end = time.time()
    
    print(f"Tiempo total de ejecucion: {end - start}")

    best_sol_f1 = None
    lowest_f1 = 9999999
    for sol in final_population:
        if sol.objectives[0] < lowest_f1:
            lowest_f1 = sol.objectives[0]
            best_sol_f1 = sol
    print(lowest_f1)
    # best_sol_f1.show_plot(links_file, nodes_file)

    best_sol_f2 = None
    lowest_f2 = 9999999
    for sol in final_population:
        if sol.objectives[1] < lowest_f2:
            lowest_f2 = sol.objectives[1]
            best_sol_f2 = sol
    print(lowest_f2)
    # best_sol_f2.show_plot(links_file, nodes_file)

    # plt.xlabel('Costo de Usuario', fontsize=15)
    # plt.ylabel('Costo de Operador', fontsize=15)
    # plt.scatter(user_cost, operator_cost)
    # plt.savefig(f'{network_name}.png')
    # plt.show()

if __name__ == "__main__":

    # run_sequential(network_name='mandl', num_nodes=15, 
    #     links_file="networks/Mandl/mandl_links.csv",
    #     demand_file="networks/Mandl/mandl_demand.csv",
    #     nodes_file="networks/Mandl/mandl_nodes.csv",
    #     num_of_individuals=100,
    #     generations=300,
    #     num_routes=6,
    #     min_route=2,
    #     max_route=8)
    
    # run_parallel(network_name='mandl', num_nodes=15, 
    #     links_file="networks/Mandl/mandl_links.csv",
    #     demand_file="networks/Mandl/mandl_demand.csv",
    #     nodes_file="networks/Mandl/mandl_nodes.csv",
    #     num_population=200,
    #     num_of_generations=100,
    #     num_islands=10,
    #     migration_every_gen=10,
    #     num_migrants=5,
    #     num_routes=6,
    #     min_route=2,
    #     max_route=8)
    
    # for _ in range(5):
    #     all_hv = []
    #     run_sequential(network_name='mandl', num_nodes=15, 
    #         demand_file="networks/Mandl/mandl_demand.csv",
    #         links_file="networks/Mandl/mandl_links.csv",
    #         nodes_file="networks/Mandl/mandl_nodes.csv",
    #         num_of_individuals=100,
    #         generations=100,
    #         num_routes=6,
    #         min_route=2,
    #         max_route=8,
    #         all_hv=all_hv)      
        
    # sum_hv = []
    # for i in range(100):
    #     sum_hv.append(0)   
    #     for j in range(len(all_hv)):
    #         sum_hv[i] += all_hv[j][i]
    #     sum_hv[i] = sum_hv[i] / 5
    
    # generations = np.arange(1, 101)
    # plt.figure(figsize=(10, 6))
    # plt.plot(generations, sum_hv, label="Hipervolumen", color="blue", marker="o")
    # plt.title("Grafico de Convergencia: Indicador de Hipervolumen")
    # plt.xlabel("Generacion")
    # plt.ylabel("Hipervolumen")
    # plt.grid(True)
    # plt.legend()
    # plt.show()

    # run_sequential(network_name='mumford0', num_nodes=30, 
    #     links_file="networks/Mumford0/mumford0_links.csv",
    #     demand_file="networks/Mumford0/mumford0_demand.csv",
    #     nodes_file="networks/Mumford0/mumford0_nodes.csv",
    #     num_of_individuals=100,
    #     generations=100,
    #     num_routes=12,
    #     min_route=2,
    #     max_route=15)


    # run_parallel(network_name='mumford0', num_nodes=30, 
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

    # run_sequential(network_name='mumford1', num_nodes=70, 
    #     links_file="networks/Mumford1/mumford1_links.csv",
    #     demand_file="networks/Mumford1/mumford1_demand.csv",
    #     nodes_file="networks/Mumford1/mumford1_nodes.csv",
    #     num_of_individuals=100,
    #     generations=100,
    #     num_routes=15,
    #     min_route=10,
    #     max_route=30)


    # run_parallel(network_name='mumford1', num_nodes=70, 
    #     links_file="networks/Mumford1/mumford1_links.csv",
    #     demand_file="networks/Mumford1/mumford1_demand.csv",
    #     nodes_file="networks/Mumford1/mumford1_nodes.csv",
    #     num_population=100,
    #     num_of_generations=100,
    #     num_islands=4,
    #     migration_every_gen=8,
    #     num_migrants=4,
    #     num_routes=15,
    #     min_route=10,
    #     max_route=30)




    # run_sequential(network_name='mumford2', num_nodes=110, 
    #     links_file="networks/Mumford2/mumford2_links.csv",
    #     demand_file="networks/Mumford2/mumford2_demand.csv",
    #     nodes_file="networks/Mumford2/mumford2_nodes.csv",
    #     num_of_individuals=50,
    #     generations=50,
    #     num_routes=56,
    #     min_route=10,
    #     max_route=22)


    # run_parallel(network_name='mumford2', num_nodes=110, 
    #     links_file="networks/Mumford2/mumford2_links.csv",
    #     demand_file="networks/Mumford2/mumford2_demand.csv",
    #     nodes_file="networks/Mumford2/mumford2_nodes.csv",
    #     num_population=50,
    #     num_of_generations=50,
    #     num_islands=5,
    #     migration_every_gen=5,
    #     num_migrants=2,
    #     num_routes=56,
    #     min_route=10,
    #     max_route=22)


    run_sequential(network_name='mumford3', num_nodes=127, 
        links_file="networks/Mumford3/mumford3_links.csv",
        demand_file="networks/Mumford3/mumford3_demand.csv",
        nodes_file="networks/Mumford3/mumford3_nodes.csv",
        num_of_individuals=30,
        generations=30,
        num_routes=60,
        min_route=12,
        max_route=25)


    # run_parallel(network_name='mumford3', num_nodes=127, 
    #     links_file="networks/Mumford3/mumford3_links.csv",
    #     demand_file="networks/Mumford3/mumford3_demand.csv",
    #     nodes_file="networks/Mumford3/mumford3_nodes.csv",
    #     num_population=30,
    #     num_of_generations=30,
    #     num_islands=3,
    #     migration_every_gen=5,
    #     num_migrants=2,
    #     num_routes=60,
    #     min_route=12,
    #     max_route=25)