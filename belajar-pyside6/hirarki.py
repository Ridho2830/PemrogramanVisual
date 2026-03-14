import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton


class contohHirarki(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Contoh Hirarki")
        self.resize(400, 300)

        # Membuat layout (parent widget)
        layout = QVBoxLayout()

        # Menambahkan widget child (label)
        label = QLabel("Ini label")
        tombol = QPushButton("Ini tombol")
        layout.addWidget(label)

        # Menambahkan child ke layout
        # Layout otomatis menjadi parent dari widget yang ditambahkan
        layout.addWidget(label)
        label.setStyleSheet("qproperty-alignment: AlignCenter;")
        layout.addWidget(tombol)
        
        self.setLayout(layout)  # Set layout ke widget utama (self)

app = QApplication(sys.argv)
window = contohHirarki()    
window.show()
sys.exit(app.exec())   