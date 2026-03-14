import sys
from PySide6.QtWidgets import QApplication, QHBoxLayout, QWidget, QPushButton

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Contoh QBoxLayout")
        self.resize(300, 150)

        # Buat Layout (vertikal)
        layout = QHBoxLayout()

        # Tambahkan Widget ke Layout
        layout.addWidget(QPushButton("Tombol 1"))
        layout.addWidget(QPushButton("Tombol 2"))
        layout.addWidget(QPushButton("Tombol 3"))

        # Tambahkan stretch untuk memberi ruang
        layout.addStretch()

        # Pasang Layout
        self.setLayout(layout)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())