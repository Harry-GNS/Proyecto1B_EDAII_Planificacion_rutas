import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

from interfaz import TransporteApp, TransporteAppBFS

class MenuPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Menú Principal")
        self.setStyleSheet("background: #23272e; color: #e0e7ef;")
        self.setFixedSize(400, 250)
        layout = QVBoxLayout(self)
        layout.setSpacing(30)

        titulo = QLabel("Bienvenido al Planificador de Rutas")
        titulo.setFont(QFont("Segoe UI", 16, QFont.Bold))
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        btn_dfs = QPushButton("DFS (Profundidad)")
        btn_dfs.setFont(QFont("Segoe UI", 12))
        btn_dfs.clicked.connect(self.abrir_dfs)
        layout.addWidget(btn_dfs)

        btn_bfs = QPushButton("BFS (Anchura)")
        btn_bfs.setFont(QFont("Segoe UI", 12))
        btn_bfs.clicked.connect(self.abrir_bfs)
        layout.addWidget(btn_bfs)

    def abrir_dfs(self):
        self.hide()
        self.ventana_dfs = TransporteApp()
        self.ventana_dfs.showMaximized()
        self.ventana_dfs.show()

    def abrir_bfs(self):
        self.hide()
        self.ventana_bfs = TransporteAppBFS()
        self.ventana_bfs.showMaximized()
        self.ventana_bfs.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    menu = MenuPrincipal()
    menu.show()
    sys.exit(app.exec_())