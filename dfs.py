from grafo import Grafo

def dfs(grafo, inicio, fin):
    start = grafo.nodos.get(inicio)
    end = grafo.nodos.get(fin)
    if not start or not end:
        return None

    pila = [(start, [start.nombre])]  # (nodo_actual, ruta_actual)
    while pila:
        nodo, ruta = pila.pop()
        if nodo == end:
            return ruta
        if not nodo.visitado:
            nodo.visitado = True
            for adyacente in nodo.adyacentes:
                if not adyacente.visitado:
                    pila.append((adyacente, ruta + [adyacente.nombre]))
    return None