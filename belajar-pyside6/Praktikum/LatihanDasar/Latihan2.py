import sys
from PySide6.QtWidgets import (QApplication, QLabel, QWidget, QVBoxLayout, QPushButton)
from PySide6.QtCore import Qt

class AplikasiTombol(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Aplikasi Tombol")
        self.resize(300, 200)
        
        # Buat Label
        self.label = QLabel("Belum diklik!")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 16px; padding: 20px;")
        
        # Buat Tombol
        tombol = QPushButton("Klik Saya!")
        tombol.setStyleSheet("font-size: 16px; padding: 10px;")
        
        # Hubungkan sinyal klik tombol ke slot
        tombol.clicked.connect(self.tombol_diklik)
        
        # Buat Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(tombol)

        # Pasang Layout
        self.setLayout(layout)
        
    def tombol_diklik(self):
        self.label.setText("Tombol sudah diklik!")

app = QApplication(sys.argv)
window = AplikasiTombol()
window.show()
sys.exit(app.exec())