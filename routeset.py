from TNDP import Graph
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
class RouteSet:
    def __init__(self):
        self.routes = []
        self.objectives = None
        self.rank = None
        self.crowding_distance = None
        self.domination_count = None
        self.dominated_solutions = None
        self.features = None

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.features == other.features
        return False

    def dominates(self, other_individual):
        and_condition = True
        or_condition = False
        for first, second in zip(self.objectives, other_individual.objectives):
            and_condition = and_condition and first <= second
            or_condition = or_condition or first < second
        return (and_condition and or_condition)
    
    def user_cost(self, graph, demand_matrix):      # Reducir tiempo de viaje promedio de cada pasajero
        routeset_graph = self.convert_to_graph(graph)
        total_demand = 0
        dt = 0
        count = 0
        for i in range(len(demand_matrix)):
            for j in range(i, len(demand_matrix)):
                if i != j:
                    t = routeset_graph.get_shortest_path_length(i, j)
                    if t is not None:
                        total_demand += demand_matrix[i][j]
                        dt += demand_matrix[i][j] * t
                    else:
                        count += 1
        return dt / total_demand + count / (len(demand_matrix) / 2)

    def find_coverage(self, graph, demand_matrix):    
        total_demand = 0
        for i in range(len(demand_matrix)):
            for j in range(len(demand_matrix)):
                total_demand += demand_matrix[i][j]
        coverage = 0
        for route in self.routes:
            for i in range(len(route) - 1):
                for j in range(i + 1, len(route)):
                    coverage += demand_matrix[i][j]
        return coverage / total_demand * -1
    

    def find_operator_cost(self, graph, demand_matrix):
        cost_sum = 0
        for route in self.routes:
            for i in range(len(route) - 1):
                cost_sum += graph.get_edge(route[i], route[i + 1]).value
        return cost_sum

    def calculate_objectives(self, graph, demand_matrix):
        self.objectives = [self.user_cost(graph, demand_matrix), self.find_operator_cost(graph, demand_matrix)]


    def convert_to_graph(self, graph):
        routeset_graph = Graph(len(graph.nodes))
        for route in self.routes:
            for i in range(len(route) - 1):
                value = graph.get_edge(route[i], route[i + 1]).value
                routeset_graph.add_edge(route[i], route[i + 1], value)
                routeset_graph.add_edge(route[i + 1], route[i], value)
        return routeset_graph
    
    def show_plot(self, edges_file, nodes_file):
        pass

        # nodes_df = pd.read_csv(nodes_file)
        # edges_df = pd.read_csv(edges_file)

        # G = nx.Graph()  # Use nx.Graph() for undirected graphs

        # for _, row in nodes_df.iterrows():
        #     G.add_node(int(row['id']), pos=(row['lat'], row['lon']))

        # for _, row in edges_df.iterrows():
        #     G.add_edge(row['from'], row['to'], weight=row['travel_time'])

        # pos = nx.get_node_attributes(G, 'pos')

        # plt.figure(figsize=(8, 6))

        # for (source, target, weight) in G.edges(data='weight'):
        #     x1, y1 = pos[source]
        #     x2, y2 = pos[target]
        #     plt.text(
        #         (x1 + x2) / 2,
        #         (y1 + y2) / 2,
        #         str(weight),
        #         fontsize=8,
        #         color="red",
        #         ha='center',
        #         va='center',
        #     )

        # cmap = plt.get_cmap('tab10', len(self.routes))  # Use a discrete colormap
        # colors = [cmap(i) for i in range(len(self.routes))]
        # print(colors)



        # # Draw routes with different colors
        # for idx, route in enumerate(self.routes):
        #     G = nx.Graph()  # Use nx.Graph() for undirected graphs

        #     for _, row in nodes_df.iterrows():
        #         G.add_node(int(row['id']), pos=(row['lat'], row['lon']))

        #     for _, row in edges_df.iterrows():
        #         G.add_edge(row['from'], row['to'], weight=row['travel_time'])

        #     pos = nx.get_node_attributes(G, 'pos')

        #     plt.figure(figsize=(8, 6))

        #     for (source, target, weight) in G.edges(data='weight'):
        #         x1, y1 = pos[source]
        #         x2, y2 = pos[target]
        #         plt.text(
        #             (x1 + x2) / 2,
        #             (y1 + y2) / 2,
        #             str(weight),
        #             fontsize=8,
        #             color="red",
        #             ha='center',
        #             va='center',
        #         )
        #     route_edges = [(route[i] + 1, route[i + 1] + 1) for i in range(len(route) - 1)]
        #     nx.draw(
        #         G, pos, with_labels=True, node_color="skyblue", node_size=300, edge_color="gray", arrows=False, font_weight="bold", font_size=8
        #     )
        #     nx.draw_networkx_edges(G, pos, edgelist=route_edges, edge_color=[colors[idx]], arrows=False, width=5)


        # plt.show()
