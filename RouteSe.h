#ifndef __ROUTESET_H__
#define __ROUTESET_H__

#include "Route.h"
#include "Graph.h"
class RouteSet
{
public:
    std::vector<Route> routes;
    int size;
    Graph * network_graph;
    std::vector<std::vector<int>> * demand_matrix;
    std::vector<double> objectives;
    int rank;
    double crowding_distance;
    int domination_count;
    std::vector<RouteSet> dominated_solutions;

    RouteSet();
    RouteSet(Graph & network_graph, std::vector<std::vector<int>> & demand_matrix);
    bool dominates(RouteSet other_individual);
    double user_cost();   
    double find_coverage();    
    void calculate_objectives();
    bool operator< (const RouteSet &other) const {
        return this->crowding_distance < other.crowding_distance;
    }
};

#endif
