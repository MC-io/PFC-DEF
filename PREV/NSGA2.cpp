#include "NSGA2.h"
#include <algorithm>
#include <iostream>
#include <set>
#include <time.h>
#include <random>
struct less_than_key
{
    inline bool operator() (const RouteSet& struct1, const RouteSet& struct2)
    {
        return (struct1.crowding_distance > struct2.crowding_distance);
    }
};

NSGA2::NSGA2(int generations, int num_of_individuals, TNDP & tndp, int num_of_routes, int num_of_tour_particips, float tournament_prob, int min_route, int max_route) : gen(std::random_device{}())
{
    this->generations = generations;
    this->num_of_individuals = num_of_individuals;
    this->network_graph = &tndp.network_graph;
    this->demand_matrix = &tndp.demand_matrix;
    this->network_size = tndp.size;
    this->population = Population();
    this->num_of_routes = num_of_routes;
    this->num_of_tour_particips = num_of_tour_particips;
    this->tournament_prob = tournament_prob;
    this->min_route = min_route;
    this->max_route = max_route;

    for (int i = 0; i < this->network_graph->nodes.size(); i++)
    {
        std::cout << "Nodo " << i << " -> ";
        for (int j = 0; j < this->network_graph->nodes[i].size(); j++)
        {
            std::cout << this->network_graph->nodes[i][j].to << ' ';
        }
        std::cout << '\n';
    }
    
}

void NSGA2::absorption(RouteSet & routeset)
{
    std::vector<int> routes_to_absorb;

    for (int i = routeset.routes.size() - 1; i >= 0; i--)
    {
        for (int j = 0; j < routeset.routes.size(); j++)
        {
            bool is_i_absorbed = std::find(routes_to_absorb.begin(), routes_to_absorb.end(), i) != routes_to_absorb.end();
            bool is_j_absorbed = std::find(routes_to_absorb.begin(), routes_to_absorb.end(), j) != routes_to_absorb.end();
            
            if (i != j && !is_j_absorbed && !is_i_absorbed && routeset.routes[i].nodes.size() <= routeset.routes[j].nodes.size())
            {
                for (int  k = 0; k < (routeset.routes[j].nodes.size() - routeset.routes[i].nodes.size() + 1); k++)
                {
                    std::vector<int> possible_subroute;
                    std::vector<int> possible_subroute_reverse;

                    for (int kk = k; kk < k + routeset.routes[i].nodes.size(); kk++)
                    {
                        possible_subroute.push_back(routeset.routes[j].nodes[kk]);
                        possible_subroute_reverse.insert(possible_subroute_reverse.begin(), routeset.routes[j].nodes[kk]);
                    }

                    if (possible_subroute == routeset.routes[i].nodes || possible_subroute_reverse == routeset.routes[i].nodes)
                    {
                        routes_to_absorb.push_back(i);
                    }
                }
            }
        }
    }
    for (auto index : routes_to_absorb)
    {
        routeset.routes.erase(routeset.routes.begin() + index);
    }
}

void NSGA2::explore(std::vector<bool> & visited, int node, int node_from, Route & route, int max_length)
{
    if (!visited[node])
    {
        visited[node] = true;
        std::cout << "EXPLORING in node " << node << "\n";
        std::cout << "It has " << this->network_graph->nodes[node].size() << " edges\n";
        std::vector<int> cand_nodes;
        for (int i = 0; i < this->network_graph->nodes[node].size(); i++)
        {
            std::cout << "for edge " << this->network_graph->nodes[node][i].to << '\n';
            if (this->network_graph->nodes[node][i].to != node_from && !visited[this->network_graph->nodes[node][i].to])
            {
                cand_nodes.push_back(this->network_graph->nodes[node][i].to);
            }
        }
        std::cout << "CAND NODES ADDED\n";


        if (cand_nodes.size() == 0)
        {
            return;
        }
        int neighbour = this->get_random_int(0, cand_nodes.size() - 1);
        // std::cout << neighbour << ' ' << cand_nodes.size() << '\n';

        std::cout << "NEIGHBOUR CREATED\n";

        route.add_node(cand_nodes[neighbour]);

        std::cout << "NEW NODE ADDED\n";


        if (route.size < max_length)
        {
            std::cout << "WILL CONTINUE EXPLORING\n";

            this->explore(visited, cand_nodes[neighbour], node, route, max_length);
        }
        std::cout << "ALL EXPLORING FINISHED\n";

    }
}
Route NSGA2::generate_random_route(std::vector<int> & not_elected_nodes)
{
    int random_start_point = this->get_random_int(0, this->network_size - 1);

    if (not_elected_nodes.size() > 0)
    {
        int pos = this->get_random_int(0, not_elected_nodes.size() - 1);
        random_start_point = not_elected_nodes[pos];
        not_elected_nodes.erase(std::remove(not_elected_nodes.begin(), not_elected_nodes.end(), random_start_point), not_elected_nodes.end());
    }
    int max_length = this->get_random_int(this->min_route, this->max_route);
    std::vector<bool> visited(this->network_size, false);
    Route random_route;
    random_route.add_node(random_start_point);
    
    int node = random_start_point;
    int node_from = -1;

    while (random_route.size < max_length)
    {
        if (!visited[node])
        {
            visited[node] = true;
            std::cout << "EXPLORING in node " << node << "\n";
            std::cout << "It has " << this->network_graph->nodes[node].size() << " edges\n";
            std::vector<int> cand_nodes;
            for (int i = 0; i < this->network_graph->nodes[node].size(); i++)
            {
                std::cout << "for edge " << this->network_graph->nodes[node][i].to << '\n';
                if (this->network_graph->nodes[node][i].to != node_from && !visited[this->network_graph->nodes[node][i].to])
                {
                    cand_nodes.push_back(this->network_graph->nodes[node][i].to);
                }
            }
            std::cout << "CAND NODES ADDED\n";
            if (cand_nodes.size() == 0)
            {
                break;
            }
            int neighbour = this->get_random_int(0, cand_nodes.size() - 1);
            // std::cout << neighbour << ' ' << cand_nodes.size() << '\n';

            std::cout << "NEIGHBOUR CREATED\n";

            random_route.add_node(cand_nodes[neighbour]);

            std::cout << "NEW NODE ADDED\n";

            node_from = node;
            node = cand_nodes[neighbour];

        }
    }

    return random_route;
}

