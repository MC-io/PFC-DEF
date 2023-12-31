import matplotlib.pyplot as plt
from TNDP import TNDP
from genetic import GeneticAlgorithm

def main():
    num_nodes = 30

    tndp = TNDP(num_nodes)

    tndp.read_network_from_file("networks\\Mumford0\\mumford0_links.csv")
    tndp.read_demand_matrix_from_file("networks\\Mumford0\\mumford0_demand.csv")

    g_user_cost = []
    g_coverage = []
    for nroutes in range(10,14):
        ga = GeneticAlgorithm(num_of_individuals=50, generations=20, tndp=tndp, num_of_routes=nroutes, num_of_tour_particips=2, tournament_prob=0.9, min_route=2, max_route=15)
        """
        for i in range(len(nsga.graph.nodes)):
            for edge in nsga.graph.nodes[i]:
                print("{} - {}".format(i, edge.to))
        """
        final_population = ga.run()


        func = [i.objectives for i in final_population]

        user_cost = [i[0] for i in func]
        coverage = [i[1] for i in func]

        g_user_cost.extend(user_cost)
        g_coverage.extend(coverage)

    avg_user_cost = sum(g_user_cost) / len(g_user_cost)
    avg_coverage = sum(g_coverage) / len(g_coverage)

    print(len(g_user_cost))

    print("Costo de Usuario promedio: {}".format(avg_user_cost))
    print("Cobertura promedio: {}".format(avg_coverage))


    plt.xlabel('Costo de Usuario', fontsize=15)
    plt.ylabel('Cobertura', fontsize=15)
    plt.scatter(g_user_cost, g_coverage)
    plt.savefig('traditional_mumford0.png')
    plt.show()

if __name__ == "__main__":
    main()