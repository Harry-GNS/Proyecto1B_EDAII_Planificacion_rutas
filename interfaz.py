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
import matplotlib.image as mpimg
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

from grafo import Grafo
from dfs import dfs_ruta_mas_profunda
from bfs import bfs_ruta_mas_corta

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
        # Dibuja solo las aristas
        nx.draw(
            G, pos,
            with_labels=False,
            node_color='none',  # No dibujar círculos
            node_size=10,
            edge_color="#B0BEC5",
            linewidths=1.5,
            ax=self.ax
        )
        # Cargar imagen de parada de bus
        try:
            img = mpimg.imread("Media/parada.png")
        except Exception:
            img = None
        # Coloca la imagen en cada nodo
        if img is not None:
            for p in pos.values():
                imagebox = OffsetImage(img, zoom=0.02)  # Ajusta el zoom según tamaño deseado
                ab = AnnotationBbox(imagebox, p, frameon=False)
                self.ax.add_artist(ab)
                
        # Etiquetas encima de la imagen
        label_pos = {k: (v[0], v[1]+0.09) for k, v in pos.items()}
        nx.draw_networkx_labels(
            G, label_pos,
            labels={n: n for n in G.nodes()},
            font_size=4,
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
            QTextEdit#CargadosTextEdit {
                font-size: 9pt; /* Más pequeño */
                background: #23272e;
                color: #80cbc4;
                border: 2px solid #44475a;
                border-radius: 8px;
                margin-bottom: 12px;
            }
            QTextEdit { padding: 8px; }
        """)
        self.grafo = Grafo()
        self.init_ui()
        self.showMaximized()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        # --- Panel superior: controles y resultados ---
        top_panel = QHBoxLayout()
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

        # Texto de resultados de agregados/cargados (más alto, bien encuadrado, con barra scroll)
        self.texto = QTextEdit()
        self.texto.setObjectName("CargadosTextEdit")
        self.texto.setReadOnly(True)
        self.texto.setFixedHeight(180)
        self.texto.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.texto.setLineWrapMode(QTextEdit.WidgetWidth)
        left_panel.addWidget(self.texto)

        # Línea separadora entre cuadros
        dfs_line = QFrame()
        dfs_line.setFrameShape(QFrame.HLine)
        dfs_line.setFrameShadow(QFrame.Sunken)
        dfs_line.setStyleSheet("color: #44475a; background: #44475a; max-height: 2px; margin-bottom: 8px;")
        left_panel.addWidget(dfs_line)

        left_panel.addStretch(0)

        # --- LADO DERECHO: Grafo ---
        self.grafo_canvas = GrafoCanvas(self.grafo)
        self.grafo_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # --- Panel superior: controles (izq) y grafo (der) ---
        top_panel.addLayout(left_panel, stretch=1)
        top_panel.addWidget(self.grafo_canvas, stretch=2)

        # --- Panel inferior: resultado DFS a lo ancho ---
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setStyleSheet("background: #23272e; color: #FFD600; font-size: 12pt; border: 2px solid #44475a; border-radius: 8px;")
        self.resultado.setLineWrapMode(QTextEdit.WidgetWidth)
        self.resultado.setFixedHeight(70)

        main_layout.addLayout(top_panel, stretch=5)
        main_layout.addWidget(self.resultado, stretch=0)

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
            with open(archivo, 'r',encoding='utf-8') as f:
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
            ruta = dfs_ruta_mas_profunda(self.grafo, inicio, fin)
            if ruta:
                self.resultado.setText(f"Ruta más profunda: {' -> '.join(ruta)}")
            else:
                self.resultado.setText("Ruta más profunda: No se encontró ruta.")

class TransporteAppBFS(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Planificador de Rutas BFS")
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
            QTextEdit#CargadosTextEdit {
                font-size: 9pt; /* Más pequeño */
                background: #23272e;
                color: #80cbc4;
                border: 2px solid #44475a;
                border-radius: 8px;
                margin-bottom: 12px;
            }
            QTextEdit { padding: 8px; }
        """)
        self.grafo = Grafo()
        self.init_ui()
        self.showMaximized()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        top_panel = QHBoxLayout()
        left_panel = QVBoxLayout()
        left_panel.setSpacing(18)
        title = QLabel("Planificador de Rutas BFS")
        title.setFont(QFont("Segoe UI", 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        left_panel.addWidget(title)
        self.entry = QLineEdit()
        self.entry.setPlaceholderText("Parada (origen,destino)")
        left_panel.addWidget(self.entry)
        self.add_btn = QPushButton("Agregar")
        self.add_btn.clicked.connect(self.agregar_parada)
        left_panel.addWidget(self.add_btn)
        self.csv_btn = QPushButton("Cargar CSV")
        self.csv_btn.clicked.connect(self.cargar_csv)
        left_panel.addWidget(self.csv_btn)
        self.buscar_btn = QPushButton("Buscar Ruta BFS")
        self.buscar_btn.clicked.connect(self.buscar_ruta)
        left_panel.addWidget(self.buscar_btn)
        self.texto = QTextEdit()
        self.texto.setObjectName("CargadosTextEdit")
        self.texto.setReadOnly(True)
        self.texto.setFixedHeight(180)
        self.texto.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.texto.setLineWrapMode(QTextEdit.WidgetWidth)
        left_panel.addWidget(self.texto)
        bfs_line = QFrame()
        bfs_line.setFrameShape(QFrame.HLine)
        bfs_line.setFrameShadow(QFrame.Sunken)
        bfs_line.setStyleSheet("color: #44475a; background: #44475a; max-height: 2px; margin-bottom: 8px;")
        left_panel.addWidget(bfs_line)
        left_panel.addStretch(0)
        self.grafo_canvas = GrafoCanvas(self.grafo)
        self.grafo_canvas.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        top_panel.addLayout(left_panel, stretch=1)
        top_panel.addWidget(self.grafo_canvas, stretch=2)
        self.resultado = QTextEdit()
        self.resultado.setReadOnly(True)
        self.resultado.setStyleSheet("background: #23272e; color: #00E676; font-size: 12pt; border: 2px solid #44475a; border-radius: 8px;")
        self.resultado.setLineWrapMode(QTextEdit.WidgetWidth)
        self.resultado.setFixedHeight(70)
        main_layout.addLayout(top_panel, stretch=5)
        main_layout.addWidget(self.resultado, stretch=0)

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
            with open(archivo, 'r',encoding='utf-8') as f:
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
            ruta = bfs_ruta_mas_corta(self.grafo, inicio, fin)
            if ruta:
                self.resultado.setText(f"Ruta más corta: {' -> '.join(ruta)}")
            else:
                self.resultado.setText("Ruta más corta: No se encontró ruta.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = TransporteApp()
    ventana.show()
    sys.exit(app.exec_())