std::vector<int> NSGA2::get_not_elected_nodes(const RouteSet & routeset)
{
    std::set<int> elected_nodes;

    for (const auto & route : routeset.routes)
    {
        for (auto a : route.nodes)
        {
            elected_nodes.insert(a);
        }
    }

    std::vector<int> not_elected_nodes;

    for (int i = 0; i < this->network_size; i++)
    {
        // Si i no sesta en elected_nodes
        if (!elected_nodes.count(i))
        {   
            not_elected_nodes.push_back(i);
        }   
    }

    return not_elected_nodes;
}


RouteSet NSGA2::generate_individual()
{
    RouteSet random_routeset;


    while (random_routeset.routes.size() < this->num_of_routes)
    {
        std::vector<int> not_elected_nodes;

        if (random_routeset.routes.size() > 0)
        {
            not_elected_nodes = this->get_not_elected_nodes(random_routeset);
        }
        while (random_routeset.routes.size() < this->num_of_routes)
        {
            Route random_route = this->generate_random_route(not_elected_nodes);
            random_routeset.routes.push_back(random_route);
        }
        this->absorption(random_routeset);
    }

    // for (int i = 0; i < this->num_of_routes; i++)
    // {
    //     Route random_route = this->generate_random_route();
    //     random_routeset.add_route(random_route);
    // }
    return random_routeset;
}

Population NSGA2::initialize_population()
{
    Population population;

    for (int i = 0; i < this->num_of_individuals; i++)
    {
        RouteSet individual = this->generate_individual();
        individual.calculate_objectives(*(this->network_graph), *(this->demand_matrix));
        population.all_population.push_back(individual);
    }
    return population;
}

