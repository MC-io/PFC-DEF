#ifndef __ROUTESET_H__
#define __ROUTESET_H__

#include "Route.h"
#include "Graph.h"
class RouteSet
{
public:
    std::vector<Route> routes;
    int size;
    std::vector<double> objectives;
    int rank;
    double crowding_distance;
    int domination_count;
    std::vector<RouteSet> dominated_solutions;

    RouteSet();
    bool dominates(RouteSet other_individual);
    void add_route(Route & route);
    
    Graph convert_to_graph(Graph & graph);

    float user_cost(Graph & graph, std::vector<std::vector<int>> & demand_matrix)
    {
        Graph routeset_graph = this->convert_to_graph(graph);
        int total_demand = 0;
        int dt = 0;
        int count = 0;

        for (int i = 0; i < demand_matrix.size(); i++)
        {
            for (int j = i; j < demand_matrix.size(); j++)
            {
                if (i != j)
                {
                    int t = routeset_graph.get_shortest_path_length(i, j);
                    if (t >= 0)
                    {
                        total_demand += demand_matrix[i][j];
                        dt + demand_matrix[i][j] * t;
                    }
                    else
                    {
                        count++;
                    }
                }
            }
        }
        return dt / (float)total_demand + count / (demand_matrix.size() / 2.f);
    }


    float find_operator_cost(Graph & graph, std::vector<std::vector<int>> & demand_matrix)
    {
        float cost_sum = 0.f;
        for (auto route: this->routes)
        {
            for (int i = 0; i < route.nodes.size() - 1; i++)
            {
                cost_sum += graph.get_edge(route.nodes[i], route.nodes[i + 1])->value;
            }
        }
        return cost_sum;
    }

    void calculate_objectives(Graph & graph, std::vector<std::vector<int>> & demand_matrix)
    {
        this->objectives = {this->user_cost(graph, demand_matrix), this->find_operator_cost(graph, demand_matrix)};
    }

    bool operator< (const RouteSet &other) const {
        return this->crowding_distance < other.crowding_distance;
    }

    bool equals(const RouteSet & rhs)
    {
        if (this->routes.size() != rhs.routes.size()) return false;
        for (int i = 0; i < this->routes.size(); i++)
        {
            if (rhs.routes[i].nodes != this->routes[i].nodes)
            {
                return false;
            }
        }
        return true;
    }
};

#endif
