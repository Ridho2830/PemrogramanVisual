import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QLineEdit, QComboBox, QCheckBox, QRadioButton, QVBoxLayout)
from PySide6.QtCore import Qt

class InputNama(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Input Nama")
        self.resize(400, 300)
        
        # Label Intruksi
        label_intruksi = QLabel("Masukkan Nama Anda:")
        label_intruksi.setAlignment(Qt.AlignCenter)
        label_intruksi.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px;")
        
        # Input Nama
        self.input_nama = QLineEdit()
        self.input_nama.setPlaceholderText("Nama Anda")
        self.input_nama.setStyleSheet(""" 
                                        font-size: 14px; 
                                        padding: 10px;
                                        border: 2px solid gray;
                                        border-radius: 5px;
                                        """)

        # Tombol Sapa
        self.tombol_sapa = QPushButton("Sapa!")
        self.tombol_sapa.setStyleSheet("""
                            padding: 15px;
                            font-size: 16px;
                            background-color: #2ecc71;
                            border: 2px solid green;
                            border-radius: 5px;
                            """)
        self.tombol_sapa.clicked.connect(self.sapa)
        
        # Label Hasil
        self.label_hasil = QLabel("")
        self.label_hasil.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_hasil.setStyleSheet("font-size: 14px; font-weight: bold; padding: 10px;")

        # Buat Layout
        layout = QVBoxLayout()
        layout.addWidget(label_intruksi)
        layout.addWidget(self.input_nama)
        layout.addWidget(self.tombol_sapa)
        layout.addWidget(self.label_hasil)

        # Pasang Layout
        self.setLayout(layout)
        
    def sapa(self):
        nama = self.input_nama.text().strip()
        if nama:
            self.label_hasil.setText(f"Halo, {nama}!")
            self.label_hasil.setStyleSheet("font-size: 16px; font-weight: bold; color: green; padding: 10px;")
        else:
            self.label_hasil.setText("Masukkan nama terlebih dahulu!")
            self.label_hasil.setStyleSheet("font-size: 14px; font-weight: bold; color: red; padding: 10px;")

app = QApplication(sys.argv)
window = InputNama()
window.show()
sys.exit(app.exec())