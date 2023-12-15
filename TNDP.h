#ifndef __TNDP_H__
#define __TNDP_H__

#include "Graph.h"
#include <string>

class TNDP
{
public:
    int size;
    Graph network_graph;
    std::vector<std::vector<int>> demand_matrix;
    TNDP(int size);
    TNDP();

    void read_network_from_file(std::string filename);
    void read_demand_matrix_from_file(std::string filename);
};

#endif