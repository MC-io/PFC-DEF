#include "Graph.h"

Graph::Graph()
{
    this->size = 0;
}


Graph::Graph(int size)
{
    this->size = size;
    this->nodes = std::vector<std::vector<Edge>>(size, std::vector<Edge>());
}

void Graph::add_edge(int a, int b, int value)
{
    this->nodes[a].push_back(Edge(b, value));
}