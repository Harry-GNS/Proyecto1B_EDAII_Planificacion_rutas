from grafo import Grafo
from collections import deque

# BFS para encontrar la ruta más corta entre dos nodos en un grafo no dirigido
# Retorna la ruta como una lista de nombres de nodos, o None si no hay camino

def bfs_ruta_mas_corta(grafo, inicio, fin):
    start = grafo.nodos.get(inicio)
    end = grafo.nodos.get(fin)
    if not start or not end:
        return None

    visitados = set()
    cola = deque()
    padres = {}

    cola.append(start)
    visitados.add(start.nombre)
    padres[start.nombre] = None

    while cola:
        actual = cola.popleft()
        if actual == end:
            # Reconstruir la ruta desde el final hasta el inicio
            ruta = []
            while actual:
                ruta.append(actual.nombre)
                actual = grafo.nodos.get(padres[actual.nombre]) if padres[actual.nombre] else None
            return list(reversed(ruta))
        for adyacente in actual.adyacentes:
            if adyacente.nombre not in visitados:
                visitados.add(adyacente.nombre)
                padres[adyacente.nombre] = actual.nombre
                cola.append(adyacente)
    return None

# Ejemplo de uso (puedes borrar esto si lo usas desde main.py)
if __name__ == "__main__":
    g = Grafo()
    g.agregar_arista("A", "B")
    g.agregar_arista("A", "C")
    g.agregar_arista("B", "D")
    g.agregar_arista("C", "D")
    g.agregar_arista("D", "E")
    ruta = bfs_ruta_mas_corta(g, "A", "E")
    print("Ruta más corta de A a E:", ruta)
