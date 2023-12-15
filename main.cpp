#include "NSGA2.h"
#include <stdlib.h>
#include <time.h>
#include <iostream>

int main() 
{
    std::cout << "HOLAPASADEPUESDELSRAND\n";

    srand(time(NULL));
    std::cout << "HOLAPASADEPUESDELSRAND\n";
    int num_nodes = 15;
    TNDP tndp(num_nodes);
    std::cout << "HOLAPASADEPUESDETNDP\n";


    tndp.read_network_from_file("networks\\mandl_links.csv");
    tndp.read_demand_matrix_from_file("networks\\mandl_demand.csv");

    NSGA2 nsga(100, 50, tndp, 3, 2, 0.9);

    std::vector<RouteSet> final_population = nsga.run();


    return 0;
}