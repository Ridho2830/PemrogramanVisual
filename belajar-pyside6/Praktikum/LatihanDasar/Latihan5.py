import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout
)
from PySide6.QtCore import Qt

class KalkulatorMini(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Kalkulator Mini")
        self.resize(400, 200)
        
        layout = QVBoxLayout()
        
        #Judul
        judul = QLabel("KALKULATOR MINI")
        judul.setAlignment(Qt.AlignmentFlag.AlignCenter)
        judul.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px; background-color: #34495e; color: white; border-radius: 5px;")
        
        # Angka Pertama
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Angka Pertama")
        self.input1.setStyleSheet("""
                                        font-size: 14px; 
                                        padding: 10px;
                                        border: 2px solid gray;
                                        border-radius: 5px;
                                        """)
        # Angka Kedua
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("Angka Kedua")
        self.input2.setStyleSheet("""
                                        font-size: 14px; 
                                        padding: 10px;
                                        border: 2px solid gray;
                                        border-radius: 5px;
                                        """)
        
        # Tombol Operasi
        tombol_layout = QHBoxLayout()
        self.btn_plus = QPushButton("+")
        self.btn_minus = QPushButton("-")
        
        # Style Tombol
        for btn in (self.btn_plus, self.btn_minus):
            btn.setStyleSheet("""
                                        padding: 15px;
                                        font-size: 16px;
                                        background-color: #2980b9;
                                        border: 2px solid blue;
                                        border-radius: 5px;
                                        """)
        
        tombol_layout.addWidget(self.btn_plus)
        tombol_layout.addWidget(self.btn_minus)
        
        # Hubungkan tombol ke fungsi
        self.btn_plus.clicked.connect(self.hitung_plus)
        self.btn_minus.clicked.connect(self.hitung_minus)
        
        # Label Hasil
        self.label_hasil = QLabel("Hasil: -")
        self.label_hasil.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_hasil.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        
        # Assemble Layout
        layout.addWidget(judul)
        layout.addWidget(self.input1)
        layout.addWidget(self.input2)
        layout.addLayout(tombol_layout)
        layout.addWidget(self.label_hasil)
                
        
        
        # Pasang Layout
        self.setLayout(layout)
        
    def hitung_plus(self):
        try:
            angka1 = float(self.input1.text())
            angka2 = float(self.input2.text())
            hasil = angka1 + angka2
            self.label_hasil.setText(f"Hasil: {hasil}")
            self.label_hasil.setStyleSheet("font-size: 16px; font-weight: bold; color: green; padding: 10px;")
        except ValueError:
            self.label_hasil.setText("Input tidak valid!")
            self.label_hasil.setStyleSheet("font-size: 14px; font-weight: bold; color: red; padding: 10px;")

    def hitung_minus(self):
        try:
            angka1 = float(self.input1.text())
            angka2 = float(self.input2.text())
            hasil = angka1 - angka2
            self.label_hasil.setText(f"Hasil: {hasil}")
            self.label_hasil.setStyleSheet("font-size: 16px; font-weight: bold; color: green; padding: 10px;")
        except ValueError:
            self.label_hasil.setText("Input tidak valid!")
            self.label_hasil.setStyleSheet("font-size: 14px; font-weight: bold; color: red; padding: 10px;")

app = QApplication(sys.argv)
window = KalkulatorMini()
window.show()
sys.exit(app.exec())