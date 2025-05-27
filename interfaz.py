import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
from grafo import Grafo
from dfs import dfs

class TransporteApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Planificador de Rutas DFS")
        self.grafo = Grafo()

        # Frame principal
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Entrada de paradas
        entry_frame = tk.Frame(main_frame, bg="#f0f0f0")
        entry_frame.pack(fill=tk.X, pady=5)
        self.label = tk.Label(entry_frame, text="Ingrese paradas (origen,destino):", bg="#f0f0f0")
        self.label.pack(side=tk.LEFT)
        self.entry = tk.Entry(entry_frame, width=30)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.agregar_btn = tk.Button(entry_frame, text="Agregar Parada", command=self.agregar_parada, bg="#4caf50", fg="white")
        self.agregar_btn.pack(side=tk.LEFT, padx=5)
        self.cargar_btn = tk.Button(entry_frame, text="Cargar CSV", command=self.cargar_csv, bg="#2196f3", fg="white")
        self.cargar_btn.pack(side=tk.LEFT, padx=5)

        # Botones de acción
        action_frame = tk.Frame(main_frame, bg="#f0f0f0")
        action_frame.pack(fill=tk.X, pady=5)
        self.buscar_btn = tk.Button(action_frame, text="Buscar Ruta DFS", command=self.buscar_ruta, bg="#ff9800", fg="white")
        self.buscar_btn.pack(side=tk.LEFT, padx=5)
        self.mostrar_grafo_btn = tk.Button(action_frame, text="Mostrar Grafo", command=self.mostrar_grafo, bg="#9c27b0", fg="white")
        self.mostrar_grafo_btn.pack(side=tk.LEFT, padx=5)

        # Texto de resultados
        self.texto = tk.Text(main_frame, height=8, width=50, bg="#e3f2fd")
        self.texto.pack(pady=5, fill=tk.X)

        # Frame para el grafo
        self.grafo_frame = tk.Frame(main_frame, bg="#f0f0f0", bd=2, relief=tk.GROOVE)
        self.grafo_frame.pack(pady=5, fill=tk.BOTH, expand=True)
        self.canvas = None  # Para el canvas de matplotlib

    def agregar_parada(self):
        datos = self.entry.get().strip()
        if ',' not in datos:
            messagebox.showerror("Error", "Formato: origen,destino")
            return
        origen, destino = datos.split(',')
        self.grafo.agregar_arista(origen.strip(), destino.strip())
        self.texto.insert(tk.END, f"Agregado: {origen.strip()} -> {destino.strip()}\n")
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
        inicio = simpledialog.askstring("Inicio", "Estación de inicio:")
        fin = simpledialog.askstring("Fin", "Estación de destino:")
        if inicio and fin:
            ruta = dfs(self.grafo, inicio, fin)
            if ruta:
                self.texto.insert(tk.END, f"Ruta DFS: {' -> '.join(ruta)}\n")
            else:
                messagebox.showinfo("Info", "No se encontró ruta.")

    def mostrar_grafo(self):
        # Elimina el canvas anterior si existe
        if self.canvas:
            self.canvas.get_tk_widget().destroy()

        G = nx.Graph()
        for nombre, nodo in self.grafo.nodos.items():
            G.add_node(nombre)
            for adyacente in nodo.adyacentes:
                G.add_edge(nombre, adyacente.nombre)

        fig, ax = plt.subplots(figsize=(5, 4))
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=1200, font_size=10, font_weight='bold', edge_color='gray', ax=ax)
        ax.set_title("Visualización del Grafo de Paradas")
        ax.axis('off')

        self.canvas = FigureCanvasTkAgg(fig, master=self.grafo_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        plt.close(fig)  # Cierra la figura para evitar advertencias

# Elimina el bloque if __name__ == "__main__": si lo tienes en este archivo


if __name__ == "__main__":
    root = tk.Tk()
    app = TransporteApp(root)
    root.mainloop()