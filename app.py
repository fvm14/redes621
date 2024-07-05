from flask import Flask, render_template, request, redirect, url_for
from grafica import Grafica
from bellmanford import BellmanFord

app = Flask(__name__)

@app.route('/')
def index():
    grafo = Grafica()
    if grafo.error:
        return render_template('index2.html', error_message=grafo.error)
    image_data = grafo.graficar()
    return render_template('index2.html', image_data=image_data)

@app.route('/dijkstra', methods=['GET', 'POST'])
def dijkstra():
    grafo = Grafica()
    if grafo.error:
        return render_template('index.html', error_message=grafo.error)
    
    if request.method == 'POST':
        return redirect(url_for('calcular_rutaDijkstra'))
    else:
        image_data = grafo.graficar()
        return render_template('index.html', image_data=image_data)

@app.route('/calcular_ruta', methods=['GET', 'POST'])
def calcular_rutaDijkstra():
    grafo = Grafica()
    if grafo.error:
        return render_template('index.html', error_message=grafo.error)

    if request.method == 'POST':
        nodo_inicial = int(request.form['nodo_inicial'])
        nodo_final = int(request.form['nodo_final'])

        # Verificar que los nodos existen en el grafo
        if nodo_inicial not in grafo.vertices or nodo_final not in grafo.vertices:
            error_message = "Uno o ambos nodos no existen en el grafo. Por favor, ingrese nodos válidos."
            return render_template('index.html', error_message=error_message, image_data=grafo.graficar())

        # Aplicar algoritmo de Dijkstra
        grafo.dijkstra(nodo_inicial)
        camino, distancia = grafo.camino(nodo_inicial, nodo_final)

        # Generar imagen con el camino encontrado
        image_data = grafo.graficarCamino(camino)

        return render_template('ruta.html', camino=camino, distancia=distancia, image_data=image_data)

    return redirect(url_for('index'))

@app.route('/bellmanFord', methods=['GET', 'POST'])
def bellmanFord():
    bellman_ford_grafo = BellmanFord()
    if request.method == 'POST':
        return redirect(url_for('calcular_rutaBellmanFord'))
    else:
        image_data = bellman_ford_grafo.graficar()
        return render_template('bellmanford.html', image_data=image_data)

@app.route('/calcular_rutaBellmanFord', methods=['GET', 'POST'])
def calcular_rutaBellmanFord():
    bellman_ford_grafo = BellmanFord()

    if request.method == 'POST':
        nodo_inicial = int(request.form['nodo_inicial'])
        nodo_final = int(request.form['nodo_final'])

        # Verificar que los nodos existen en el grafo
        if nodo_inicial not in bellman_ford_grafo.G.nodes or nodo_final not in bellman_ford_grafo.G.nodes:
            error_message = "Uno o ambos nodos no existen en el grafo. Por favor, ingrese nodos válidos."
            return render_template('bellmanford.html', error_message=error_message, image_data=bellman_ford_grafo.graficar())

        # Aplicar algoritmo de Bellman-Ford
        camino, distancia = bellman_ford_grafo.bellman_ford(nodo_inicial, nodo_final)

        # Generar imagen con el camino encontrado
        image_data = bellman_ford_grafo.graficarCamino(camino)

        return render_template('rutabf.html', camino=camino, distancia=distancia, image_data=image_data)

    return redirect(url_for('bellmanFord'))

@app.route('/grafo_graficado')
def grafo_graficado():
    grafo = Grafica()
    image_data = grafo.graficar()
    return render_template('graficooriginal.html', image_data=image_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
