#include "Route.h"

Route::Route()
{
    this->size = 0;
}

void Route::add_node(int node)
{
    this->nodes.push_back(node);
    this->size++;
}