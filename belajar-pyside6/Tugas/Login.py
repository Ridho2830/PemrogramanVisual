import sys
from PySide6.QtWidgets import (QApplication, QCheckBox, QHBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFormLayout, QMessageBox)
from PySide6.QtCore import Qt

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Login")
        self.resize(300, 300)
        
        layout = QVBoxLayout()
        
        # Judul
        judul = QLabel("LOGIN")
        judul.setAlignment(Qt.AlignmentFlag.AlignCenter)
        judul.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px; background-color: #34495e; color: white; border-radius: 5px;")
        
        # Form Login
        form_layout = QFormLayout()
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        
        # Checkbox Show Password
        self.show_password_checkbox = QCheckBox("Show Password")
        self.show_password_checkbox.setCheckable(True)
        self.show_password_checkbox.clicked.connect(self.toggle_password_visibility)
        
        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)
        form_layout.addRow("", self.show_password_checkbox)
        
        # Tombol
        btn_layout = QHBoxLayout()
        self.login_button = QPushButton("Login")
        self.login_button.setStyleSheet("""
                                        padding: 10px;
                                        font-size: 14px;
                                        background-color: #2980b9;
                                        border: 2px solid blue;
                                        border-radius: 5px;
                                        """)
        btn_layout.addWidget(self.login_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.setStyleSheet("""
                                        padding: 10px;
                                        font-size: 14px;
                                        background-color: #e74c3c;
                                        border: 2px solid red;
                                        border-radius: 5px;
                                        """)
        btn_layout.addWidget(self.reset_button)

        # Connect tombol ke fungsi
        self.login_button.clicked.connect(self.handle_login)
        self.reset_button.clicked.connect(self.handle_reset)
        
        # Label untuk informasi
        self.info_label = QLabel("")
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("font-size: 12px; padding:15px;")
        # Tambahkan widget ke layout
        layout.addWidget(judul)
        layout.addLayout(form_layout)
        layout.addLayout(btn_layout)
        layout.addWidget(self.info_label)

        self.setLayout(layout)
    
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if username == "admin" and password == "12345":
            self.info_label.setText("Login berhasil!")
            self.info_label.setStyleSheet("color: green; font-size: 12px; padding:15px;")
        else:
            self.info_label.setText("Login gagal. Silakan coba lagi.")
            self.info_label.setStyleSheet("color: red; font-size: 12px; padding:15px;")

    def handle_reset(self):
        self.username_input.clear()
        self.password_input.clear()
        self.show_password_checkbox.setChecked(False)
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.info_label.setText("")

    def toggle_password_visibility(self):
        if self.show_password_checkbox.isChecked():
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            
app = QApplication(sys.argv)
window = Login()
window.show()
sys.exit(app.exec())