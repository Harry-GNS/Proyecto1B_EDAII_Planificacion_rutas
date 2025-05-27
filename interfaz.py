import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QFileDialog, QMessageBox, QInputDialog, QFrame, QSizePolicy
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from grafo import Grafo
from dfs import dfs

class GrafoCanvas(FigureCanvas):
    def __init__(self, grafo):
        self.fig, self.ax = plt.subplots(figsize=(7, 6), dpi=120)
        super().__init__(self.fig)
        self.set_grafo(grafo)

    def set_grafo(self, grafo):
        self.ax.clear()
        G = nx.Graph()
        for nombre, nodo in grafo.nodos.items():
            G.add_node(nombre)
            for adyacente in nodo.adyacentes:
                G.add_edge(nombre, adyacente.nombre)
        pos = nx.spring_layout(G, seed=42)
        nx.draw(
            G, pos,
            with_labels=False,
            node_color="#E0E7EF",
            node_size=320,
            edge_color="#B0BEC5",
            linewidths=1.5,
            ax=self.ax
        )
        label_pos = {k: (v[0], v[1]+0.09) for k, v in pos.items()}
        nx.draw_networkx_labels(
            G, label_pos,
            labels={n: n for n in G.nodes()},
            font_size=9,
            font_color="#FFFFFF",
            font_weight='light',
            bbox=dict(boxstyle="round,pad=0.25", fc="#23272e", ec="#B0BEC5", lw=1, alpha=0.85),
            ax=self.ax
        )
        self.ax.set_title(
            "Grafo de Paradas",
            fontsize=11,
            color="#B0BEC5",
            fontweight='light',
            pad=8
        )
        self.ax.set_facecolor("#23272e")
        self.fig.patch.set_facecolor("#23272e")
        self.ax.axis('off')
        self.draw()

class TransporteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Planificador de Rutas DFS")
        self.setStyleSheet("""
            QWidget { background: #23272e; }
            QLabel, QLineEdit, QTextEdit {
                color: #e0e7ef;
                font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
                font-size: 11pt;
                font-weight: 400;
            }
            QPushButton {
                background: #23272e;
                color: #e0e7ef;
                border: 1px solid #44475a;
                border-radius: 7px;
                padding: 7px 18px;
                font-size: 11pt;
                font-weight: 500;
            }
            QPushButton:hover {
                background: #44475a;
                color: #ffffff;
            }
            QLineEdit, QTextEdit {
                background: #282a36;
                border: 1px solid #44475a;
                border-radius: 6px;
                font-size: 11pt;
            }
            QTextEdit { padding: 8px; }
        """)
        self.grafo = Grafo()
        self.init_ui()
        self.showMaximized()

    def init_ui(self):
        main_layout = QHBoxLayout(self)

        # --- LADO IZQUIERDO: Controles ---
        left_panel = QVBoxLayout()
        left_panel.setSpacing(18)

        title = QLabel("Planificador de Rutas DFS")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        left_panel.addWidget(title)

        # Entrada de paradas
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Parada (origen,destino)")
        left_panel.addWidget(self.entry)

        self.add_btn = QPushButton("Agregar")
        self.add_btn.clicked.connect(self.agregar_parada)
        left_panel.addWidget(self.add_btn)

        self.csv_btn = QPushButton("Cargar CSV")
        self.csv_btn.clicked.connect(self.cargar_csv)
        left_panel.addWidget(self.csv_btn)

        self.buscar_btn = QPushButton("Buscar Ruta DFS")
        self.buscar_btn.clicked.connect(self.buscar_ruta)
        left_panel.addWidget(self.buscar_btn)

        # Texto de resultados de agregados/cargados
        self.texto = QTextEdit()
        self.texto.setReadOnly(True)
        self.texto.setFixedHeight(90)
        left_panel.addWidget(self.texto)

        # Línea separadora
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        line.setStyleSheet("color: #44475a; background: #44475a; max-height: 2px;")
        left_panel.addWidget(line)

        # Texto de resultado de búsqueda DFS (abajo, separado)
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setFixedHeight(40)
        left_panel.addWidget(self.resultado)

        # Espaciador para empujar todo hacia arriba
        left_panel.addStretch(1)

        # --- LADO DERECHO: Grafo ---
        self.grafo_canvas = GrafoCanvas(self.grafo)
        self.grafo_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # --- Distribución principal ---
        main_layout.addLayout(left_panel, stretch=1)
        main_layout.addWidget(self.grafo_canvas, stretch=3)

    def agregar_parada(self):
        datos = self.entry.text().strip()
        if ',' not in datos:
            QMessageBox.critical(self, "Error", "Formato: origen,destino")
            return
        origen, destino = datos.split(',')
        self.grafo.agregar_arista(origen.strip(), destino.strip())
        self.texto.append(f"Agregado: {origen.strip()} -> {destino.strip()}")
        self.entry.clear()
        self.grafo_canvas.set_grafo(self.grafo)

    def cargar_csv(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Abrir CSV", "", "CSV Files (*.csv)")
        if archivo:
            with open(archivo, 'r') as f:
                for linea in f:
                    origen, destino = linea.strip().split(',')
                    self.grafo.agregar_arista(origen, destino)
                    self.texto.append(f"Cargado: {origen} -> {destino}")
            self.grafo_canvas.set_grafo(self.grafo)

    def pedir_estacion(self, titulo, mensaje):
        texto, ok = QInputDialog.getText(self, titulo, mensaje)
        return texto.strip() if ok and texto else None

    def buscar_ruta(self):
        inicio = self.pedir_estacion("Inicio", "Estación de inicio:")
        fin = self.pedir_estacion("Fin", "Estación de destino:")
        if inicio and fin:
            ruta = dfs(self.grafo, inicio, fin)
            if ruta:
                self.resultado.setText(f"Ruta DFS: {' -> '.join(ruta)}")
            else:
                self.resultado.setText("Ruta DFS: No se encontró ruta.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = TransporteApp()
    ventana.show()
    sys.exit(app.exec_())