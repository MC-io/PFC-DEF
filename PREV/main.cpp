#include "NSGA2.h"
#include <stdlib.h>
#include <time.h>
#include <iostream>
#include <random>
#include <omp.h>

int main() 
{
    int num_nodes = 15;
    TNDP tndp(num_nodes);
    tndp.read_network_from_file("C:\\Users\\pc\\Desktop\\8vo Semestre\\Proyecto Final de Carrera 1\\PFC-DEF\\networks\\Mandl\\mandl_links.csv");
    tndp.read_demand_matrix_from_file("C:\\Users\\pc\\Desktop\\8vo Semestre\\Proyecto Final de Carrera 1\\PFC-DEF\\networks\\Mandl\\mandl_demand.csv");


    for (int i = 0; i < num_nodes; i++)
    {
        std::cout << i << " -> ";
        for (int j = 0; j < tndp.network_graph.nodes[i].size(); j++)
        {
            std::cout << tndp.network_graph.nodes[i][j].to << ' ';
        }
        std::cout << '\n';
    }

    NSGA2 nsga(4, 5, tndp, 3, 2, 0.9, 4, 8);

    
    std::vector<RouteSet> final_population = nsga.run();
    
    
/*
    srand(time(NULL));
    std::cout << "HOLAPASADEPUESDELSRAND\n";
    int num_nodes = 15;
    TNDP tndp(num_nodes);
    std::cout << "HOLAPASADEPUESDETNDP\n";


    tndp.read_network_from_file("networks\\mandl_links.csv");
    tndp.read_demand_matrix_from_file("networks\\mandl_demand.csv");

    NSGA2 nsga(100, 50, tndp, 3, 2, 0.9);

    std::vector<RouteSet> final_population = nsga.run();
*/

    return 0;
}