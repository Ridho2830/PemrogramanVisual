import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox,QCheckBox,QFormLayout)
from PySide6.QtCore import Qt

class FormRegistrasi(QWidget):
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Form Registrasi")
        self.resize(400, 300)
        
        main_layout = QVBoxLayout()
        
        # Judul
        judul = QLabel("FORM REGISTRASI")
        judul.setAlignment(Qt.AlignmentFlag.AlignCenter)
        judul.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px; background-color: #34495e; color: white; border-radius: 5px;")
        
        # form layout
        form_layout = QFormLayout()
        
        self.input_nama = QLineEdit()
        self.input_nama.setPlaceholderText("Nama Lengkap")
        form_layout.addRow("Nama:", self.input_nama)
        self.input_nama.setStyleSheet("""
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 3px;
        """)
        
        
        self.input_email = QLineEdit()
        self.input_email.setPlaceholderText("Email")
        form_layout.addRow("Email:", self.input_email)
        self.input_email.setStyleSheet("""
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 3px;
        """)
        
        self.input_password = QLineEdit()
        self.input_password.setPlaceholderText("NIM")
        form_layout.addRow("NIM:", self.input_password)
        self.input_password.setStyleSheet("""
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 3px;
        """)
        
        self.combo_prodi = QComboBox()
        self.combo_prodi.addItems(["--- Pilih Program Studi ---", "Informatika", "Sistem Informasi", "Teknik Komputer"])
        form_layout.addRow("Program Studi:", self.combo_prodi)
        self.combo_prodi.setStyleSheet("""
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 3px;
        """)
        
        # Checkbox
        self.checkbox = QCheckBox("Saya setuju dengan syarat dan ketentuan")
        form_layout.addRow("", self.checkbox)
        self.checkbox.setStyleSheet("""
            padding: 5px;
        """)
        
        # Tombol Submit
        btn_layout = QHBoxLayout()
        self.btn_submit = QPushButton("Submit")
        self.btn_submit.setStyleSheet("""
            padding: 10px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 3px;
        """)
        self.btn_submit.clicked.connect(self.submit_form)
        
        self.btn_reset = QPushButton("Reset")
        self.btn_reset.setStyleSheet("""
            padding: 10px;
            background-color: #e74c3c;
            color: white;
            border: none;
            border-radius: 3px;
        """)
        self.btn_reset.clicked.connect(self.reset_form)
        
        btn_layout.addWidget(self.btn_submit)
        btn_layout.addWidget(self.btn_reset)
        
        # Label Hasil
        self.label_hasil = QLabel("")
        self.label_hasil.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_hasil.setStyleSheet("font-size: 14px; padding: 10px; color: green;")
        
        # Assemble Layout
        main_layout.addWidget(judul)
        main_layout.addLayout(form_layout)
        main_layout.addWidget(self.checkbox)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.label_hasil)
        main_layout.addStretch()
        self.setLayout(main_layout)
        
    def submit_form(self):
        nama = self.input_nama.text()
        email = self.input_email.text()
        nim = self.input_password.text()
        prodi = self.combo_prodi.currentText()
        setuju = self.checkbox.isChecked()
        
        if not nama or not email or not nim or prodi == "--- Pilih Program Studi ---":
            QMessageBox.warning(self, "Error", "Semua field harus diisi!")
            return
        
        if not setuju:
            QMessageBox.warning(self, "Error", "Anda harus menyetujui syarat dan ketentuan!")
            return
        
        self.label_hasil.setText(f"Registrasi Berhasil!\nNama: {nama}\nEmail: {email}\nNIM: {nim}\nProgram Studi: {prodi}")

    def reset_form(self):
        self.input_nama.clear()
        self.input_email.clear()
        self.input_password.clear()
        self.combo_prodi.setCurrentIndex(0)
        self.checkbox.setChecked(False)
        self.label_hasil.clear()

app = QApplication(sys.argv)
window = FormRegistrasi()
window.show()
sys.exit(app.exec())
        