void NSGA2::fast_non_dominated_sort(Population & population)
{
    this->population.fronts = std::vector<std::vector<RouteSet>>(1, std::vector<RouteSet>{});
    for (auto & individual: population.all_population)
    {
        individual.domination_count = 0;
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
    while (i < population.fronts.size() && population.fronts[i].size() > 0)
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

std::vector<RouteSet> NSGA2::create_children(Population & population)
{
    std::cout << "CREATING OFFSPRING\n";
    std::vector<RouteSet> children;
    while (children.size() < population.all_population.size())
    {
        std::cout << "creating parents\n";
        RouteSet parent1 = this->tournament(population);
        RouteSet parent2 = this->tournament(population);
        std::cout << "parents\n";
        std::cout << parent1.routes[0].nodes[0] << '\n';
        std::cout << parent2.routes[0].nodes[0] << '\n';


        while (parent1.equals(parent2))
        {
            parent2 = this->tournament(population);
        }
        std::cout << "parents created\n";

        std::vector<RouteSet> offspring = this->crossover(parent1, parent2);
        RouteSet child1 = offspring[0];
        RouteSet child2 = offspring[1];

        std::cout << "children created\n";

        this->mutate(child1);
        this->mutate(child2);
        std::cout << "children mutated\n";

        child1.calculate_objectives(*(this->network_graph), *(this->demand_matrix));
        child2.calculate_objectives(*(this->network_graph), *(this->demand_matrix));

        children.push_back(child1);
        children.push_back(child2);
    }
    std::cout << "FINISHED OFFSPRING\n";

    return children;
}


RouteSet NSGA2::tournament(Population & population)
{
    std::vector<RouteSet> participants;
    std::vector<bool> taken(population.all_population.size(), false);
    
    int n = 0;
    while (n < num_of_tour_particips)
    {
        int participant = this->get_random_int(0, population.all_population.size() - 1);
        while (taken[participant])
        {
            participant =  this->get_random_int(0, population.all_population.size() - 1);
        }
        participants.push_back(population.all_population[participant]);
        n++;
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
    int n = this->get_random_int(0, 100000);
    float p = (float) n / 100000.f;
    return p <= prob;
}

std::vector<RouteSet> NSGA2::crossover(RouteSet & parent1, RouteSet & parent2)
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

void NSGA2::mutate(RouteSet & routeset)
{
    for (const auto & node : routeset.routes[0].nodes)
    {
        for (int i = 1; i < routeset.routes.size(); i++)
        {
            int end_point = routeset.routes[i].nodes.size() - 1;
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
    std::cout << "HASTA ACA\n";

    for (auto & front : this->population.fronts)
    {
        this->calculate_crowding_distance(front);
    }    
    std::vector<RouteSet> children = this->create_children(this->population);
    Population * returned_population = nullptr; 

    for (int g = 0; g < this->generations; g++)
    {   
        std::cout << "Generacion " << g + 1 << ":\n";
        this->population.all_population.insert(this->population.all_population.end(), children.begin(), children.end());
        std::cout << "EMPEZANDO FNDS\n";
        this->fast_non_dominated_sort(this->population);
        std::cout << "TERMINANDO FNDS\n";

        Population new_population;
        int front_num = 0;
        std::cout << "EMPEZANDO BUCLE CROWD DIST\n";

        while (new_population.all_population.size() + this->population.fronts[front_num].size() <= this->num_of_individuals)
        {
            this->calculate_crowding_distance(this->population.fronts[front_num]);
            for (auto & rs: this->population.fronts[front_num])
            {
                new_population.all_population.push_back(rs);
            }
            front_num++;
        }
        std::cout << "TERMINANDO BUCLE CROWD DIST\n";
        std::cout << "EMPEZANDO OTRO CROWD DIST\n";
        this->calculate_crowding_distance(this->population.fronts[front_num]);
        std::cout << "TERMINANDO OTRO CROWD DIST\n";
        

        std::cout << "SORT\n";
        std::sort(this->population.fronts[front_num].begin(), this->population.fronts[front_num].end(), less_than_key());
        std::cout << "EXTEND\n";
        std::cout << new_population.all_population.size() << " " << this->population.fronts[front_num].size() << ' ' << this->population.fronts.size() << '\n';
        std::cout << front_num << '\n';
        new_population.all_population.insert(new_population.all_population.end(), this->population.fronts[front_num].begin(), this->population.fronts[front_num].end());
        // for (int i = 0; i < this->num_of_individuals - new_population.all_population.size(); i++)
        // {
        //     new_population.all_population.push_back(this->population.fronts[front_num][i]);
        // }
        
        std::cout << "CHANGE\n";
        returned_population = &this->population;
        this->population = new_population;

        std::cout << "EMPEZANDO OTRO FNDS\n";

        this->fast_non_dominated_sort(this->population);
        std::cout << "TERMINADO OTRO FNDS\n";


        std::cout << "EMPEZANDO OTRO bucle de crow dist\n";

        for (auto & front : this->population.fronts)
        {
            this->calculate_crowding_distance(front);
        }
        std::cout << "TERMINANDO OTRO bucle de crow dist\n";

        children = this->create_children(this->population);
    
        # pragma omp barrier
        // Se realizara migracion
        if (g % 2 == 0)
        {
            // Migracion aleatoria
        }

    }
    return returned_population->fronts[0]; 
}  



double NSGA2::calculate_user_cost(const RouteSet & rs)
{
    int total_time = 0;
    for (const auto & route : rs.routes)
    {
        for (int i = 0; i < route.size - 1; i++)
        {
            int nw_x = 0;
            for (const auto & edge : this->network_graph->nodes[route.nodes[i]])
            {
                if (edge.to == route.nodes[i + 1])
                {
                    nw_x = edge.value;
                }
            }
            total_time += (*this->demand_matrix)[route.nodes[i]][route.nodes[i + 1]] * nw_x;
        }
    }
    return total_time;
}

double NSGA2::calculate_coverage(const RouteSet & rs)
{
    double total_demand = 0;
    for (int i = 0; i < this->demand_matrix->size(); i++)
    {
        for (int j = 0; j < this->demand_matrix->size(); j++)
        {
            total_demand += (*this->demand_matrix)[i][j];
        }
    }
    double coverage = 0;

    for (const auto & route : rs.routes)
    {
        for (int i = 0; i < route.size; i++)
        {
            for (int j = i + 1; j < route.size; j++)
            {
                coverage += (*this->demand_matrix)[i][j];
            }
        }
    }

    return coverage / total_demand;
}

void NSGA2::calculate_objectives(RouteSet & rs)
{
    rs.objectives = {this->calculate_user_cost(rs), this->calculate_coverage(rs)};
}