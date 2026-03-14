import sys
from PySide6.QtWidgets import QApplication, QGridLayout, QWidget, QPushButton

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Contoh QBoxLayout")
        self.resize(300, 150)

        # Buat Layout (vertikal)
        layout = QGridLayout()

        # Tambahkan Widget ke Layout
        layout.addWidget(QPushButton("Tombol 1"), 0, 0)
        layout.addWidget(QPushButton("Tombol 2"), 0, 1)
        layout.addWidget(QPushButton("Tombol 3"), 0, 2)

        layout.addWidget(QPushButton("Tombol 4"), 1, 0)
        layout.addWidget(QPushButton("Tombol 5"), 1, 1)
        layout.addWidget(QPushButton("Tombol 6"), 1, 2)

        layout.addWidget(QPushButton("Tombol 7"), 2, 0)
        layout.addWidget(QPushButton("Tombol 8"), 2, 1)
        layout.addWidget(QPushButton("Tombol 9"), 2, 2)

        # Tambahkan stretch untuk memberi ruang
        # layout.setRowStretch(2, 1)
        # layout.setColumnStretch(2, 1)
        # Pasang Layout
        self.setLayout(layout)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())