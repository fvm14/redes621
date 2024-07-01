import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

df = pd.read_csv('data.csv')

G = nx.Graph()

for node in set(df['nodo_origen']).union(set(df['nodo_destino'])):
    G.add_node(node)

for index, row in df.iterrows():
    G.add_edge(row['nodo_origen'], row['nodo_destino'], weight=row['peso'])

source = int(input("Ingrese el nodo de origen: "))
target = int(input("Ingrese el nodo de destino: "))
shortest_path = nx.bellman_ford_path(G, source, target, weight='weight')
shortest_distance = nx.bellman_ford_path_length(G, source, target, weight='weight')
print(f"La ruta más corta desde el nodo {source} al nodo {target} es: {shortest_path}")
print(f"La distancia más corta es: {shortest_distance}")

pos = nx.spring_layout(G)
labels = nx.get_edge_attributes(G, 'weight')
nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_weight='bold', arrows=True, arrowsize=20)
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

path_edges = list(zip(shortest_path, shortest_path[1:]))
nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)

path_labels = {(shortest_path[i], shortest_path[i+1]): G[shortest_path[i]][shortest_path[i+1]]['weight'] for i in range(len(shortest_path)-1)}
nx.draw_networkx_edge_labels(G, pos, edge_labels=path_labels)

plt.show()