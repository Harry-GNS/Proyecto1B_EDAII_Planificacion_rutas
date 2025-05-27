from grafo import Grafo

def dfs(grafo, inicio, fin):
    start = grafo.nodos.get(inicio)
    end = grafo.nodos.get(fin)
    if not start or not end:
        return None

    pila = [(start, [start.nombre])]  # (nodo_actual, ruta_actual)
    visitados = set()  # Conjunto para almacenar nodos visitados

    while pila:
        nodo, ruta = pila.pop()
        if nodo == end:
            return ruta
        
        if nodo.nombre not in visitados:  # Verifica si ya fue visitado
            visitados.add(nodo.nombre)  # Marca como visitado

            for adyacente in nodo.adyacentes:
                if adyacente.nombre not in visitados:
                    pila.append((adyacente, ruta + [adyacente.nombre]))

    return None
