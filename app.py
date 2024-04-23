# -*- coding: utf-8 -*-
from flask import Flask, render_template
from DFS import buscar_solucion_DFS, obtener_resultado_DFS
from Puzzle_Lineal import buscar_solucion_BFS, obtener_resultado_Puzzle
from Vuelos_Busqueda import DFS_prof_iter, nodo_inicial
import heapq

# Especifica la ubicación de la carpeta de plantillas
app = Flask(__name__)

# Funciones de Dijkstra
def dijkstra(graph, start):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    queue = [(0, start)]
    previous_nodes = {}

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))
                previous_nodes[neighbor] = current_node

    return previous_nodes

def shortest_path(graph, start, end):
    previous_nodes = dijkstra(graph, start)
    path = []
    current_node = end

    while current_node != start:
        path.insert(0, current_node)
        current_node = previous_nodes[current_node]

    path.insert(0, start)
    return path

@app.route('/')
def index():
    # Problema DFS
    estado_inicial_dfs = [4, 2, 3, 1]
    solucion_dfs = [1, 2, 3, 4]
    nodo_solucion_dfs = buscar_solucion_DFS(estado_inicial_dfs, solucion_dfs)
    resultado_dfs = obtener_resultado_DFS(nodo_solucion_dfs)
    
    # Problema Puzzle Lineal
    estado_inicial_puzzle = [4, 2, 3, 1]
    solucion_puzzle = [1, 2, 3, 4]
    nodo_solucion_puzzle = buscar_solucion_BFS(estado_inicial_puzzle, solucion_puzzle)
    resultado_puzzle = obtener_resultado_Puzzle(nodo_solucion_puzzle)
    
    # Problema Vuelos
    estado_inicial_vuelos = 'EDO.MEX'
    solucion_vuelos = 'HIDALGO'
    visitados = []  # Lista para almacenar los nodos visitados en la búsqueda de vuelos
    resultado_vuelos = DFS_prof_iter(nodo_inicial, solucion_vuelos, visitados)
    
    # Calcular camino más corto
    graph = {
        1: {2: 4},
        2: {3: 2},
        3: {5: 4},
        5: {7: 20},
        7: {}
    }
    start_node = 1
    end_node = 7
    shortest_path_nodes = shortest_path(graph, start_node, end_node)
    
    return render_template('resultado.html', resultado_dfs=resultado_dfs, resultado_puzzle=resultado_puzzle, resultado_vuelos=resultado_vuelos, nodos_visitados=visitados, shortest_path_nodes=shortest_path_nodes)

if __name__ == '__main__':
    app.run(debug=True)



