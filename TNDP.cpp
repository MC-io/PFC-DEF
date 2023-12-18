#include "TNDP.h"
#include <fstream>


TNDP::TNDP()
{
    this->size = 0;
}

TNDP::TNDP(int size)
{
    this->size = size;
    this->network_graph = Graph(this->size);

    for (int i = 0; i < size; i++)
    {
        this->demand_matrix.push_back(std::vector<int>{});

        for (int j = 0; j < size; j++)
        {
            this->demand_matrix[i].push_back(0);
        }
    }
}

void TNDP::read_network_from_file(std::string filename)
{
    std::ifstream file;
    file.open(filename.c_str());
    std::string notimportant;
    file >> notimportant;
    int from = 0;
    int to = 0;
    int travel_time = 0;
    char comma;
    while (file >> from)
    {
        file >> comma >> to >> comma >> travel_time;
        this->network_graph.add_edge(from - 1, to - 1, travel_time);
    }
    file.close();
}

void TNDP::read_demand_matrix_from_file(std::string filename)
{
    std::ifstream file;
    file.open(filename.c_str());
    std::string notimportant;
    file >> notimportant;
    int from = 0;
    int to = 0;
    int demand = 0;
    char comma;
    while (file >> from)
    {
        file >> comma >> to >> comma >> demand;
        this->demand_matrix[from - 1][to - 1] = demand;
    }
    file.close();
}