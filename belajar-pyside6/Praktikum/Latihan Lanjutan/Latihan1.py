import sys
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox)
from PySide6.QtCore import Qt

class Kalkulator(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Kalkulator")
        self.resize(400, 300)
        
        layout = QVBoxLayout()
        
        #Judul
        judul = QLabel("KALKULATOR")
        judul.setAlignment(Qt.AlignmentFlag.AlignCenter)
        judul.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px; background-color: #34495e; color: white; border-radius: 5px;")
        
        # Input Field
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Angka Pertama")
        self.input1.setStyleSheet("""
                                        font-size: 14px; 
                                        padding: 10px;
                                        border: 2px solid gray;
                                        border-radius: 5px;
                                        """)
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
        self.btn_kali = QPushButton("*")
        self.btn_bagi = QPushButton("/")
        
        btn_style = """
                        padding: 15px;
                        font-size: 16px;
                        background-color: #2980b9;
                        border: 2px solid blue;
                        border-radius: 5px;
                        """
        for btn in (self.btn_plus, self.btn_minus, self.btn_kali, self.btn_bagi):
            btn.setStyleSheet(btn_style)
            tombol_layout.addWidget(btn)

        # Connect tombol ke fungsi
        self.btn_plus.clicked.connect(self.hitung_plus)
        self.btn_minus.clicked.connect(self.hitung_minus)
        self.btn_kali.clicked.connect(self.hitung_kali)
        self.btn_bagi.clicked.connect(self.hitung_bagi)
        
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
        self.setLayout(layout)
        
    def get_numbers(self):
            try:
                num1 = float(self.input1.text())
                num2 = float(self.input2.text())
                return num1, num2
            except ValueError:
                QMessageBox.warning(self, "Input Error", "Masukkan angka yang valid!")
                return None, None    
        
    def tampil_hasil(self, hasil):
        self.label_hasil.setText(f"Hasil: {hasil}")
        self.label_hasil.setStyleSheet("font-size: 16px; font-weight: bold; color: green; padding: 10px;")

    def hitung_plus(self):
            num1, num2 = self.get_numbers()
            if num1 is not None and num2 is not None:
                hasil = num1 + num2
                self.tampil_hasil(hasil)

    def hitung_plus(self):
            num1, num2 = self.get_numbers()
            if num1 is not None and num2 is not None:
                hasil = num1 + num2
                self.tampil_hasil(hasil)

    def hitung_minus(self):
            num1, num2 = self.get_numbers()
            if num1 is not None and num2 is not None:
                hasil = num1 - num2
                self.tampil_hasil(hasil)

    def hitung_kali(self):
            num1, num2 = self.get_numbers()
            if num1 is not None and num2 is not None:
                hasil = num1 * num2
                self.tampil_hasil(hasil)

    def hitung_bagi(self):
            num1, num2 = self.get_numbers()
            if num1 is not None and num2 is not None:
                if num2 != 0:
                    hasil = num1 / num2
                    self.tampil_hasil(hasil)
                else:
                    QMessageBox.warning(self, "Error", "Tidak bisa membagi dengan nol!")

        
app = QApplication(sys.argv)
window = Kalkulator()
window.show()
sys.exit(app.exec())