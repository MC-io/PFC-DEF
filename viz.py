import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# Load the CSV files
nodes_file = "networks/Mumford0/mumford0_nodes.csv"  # Replace with your nodes CSV file name
edges_file = "networks/Mumford0/mumford0_links.csv"  # Replace with your edges CSV file name

nodes_df = pd.read_csv(nodes_file)
edges_df = pd.read_csv(edges_file)

# Create a graph
G = nx.Graph()  # Use nx.Graph() for undirected graphs

# Add nodes with positions
for _, row in nodes_df.iterrows():
    G.add_node(row['id'], pos=(row['lat'], row['lon']))

# Add edges with weights
for _, row in edges_df.iterrows():
    G.add_edge(row['from'], row['to'], weight=row['travel_time'])

# Extract node positions
pos = nx.get_node_attributes(G, 'pos')

# Draw nodes and edges
plt.figure(figsize=(8, 6))
# nx.draw(
#     G,
#     pos,
#     with_labels=True,
#     node_color="skyblue",
#     node_size=300,
#     edge_color="gray",
#     font_weight="bold",
#     arrows=False,
#     font_size=8,
# )

# Draw edge labels
for (source, target, weight) in G.edges(data='weight'):
    x1, y1 = pos[source]
    x2, y2 = pos[target]
    plt.text(
        (x1 + x2) / 2,
        (y1 + y2) / 2,
        str(weight),
        fontsize=8,
        color="red",
        ha='center',
        va='center',
    )

routes = [
    [6, 7, 17, 28],
    [12, 26, 29],
    [30, 3, 28],
    [8, 17, 11],
    [17, 8, 21]
]

cmap = plt.get_cmap('tab10', len(routes))  # Use a discrete colormap
colors = [cmap(i) for i in range(len(routes))]
print(colors)

nx.draw(
    G, pos, with_labels=True, node_color="skyblue", node_size=300, edge_color="gray", arrows=False, font_weight="bold", font_size=8
)

# Draw routes with different colors
for idx, route in enumerate(routes):
    route_edges = [(route[i], route[i + 1]) for i in range(len(route) - 1)]
    nx.draw_networkx_edges(G, pos, edgelist=route_edges, edge_color=[colors[idx]], arrows=False, width=5)


plt.title("Graph with Nodes and Edges")
plt.show()