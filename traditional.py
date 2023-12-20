import matplotlib.pyplot as plt
from TNDP import TNDP
from genetic import GeneticAlgorithm

def main():
    num_nodes = 127

    tndp = TNDP(num_nodes)

    tndp.read_network_from_file("networks\\Mumford3\\mumford3_links.csv")
    tndp.read_demand_matrix_from_file("networks\\Mumford3\\mumford3_demand.csv")

    g_user_cost = []
    g_coverage = []
    for nroutes in range(45,76,3):
        ga = GeneticAlgorithm(num_of_individuals=50, generations=5, tndp=tndp, num_of_routes=nroutes, num_of_tour_particips=2, tournament_prob=0.9)
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


    plt.xlabel('Costo de Usuario', fontsize=15)
    plt.ylabel('Cobertura', fontsize=15)
    plt.scatter(g_user_cost, g_coverage)
    plt.show()

if __name__ == "__main__":
    main()