#ifndef __POPULATION_H__
#define __POPUALTION_H__

#include "RouteSet.h"

class Population
{
public:
    std::vector<RouteSet> all_population;
    std::vector<std::vector<RouteSet>> fronts;
};

#endif