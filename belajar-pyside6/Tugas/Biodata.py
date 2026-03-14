import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QComboBox, QMessageBox)
from PySide6.QtCore import Qt

class Biodata(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Form Biodata")
        self.resize(500, 500)
        
        main_layout = QVBoxLayout()
        
        # Judul
        judul = QLabel("FORM BIODATA")
        judul.setAlignment(Qt.AlignmentFlag.AlignCenter)
        judul.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px; background-color: #34495e; color: white; border-radius: 5px;")
        
        # Form Layout
        form_layout = QFormLayout()
        
        self.input_nama = QLineEdit()
        self.input_nama.setPlaceholderText("Nama Lengkap")
        form_layout.addRow("Nama:", self.input_nama)
        
        self.input_nim = QLineEdit()
        self.input_nim.setPlaceholderText("NIM")
        form_layout.addRow("NIM:", self.input_nim)
        
        self.input_kelas = QLineEdit()
        self.input_kelas.setPlaceholderText("Kelas")
        form_layout.addRow("Kelas:", self.input_kelas)
        
        for input in [self.input_nama, self.input_nim, self.input_kelas]:
            input.setStyleSheet("""
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            """)

        self.combo_gender = QComboBox()
        self.combo_gender.addItems(["--- Gender ---", "Laki-laki", "Perempuan"])
        form_layout.addRow("Jenis Kelamin:", self.combo_gender)
        self.combo_gender.setStyleSheet("""
                padding: 5px;
                border: 1px solid #ccc;
                border-radius: 3px;
            """)
        
        # Tombol Submit
        btn_layout = QVBoxLayout()
        self.tombol_submit = QPushButton("Submit")
        self.tombol_submit.setStyleSheet("""
            padding: 10px;
            font-size: 16px;
            background-color: #3498db;
            border: 2px solid blue;
            border-radius: 5px;
        """)
        self.tombol_reset = QPushButton("Reset")
        self.tombol_reset.setStyleSheet("""
            padding: 10px;
            font-size: 16px;
            background-color: #e74c3c;
            border: 2px solid red;
            border-radius: 5px;
        """)
        
        self.tombol_submit.clicked.connect(self.submit_data)
        self.tombol_reset.clicked.connect(self.reset_form)
        
        btn_layout.addWidget(self.tombol_submit)
        btn_layout.addWidget(self.tombol_reset)
        
        # Label Hasil
        self.label_hasil = QLabel("")
        self.label_hasil.setWordWrap(True)        
        self.label_hasil.setStyleSheet("font-size: 14px; padding: 10px; color: green;")
        
        main_layout.addWidget(judul)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.label_hasil)
        self.setLayout(main_layout)
    
    def submit_data(self):
        nama = self.input_nama.text()
        nim = self.input_nim.text()
        kelas = self.input_kelas.text()
        gender = self.combo_gender.currentText()
        
        if not nama or not nim or not kelas or gender == "--- Gender ---":
            QMessageBox.warning(self, "Error", "Semua field harus diisi!")
        
        else:
            self.label_hasil.setText(f"Nama: {nama}\nNIM: {nim}\nKelas: {kelas}\nJenis Kelamin: {gender}")
            self.label_hasil.setStyleSheet("font-size: 14px; padding: 10px; color: green; border: 1px solid #2ecc71; border-radius: 5px;")
    
    def reset_form(self):
        self.input_nama.clear()
        self.input_nim.clear()
        self.input_kelas.clear()
        self.combo_gender.setCurrentIndex(0)
        self.label_hasil.clear()
        
app = QApplication(sys.argv)
window = Biodata()
window.show()
sys.exit(app.exec())