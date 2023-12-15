#include "NSGA2.h"
#include <algorithm>

struct less_than_key
{
    inline bool operator() (const RouteSet& struct1, const RouteSet& struct2)
    {
        return (struct1.crowding_distance > struct2.crowding_distance);
    }
};

NSGA2::NSGA2(int generations, int num_of_individuals, TNDP tndp, int num_of_routes, int num_of_tour_particips, float tournament_prob)
{
    this->generations = generations;
    this->num_of_individuals = num_of_individuals;
    this->network_graph = tndp.network_graph;
    this->demand_matrix = tndp.demand_matrix;
    this->network_size = tndp.size;
    this->population = Population();
    this->num_of_routes = num_of_routes;
    this->num_of_tour_particips = num_of_tour_particips;
    this->tournament_prob = tournament_prob;
}
void NSGA2::explore(std::vector<bool> & visited, int node, int node_from, Route route, int max_length)
{
    if (!visited[node])
    {
        std::vector<int> cand_nodes;
        for (const auto x : this->network_graph.nodes[node])
        {
            if (x.to != node_from && !visited[x.to])
            {
                cand_nodes.push_back(x.to);
            }
        }
        if (cand_nodes.size() == 0)
        {
            return;
        }

        int neighbour = rand() % cand_nodes.size();
        route.nodes.push_back(cand_nodes[neighbour]);

        if (route.size < max_length)
        {
            this->explore(visited, cand_nodes[neighbour], node, route, max_length);
        }
    }
}
Route NSGA2::generate_random_route()
{
    int random_start_point = rand() % this->network_size;
    int max_length = rand() % 10 + 4;
    std::vector<bool> visited(this->network_size, false);
    Route random_route;
    random_route.nodes.push_back(random_start_point);
    this->explore(visited, random_start_point, -1, random_route, max_length);
}
RouteSet NSGA2::generate_individual()
{
    RouteSet random_routeset = RouteSet(this->network_graph, this->demand_matrix);
    for (int i = 0; i < this->num_of_routes; i++)
    {
        Route random_route = this->generate_random_route();
        random_routeset.routes.push_back(random_route);
    }
    return random_routeset;
}

Population NSGA2::initialize_population()
{
    Population population;
    for (int i = 0; i < this->num_of_individuals; i++)
    {
        RouteSet individual = this->generate_individual();
        individual.calculate_objectives();
        population.all_population.push_back(individual);
    }
    return population;
}

void NSGA2::fast_non_dominated_sort(Population & population)
{
    this->population.fronts = {{}};
    for (auto & individual: population.all_population)
    {
        individual.domination_count = 0;
        individual.dominated_solutions = {};
        for (auto & other_individual : population.all_population)
        {
            if (individual.dominates(other_individual))
            {
                individual.dominated_solutions.push_back(other_individual);
            }
            else if (other_individual.dominates(individual))
            {
                individual.domination_count++;
            }
        }
        if (individual.domination_count == 0)
        {
            individual.rank = 0;
            population.fronts[0].push_back(individual);
        }
    }
    int i = 0;
    while (population.fronts[i].size() > 0)
    {
        std::vector<RouteSet> temp;
        for (auto & individual : population.fronts[i])
        {
            for (auto & other_individual : individual.dominated_solutions)
            {
                other_individual.domination_count--;
                if (other_individual.domination_count == 0)
                {
                    other_individual.rank = i + 1;
                    temp.push_back(other_individual);
                }
            }
        }
        i++;
        population.fronts.push_back(temp);
    }
}

void NSGA2::calculate_crowding_distance(std::vector<RouteSet> & front)
{
    if (front.size() > 0)
    {
        int solutions_num = front.size();
        for (auto & individual : front)
        {
            individual.crowding_distance = 0;
        }

        for (int m = 0; m < front[0].objectives.size(); m++)
        {
            front[0].crowding_distance = INT32_MAX;
            front[solutions_num - 1].crowding_distance = INT32_MAX;
            std::vector<double> m_values;
            for (const auto & individual : front)
            {
                m_values.push_back(individual.objectives[m]);
            }
            auto it_max = max_element(std::begin(m_values), std::end(m_values));
            auto it_min = min_element(std::begin(m_values), std::end(m_values));

            int scale = *it_max - *it_min;

            if (scale == 0) scale = 1;

            for (int i = 1; i < solutions_num - 1; i++)
            {
                front[i].crowding_distance += (front[i + 1].objectives[m] - front[i - 1].objectives[m]) / scale;
            }
        }
    }
}

int NSGA2::crowding_operator(const RouteSet & individual, const RouteSet & other_individual)
{
    if ((individual.rank < other_individual.rank) || ((individual.rank == other_individual.rank) &&
     individual.crowding_distance > other_individual.crowding_distance))
    {
        return 1;
    }
    return -1;
}

