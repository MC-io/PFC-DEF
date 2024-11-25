#include "Graph.h"
#include <queue>
#include <limits>
#include <functional>
#include <utility>

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

Edge * Graph::get_edge(int a, int b)
{
    for (auto & edge: this->nodes[a])
    {
        if (edge.to == b)
        {
            return &edge;
        }
    }
    return nullptr;
}

int Graph::get_shortest_path_length(int start, int end)
{
    // std::vector<float> distances;
    // for (int i = 0; i < this->nodes.size(); i++)
    // {
    //     distances.push_back(FLT_MAX);
    // }

    std::vector<int> distances(nodes.size(), std::numeric_limits<int>::max());
    distances[start] = 0;

    std::priority_queue<std::pair<int, int>, std::vector<std::pair<int, int>>, std::greater<>> priority_queue;
    priority_queue.emplace(0, start);

    while (!priority_queue.empty()) 
    {
        std::pair<int, int> my_pair = priority_queue.top();
        int current_distance = my_pair.first;
        int currentNode = my_pair.second;

        priority_queue.pop();

        if (currentNode == end) 
        {
            return current_distance;
        }

        if (current_distance > distances[currentNode]) 
        {
            continue;
        }

        for (const auto& edge : nodes[currentNode]) 
        {
            int newDistance = current_distance + edge.value;
            if (newDistance < distances[edge.to]) 
            {
                distances[edge.to] = newDistance;
                priority_queue.emplace(newDistance, edge.to);
            }
        }
    }

    return -1;


}
