#include "RouteSet.h"
#include "Graph.h"

RouteSet::RouteSet()
{
    this->size = 0;
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

void RouteSet::add_route(Route & route)
{
    this->routes.push_back(route);
    this->size++;
}

Graph RouteSet::convert_to_graph(Graph & graph)
{
    Graph routeset_graph = Graph(graph.nodes.size());

    for (auto & route : this->routes)
    {
        for (int i = 0; i < route.nodes.size() - 1; i++)
        {
            float value = graph.get_edge(route.nodes[i], route.nodes[i + 1])->value;
            routeset_graph.add_edge(route.nodes[i], route.nodes[i + 1], value);
            routeset_graph.add_edge(route.nodes[i + 1], route.nodes[i], value);
        }
    }
    return routeset_graph;

}