import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64

class BellmanFord:
    def __init__(self):
        self.G = nx.Graph()  # Usamos un grafo no dirigido
        self.load_data()

    def load_data(self):
        df = pd.read_csv('data.csv')
        for node in set(df['nodo_origen']).union(set(df['nodo_destino'])):
            self.G.add_node(node)
        for index, row in df.iterrows():
            self.G.add_edge(row['nodo_origen'], row['nodo_destino'], weight=row['peso'])

    def bellman_ford(self, source, target):
        path = nx.bellman_ford_path(self.G, source, target, weight='weight')
        distance = nx.bellman_ford_path_length(self.G, source, target, weight='weight')
        return path, distance

    def graficar(self):
        pos = nx.spring_layout(self.G)
        labels = nx.get_edge_attributes(self.G, 'weight')
        plt.figure()
        nx.draw(self.G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_weight='bold', arrows=True, arrowsize=20)
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels)
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        image_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        return image_data

    def graficarCamino(self, path):
        pos = nx.spring_layout(self.G)
        labels = nx.get_edge_attributes(self.G, 'weight')
        plt.figure()
        nx.draw(self.G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_weight='bold')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=labels)
        
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(self.G, pos, edgelist=path_edges, edge_color='r', width=2)
        
        path_labels = {(path[i], path[i+1]): self.G[path[i]][path[i+1]]['weight'] for i in range(len(path)-1)}
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=path_labels)
        
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        image_data = base64.b64encode(buf.getvalue()).decode('utf-8')
        return image_data
