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
        self.root.configure(bg="#23272e")
        self.grafo = Grafo()

        # Frame principal
        main_frame = tk.Frame(root, bg="#23272e")
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Título
        titulo = tk.Label(main_frame, text="Planificador de Rutas DFS", font=("Segoe UI", 18, "bold"), bg="#23272e", fg="#f8f8f2")
        titulo.pack(pady=(0, 15))

        # Entrada de paradas
        entry_frame = tk.Frame(main_frame, bg="#23272e")
        entry_frame.pack(fill=tk.X, pady=5)
        self.label = tk.Label(entry_frame, text="Parada (origen,destino):", bg="#23272e", fg="#f8f8f2", font=("Segoe UI", 11))
        self.label.pack(side=tk.LEFT, padx=(0, 8))
        self.entry = tk.Entry(entry_frame, width=30, font=("Segoe UI", 11))
        self.entry.pack(side=tk.LEFT, padx=5)
        self.agregar_btn = tk.Button(entry_frame, text="Agregar", command=self.agregar_parada, bg="#50fa7b", fg="#23272e", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, activebackground="#40c96b")
        self.agregar_btn.pack(side=tk.LEFT, padx=5)
        self.cargar_btn = tk.Button(entry_frame, text="Cargar CSV", command=self.cargar_csv, bg="#8be9fd", fg="#23272e", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, activebackground="#6ad0e6")
        self.cargar_btn.pack(side=tk.LEFT, padx=5)

        # Botones de acción
        action_frame = tk.Frame(main_frame, bg="#23272e")
        action_frame.pack(fill=tk.X, pady=10)
        self.buscar_btn = tk.Button(action_frame, text="Buscar Ruta DFS", command=self.buscar_ruta, bg="#ffb86c", fg="#23272e", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, activebackground="#e6a65c")
        self.buscar_btn.pack(side=tk.LEFT, padx=5)
        self.mostrar_grafo_btn = tk.Button(action_frame, text="Mostrar Grafo", command=self.mostrar_grafo, bg="#bd93f9", fg="#23272e", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, activebackground="#a883e6")
        self.mostrar_grafo_btn.pack(side=tk.LEFT, padx=5)

        # Texto de resultados
        self.texto = tk.Text(main_frame, height=7, width=60, bg="#282a36", fg="#f8f8f2", font=("Consolas", 10), relief=tk.FLAT, borderwidth=5)
        self.texto.pack(pady=10, fill=tk.X)

        # Frame para el grafo
        self.grafo_frame = tk.Frame(main_frame, bg="#44475a", bd=2, relief=tk.GROOVE)
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

# ...existing code...

    def pedir_estacion(self, titulo, mensaje):
        dialog = tk.Toplevel(self.root)
        dialog.title(titulo)
        dialog.configure(bg="#23272e")
        dialog.grab_set()  # Hace modal la ventana

        label = tk.Label(dialog, text=mensaje, bg="#23272e", fg="#f8f8f2", font=("Segoe UI", 11))
        label.pack(padx=20, pady=(20, 10))

        entry = tk.Entry(dialog, width=30, font=("Segoe UI", 11))
        entry.pack(padx=20, pady=10)
        entry.focus_set()

        resultado = {"valor": None}

        def aceptar():
            resultado["valor"] = entry.get().strip()
            dialog.destroy()

        btn = tk.Button(dialog, text="Aceptar", command=aceptar, bg="#50fa7b", fg="#23272e", font=("Segoe UI", 10, "bold"), relief=tk.FLAT, activebackground="#40c96b")
        btn.pack(pady=(0, 20))

        dialog.bind("<Return>", lambda event: aceptar())
        dialog.wait_window()
        return resultado["valor"]

# ...existing code...

    def buscar_ruta(self):
        inicio = self.pedir_estacion("Inicio", "Estación de inicio:")
        fin = self.pedir_estacion("Fin", "Estación de destino:")
        if inicio and fin:
            ruta = dfs(self.grafo, inicio, fin)
            if ruta:
                self.texto.insert(tk.END, f"Ruta DFS: {' -> '.join(ruta)}\n")
            else:
                messagebox.showinfo("Info", "No se encontró ruta.")

# ...existing code...
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
        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color='#50fa7b', node_size=1200, font_size=11, font_weight='bold', edge_color='#8be9fd', ax=ax)
        ax.set_title("Visualización del Grafo de Paradas", fontsize=13, color="#f8f8f2")
        ax.set_facecolor("#282a36")
        fig.patch.set_facecolor("#282a36")
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