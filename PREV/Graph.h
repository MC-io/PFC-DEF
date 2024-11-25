#ifndef __GRAPH_H__
#define __GRAPH_H__

#include <vector>
#include "Edge.h"

class Graph
{
public:
    std::vector<std::vector<Edge>> nodes;
    int size;

    Graph(int _size);
    Graph();

    void add_edge(int a, int b, int value);
    Edge * get_edge(int a, int b);
    int get_shortest_path_length(int start, int end);


};

#endif