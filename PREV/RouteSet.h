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
    bool operator< (const RouteSet &other) const {
        return this->crowding_distance < other.crowding_distance;
    }

    bool equals(const RouteSet & rhs)
    {
        if (this->size != rhs.size) return false;
        for (int i = 0; i < this->size; i++)
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
