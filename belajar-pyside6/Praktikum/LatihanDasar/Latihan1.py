import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout)
from PySide6.QtCore import Qt

class JendelaPesan(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Pesan Sambutan")
        self.resize(300, 150)
        
        # Buat Label
        label = QLabel("Selamat Datang di PySide6!")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 20px; font-weight: bold; color: green;")

        # Buat Layout (vertikal)
        layout = QVBoxLayout()

        # Tambahkan Widget ke Layout
        layout.addWidget(label)

        # Pasang Layout
        self.setLayout(layout)
        
app = QApplication(sys.argv)
window = JendelaPesan()
window.show()
sys.exit(app.exec())