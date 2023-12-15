#include "RouteSe.h"
#include "Graph.h"

RouteSet::RouteSet()
{
    this->size = 0;
    this->network_graph = nullptr;
    this->demand_matrix = nullptr;

}
RouteSet::RouteSet(Graph & network_graph, std::vector<std::vector<int>> & demand_matrix)
{
    this->network_graph = &network_graph;
    this->demand_matrix = &demand_matrix;
    this->size = network_graph.size;
}

bool RouteSet::dominates(RouteSet other_individual)
{
    bool and_condition = true;
    bool or_condition = false;

    for (int i = 0; i < this->objectives.size(); i++)
    {
        and_condition = and_condition && (this->objectives[i] <= other_individual.objectives[i]);
        or_condition = or_condition || (this->objectives[i] <= other_individual.objectives[i]);
    }
    return and_condition && or_condition;
}
double RouteSet::user_cost()
{
    int total_time = 0;
    for (const auto & route : this->routes)
    {
        for (int i = 0; i < route.size - 1; i++)
        {
            int nw_x = 0;
            for (const auto & edge : this->network_graph->nodes[route.nodes[i]])
            {
                if (edge.to == route.nodes[i + 1])
                {
                    nw_x = edge.value;
                }
            }
            total_time += (*this->demand_matrix)[route.nodes[i]][route.nodes[i + 1]] * nw_x;
        }
    }
    return total_time;
}

double RouteSet::find_coverage()
{
    double total_demand = 0;
    for (int i = 0; i < this->demand_matrix->size(); i++)
    {
        for (int j = 0; j < this->demand_matrix->size(); j++)
        {
            total_demand += (*this->demand_matrix)[i][j];
        }
    }
    double coverage = 0;

    for (const auto & route : routes)
    {
        for (int i = 0; i < route.size; i++)
        {
            for (int j = i + 1; j < route.size; j++)
            {
                coverage += (*this->demand_matrix)[i][j];
            }
        }
    }

    return coverage / total_demand;
}

void RouteSet::calculate_objectives()
{
    this->objectives = {this->user_cost(), this->find_coverage()};
}