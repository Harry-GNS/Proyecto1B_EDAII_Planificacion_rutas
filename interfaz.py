import tkinter as tk
from tkinter import messagebox, filedialog
import matplotlib.pyplot as plt
import networkx as nx
from grafo import Grafo
from dfs import dfs


class TransporteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Planificador de Rutas DFS")
        self.grafo = Grafo()

        # Widgets
        self.label = tk.Label(root, text="Ingrese paradas (origen,destino):")
        self.label.pack()

        self.entry = tk.Entry(root, width=40)
        self.entry.pack()

        self.agregar_btn = tk.Button(root, text="Agregar Parada", command=self.agregar_parada)
        self.agregar_btn.pack()

        self.cargar_btn = tk.Button(root, text="Cargar CSV", command=self.cargar_csv)
        self.cargar_btn.pack()

        self.buscar_btn = tk.Button(root, text="Buscar Ruta DFS", command=self.buscar_ruta)
        self.buscar_btn.pack()

        self.texto = tk.Text(root, height=10, width=50)
        self.texto.pack()
        self.buscar_btn = tk.Button(root, text="Buscar Ruta DFS", command=self.buscar_ruta)
        self.buscar_btn.pack()

        self.mostrar_grafo_btn = tk.Button(root, text="Mostrar Grafo", command=self.mostrar_grafo)
        self.mostrar_grafo_btn.pack()

        self.texto = tk.Text(root, height=10, width=50)
        self.texto.pack()

    def agregar_parada(self):
        datos = self.entry.get().strip()
        if ',' not in datos:
            messagebox.showerror("Error", "Formato: origen,destino")
            return
        origen, destino = datos.split(',')
        self.grafo.agregar_arista(origen.strip(), destino.strip())
        self.texto.insert(tk.END, f"Agregado: {origen} -> {destino}\n")
        self.entry.delete(0, tk.END)

    def cargar_csv(self):
        archivo = filedialog.askopenfilename(filetypes=[("CSV", "*.csv")])
        if archivo:
            with open(archivo, 'r') as f:
                for linea in f:
                    origen, destino = linea.strip().split(',')
                    self.grafo.agregar_arista(origen, destino)
                    self.texto.insert(tk.END, f"Cargado: {origen} -> {destino}\n")

    def buscar_ruta(self):
        inicio = tk.simpledialog.askstring("Inicio", "Estación de inicio:")
        fin = tk.simpledialog.askstring("Fin", "Estación de destino:")
        if inicio and fin:
            ruta = dfs(self.grafo, inicio, fin)
            if ruta:
                self.texto.insert(tk.END, f"Ruta DFS: {' -> '.join(ruta)}\n")
            else:
                messagebox.showinfo("Info", "No se encontró ruta.")
    def mostrar_grafo(self):
        G = nx.Graph()

        # Agregar nodos y aristas al grafo de NetworkX
        for nombre, nodo in self.grafo.nodos.items():
            G.add_node(nombre)
            for adyacente in nodo.adyacentes:
                G.add_edge(nombre, adyacente.nombre)

        # Dibujar el grafo
        plt.figure(figsize=(8, 6))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1500, font_size=10, font_weight='bold', edge_color='gray')
        plt.title("Visualización del Grafo de Paradas")
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = TransporteApp(root)
    root.mainloop()