std::vector<RouteSet> NSGA2::create_children(Population population)
{
    std::vector<RouteSet> children;
    while (children.size() < population.all_population.size())
    {
        RouteSet parent1 = this->tournament(population);
        RouteSet parent2 = this->tournament(population);

        while (parent1.routes == parent2.routes)
        {
            parent2 = this->tournament(population);
        }
        std::vector<RouteSet> offspring = this->crossover(parent1, parent2);
        RouteSet child1 = offspring[0];
        RouteSet child2 = offspring[1];
        this->mutate(child1);
        this->mutate(child2);
        child1.calculate_objectives();
        child2.calculate_objectives();

        children.push_back(child1);
        children.push_back(child2);
    }
    return children;
}


RouteSet NSGA2::tournament(Population population)
{
    std::vector<RouteSet> participants;
    std::vector<bool> taken(population.all_population.size(), false);
    
    int n = 0;
    while (n < num_of_tour_particips)
    {
        int participant = rand() % population.all_population.size();
        while (taken[participant])
        {
            participant = rand() % population.all_population.size();
        }
        taken[participant] = true;
    }
    RouteSet * best = nullptr;
    for (auto & participant : participants)
    {
        if (best == nullptr || (this->crowding_operator(participant, *best) == 1 && this->choose_with_prob(this->tournament_prob)))
        {
            best = &participant;
        }
    }

    return *best;

}

bool NSGA2::choose_with_prob(float prob)
{
    int n = rand() % 100000;
    float p = (float) n / 100000.f;
    return p <= prob;
}

std::vector<RouteSet> NSGA2::crossover(RouteSet parent1, RouteSet parent2)
{   
    RouteSet child1 = parent1;
    RouteSet child2 = parent2;

    int longest_route_ind1 = child1.routes[0].size;
    int pos_longest_route_ind1 = 0;

    for (int i = 0; i < child1.routes.size(); i++)
    {
        if (child1.routes[i].nodes.size() > longest_route_ind1)
        {
            longest_route_ind1 = child1.routes[i].nodes.size();
            pos_longest_route_ind1 = 1;
        }
    }
    Route parent1_longest_route = child1.routes[pos_longest_route_ind1];
    child1.routes.erase(child1.routes.begin() + pos_longest_route_ind1);

    
    int longest_route_ind2 = child2.routes[0].size;
    int pos_longest_route_ind2 = 0;

    for (int i = 0; i < child2.routes.size(); i++)
    {
        if (child2.routes[i].nodes.size() > longest_route_ind2)
        {
            longest_route_ind2 = child2.routes[i].nodes.size();
            pos_longest_route_ind2 = 1;
        }
    }
    Route parent2_longest_route = child2.routes[pos_longest_route_ind2];
    child2.routes.erase(child2.routes.begin() + pos_longest_route_ind2);

    child1.routes.push_back(parent2_longest_route);
    child2.routes.push_back(parent1_longest_route);

    return std::vector<RouteSet>{child1, child2};
}

void NSGA2::mutate(RouteSet routeset)
{
    for (const auto & node : routeset.routes[0].nodes)
    {
        for (int i = 1; i < routeset.routes.size(); i++)
        {
            int end_point = routeset.routes[i].nodes.size();
            if (node == routeset.routes[i].nodes[0])
            {
                if (routeset.routes[i].nodes.size() > 2)
                {
                    routeset.routes[i].nodes.erase(routeset.routes[i].nodes.begin());
                }
            }
            else if (node == routeset.routes[i].nodes[end_point])
            {
                if (routeset.routes[i].nodes.size() > 2)
                {
                    routeset.routes[i].nodes.erase(routeset.routes[i].nodes.begin() + end_point);
                }
            }
        }
    }
}

std::vector<RouteSet> NSGA2::run()
{
    this->population = this->initialize_population();
    this->fast_non_dominated_sort(this->population);

    for (auto & front : this->population.fronts)
    {
        this->calculate_crowding_distance(front);
    }    
    std::vector<RouteSet> children = this->create_children(this->population);
    Population * returned_population = nullptr; 

    for (int g = 0; g < this->generations; g++)
    {   
        this->population.all_population.insert(this->population.all_population.end(), children.begin(), children.end());
        this->fast_non_dominated_sort(this->population);
        Population new_population;
        int front_num = 0;

        while (new_population.all_population.size() + this->population.fronts[front_num].size() <= this->num_of_individuals)
        {
            this->calculate_crowding_distance(this->population.fronts[front_num]);
            for (auto & rs: this->population.fronts[front_num])
            {
                new_population.all_population.push_back(rs);
            }
            front_num++;
        }
        this->calculate_crowding_distance(this->population.fronts[front_num]);
        std::sort(this->population.fronts[front_num].begin(), this->population.fronts[front_num].end(), less_than_key());
        new_population.all_population.insert(new_population.all_population.end(), this->population.fronts[front_num].begin(), this->population.fronts[front_num].end());
        returned_population = &this->population;
        this->population = new_population;
        this->fast_non_dominated_sort(this->population);
        for (auto front : this->population.fronts)
        {
            this->calculate_crowding_distance(front);
        }
        children = this->create_children(this->population);
    }
    return returned_population->fronts[0]; 
}  

