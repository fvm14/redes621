from flask import Flask, render_template, request, redirect, url_for
from grafica import Grafica  # Importa la clase Grafica del archivo grafica.py

app = Flask(__name__)

# Crear una instancia de la clase Grafica
grafo = Grafica()

# Rutas para las páginas
@app.route('/')
def index():
    # Generar la imagen del grafo vacío
    image_data = grafo.graficar()

    return render_template('index.html', image_data=image_data)

@app.route('/calcular_ruta', methods=['GET', 'POST'])
def calcular_ruta():
    global grafo  # Declarar grafo como global para poder accederlo y modificarlo

    if request.method == 'POST':
        nodo_inicial = int(request.form['nodo_inicial'])
        nodo_final = int(request.form['nodo_final'])

        # Aplicar algoritmo de Dijkstra
        grafo.dijkstra(nodo_inicial)
        camino, distancia = grafo.camino(nodo_inicial, nodo_final)

        # Generar imagen con el camino encontrado
        image_data = grafo.graficarCamino(camino)

        # Reiniciar estado de los vértices para futuros cálculos
        grafo = Grafica()

        return render_template('ruta.html', camino=camino, distancia=distancia, image_data=image_data)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
