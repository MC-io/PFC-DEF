
import matplotlib.pyplot as plt
from TNDP import TNDP
from nsga2 import NSGAII
import time

def main():
    num_nodes = 110
    tndp = TNDP(num_nodes)

    tndp.read_network_from_file("networks\\Mumford2\\mumford2_links.csv")
    tndp.read_demand_matrix_from_file("networks\\Mumford2\\mumford2_demand.csv")

    g_user_cost = []
    g_coverage = []

    start = time.time()

    for nroutes in range(56,57):
        nsga = NSGAII(num_of_individuals=50, generations=50, tndp=tndp, num_of_routes=nroutes, num_of_tour_particips=2, tournament_prob=0.9, min_route=10, max_route=22  )
        """
        for i in range(len(nsga.graph.nodes)):
            for edge in nsga.graph.nodes[i]:
                print("{} - {}".format(i, edge.to))
        """
        final_population = nsga.run()


        func = [i.objectives for i in final_population]

        user_cost = [i[0] for i in func]
        coverage = [i[1] for i in func]

        g_user_cost.extend(user_cost)
        g_coverage.extend(coverage)

    avg_user_cost = sum(g_user_cost) / len(g_user_cost)
    avg_coverage = sum(g_coverage) / len(g_coverage)

    print("Costo de Usuario promedio: {}".format(avg_user_cost))
    print("Cobertura promedio: {}".format(avg_coverage))
    end = time.time()
    print(f"Tiempo total de ejecucion: {end - start}")

    plt.xlabel('Costo de Usuario', fontsize=15)
    plt.ylabel('Cobertura', fontsize=15)
    plt.scatter(g_user_cost, g_coverage)
    plt.savefig('modern_mumford2.png')
    plt.show()


if __name__ == "__main__":
    main()