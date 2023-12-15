#ifndef __ROUTE_H__
#define __ROUTE_H__

#include <vector>

class Route
{
public:
    std::vector<int> nodes;
    int size;
    Route();
    void add_node(int node);


};  

#endif