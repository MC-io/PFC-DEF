#ifndef __NSGA_2_H__
#define __NSGA_2_H__

#include "Graph.h"
#include "Population.h"
#include "TNDP.h"
#include <random>

class NSGA2
{
public:
    int generations;
    int num_of_individuals;
    Graph * network_graph;
    std::vector<std::vector<int>> * demand_matrix;
    Population population;
    int num_of_routes;
    int network_size;
    int num_of_tour_particips;
    float tournament_prob;
    int min_route;
    int max_route;
    std::mt19937 gen;

    NSGA2(int generations, int num_of_individuals, TNDP & tndp, int num_of_routes, int num_of_tour_particips, float tournament_prob, int min_route, int max_route);
    int get_random_int(int min, int max)
    {
        std::uniform_int_distribution<> dist(min, max);
        return dist(gen);
    }
    void absorption(RouteSet & routeset);
    void explore(std::vector<bool> & visited, int node, int node_from, Route & route, int max_length);
    Route generate_random_route(std::vector<int> & not_elected_nodes);
    std::vector<int> get_not_elected_nodes(const RouteSet & routeset);
    RouteSet generate_individual();
    Population initialize_population();
    void fast_non_dominated_sort(Population & population);
    void calculate_crowding_distance(std::vector<RouteSet> & front);
    int crowding_operator(const RouteSet & individual, const RouteSet & other_individual);
    std::vector<RouteSet> create_children(Population & population);
    RouteSet tournament(Population & population);
    bool choose_with_prob(float prob);
    std::vector<RouteSet> crossover(RouteSet & parent1, RouteSet & parent2);
    void mutate(RouteSet & routeset);
    double calculate_user_cost(const RouteSet & rs);
    double calculate_coverage(const RouteSet & rs);
    void calculate_objectives(RouteSet & rs);


    
    
    std::vector<RouteSet> run();

};

#endif