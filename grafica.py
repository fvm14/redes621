import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64

class Vertice:
    def __init__(self, i):
        self.id = i
        self.vecinos = []
        self.visitados = False
        self.padre = None
        self.distancia = float('inf')

    def agregarVecinos(self, v, p):
        if v not in [vecino[0] for vecino in self.vecinos]:
            self.vecinos.append([v, p])

class Grafica:
    def __init__(self):
        self.vertices = {}
        self.configurar_grafica()

    def agregarVertice(self, id):
        if id not in self.vertices:
            self.vertices[id] = Vertice(id)

    def agregarArista(self, a, b, p):
        if a in self.vertices and b in self.vertices:
            self.vertices[a].agregarVecinos(b, p)
            self.vertices[b].agregarVecinos(a, p)

    def minimo(self, lista):
        if len(lista) > 0:
            m = self.vertices[lista[0]].distancia
            v = lista[0]
            for e in lista:
                if m > self.vertices[e].distancia:
                    m = self.vertices[e].distancia
                    v = e
            return v

    def imprimirGrafica(self):
        for v in self.vertices:
            print("La distancia del vertice " + str(v) + " es " +
                  str(self.vertices[v].distancia) + " llegando desde " +
                  str(self.vertices[v].padre))

    def camino(self, a, b):
        camino = []
        actual = b
        while actual is not None:
            camino.insert(0, actual)
            actual = self.vertices[actual].padre
        return [camino, self.vertices[b].distancia]

    def dijkstra(self, a):
        if a in self.vertices:
            self.vertices[a].distancia = 0
            actual = a
            noVisitados = []

            for v in self.vertices:
                if v != a:
                    self.vertices[v].distancia = float('inf')
                self.vertices[v].padre = None
                noVisitados.append(v)

            while len(noVisitados) > 0:
                for vecino in self.vertices[actual].vecinos:
                    if not self.vertices[vecino[0]].visitados:
                        if self.vertices[actual].distancia + vecino[1] < self.vertices[vecino[0]].distancia:
                            self.vertices[vecino[0]].distancia = self.vertices[actual].distancia + vecino[1]
                            self.vertices[vecino[0]].padre = actual
                self.vertices[actual].visitados = True
                noVisitados.remove(actual)
                actual = self.minimo(noVisitados)

    def graficar(self):
        G = nx.Graph()
        for v in self.vertices:
            G.add_node(v)
            for vecino in self.vertices[v].vecinos:
                G.add_edge(v, vecino[0], weight=vecino[1])

        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, font_size=10, font_weight='bold')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()  # Cerrar la figura para limpiar el estado
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return data

    def graficarCamino(self, camino):
        G = nx.Graph()
        for v in self.vertices:
            G.add_node(v)
            for vecino in self.vertices[v].vecinos:
                G.add_edge(v, vecino[0], weight=vecino[1])

        pos = nx.spring_layout(G)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=700, font_size=10, font_weight='bold')

        path_edges = list(zip(camino, camino[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='r', width=2)

        # Mostrar etiquetas de peso en las aristas del camino
        path_labels = {(camino[i], camino[i+1]): G[camino[i]][camino[i+1]]['weight'] for i in range(len(camino)-1)}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=path_labels)

        buf = io.BytesIO()
        plt.savefig(buf, format="png")
        plt.close()  # Cerrar la figura para limpiar el estado
        data = base64.b64encode(buf.getbuffer()).decode("ascii")
        return data

    def configurar_grafica(self):
        df = pd.read_csv('data.csv')
        for node in set(df['nodo_origen']).union(set(df['nodo_destino'])):
            self.agregarVertice(node)
        for index, row in df.iterrows():
            self.agregarArista(row['nodo_origen'], row['nodo_destino'], row['peso'])
