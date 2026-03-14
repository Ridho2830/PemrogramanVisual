import sys
from PySide6.QtWidgets import QApplication, QCheckBox, QComboBox, QLabel, QLineEdit, QRadioButton, QVBoxLayout, QWidget, QPushButton
from PySide6.QtCore import Qt

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Latihan Widget Label, Tombol, TextBox, Dropdown")
        self.resize(300, 150)

        # Buat Layout (vertikal)
        layout = QVBoxLayout()

        # Tambahkan Widget ke Layout
        
        # 1 Label
        label = QLabel("Tabel Latihan")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 20px; color: lightblue;")
        
        # 2 Tombol
        tombol = QPushButton("Tombol")
        tombol.clicked.connect(self.fungsi_handler)
        tombol.setEnabled(True)
        
        # 3 TextBox
        line_edit = QLineEdit()
        line_edit.setPlaceholderText("Masukkan teks")
        line_edit.setClearButtonEnabled(True)
        
        # 4 Dropdown 
        combobox = QComboBox()
        combobox.addItems(["Pilihan 1", "Pilihan 2", "Pilihan 3"])
        teks = combobox.currentText()
        index = combobox.currentIndex()
        print(f"Pilihan saat ini: {teks} (Index: {index})")
        combobox.setCurrentIndex(0)
        
        # 5 Ceckbox
        checkbox = QCheckBox("Saya setuju")
        if checkbox.isChecked():
            print("Checkbox dicentang")
        checkbox.setChecked(True)
        
        # 6 Radio Button
        radio_button1 = QRadioButton("Opsi 1")
        radio_button2 = QRadioButton("Opsi 2")
        radio_button3 = QRadioButton("Opsi 3")
        radio_button1.setChecked(True)
        if radio_button1.isChecked():
            print("AY AY CAPTEN!!!")
        
        

        layout.addWidget(label)  
        layout.addWidget(tombol)
        layout.addWidget(line_edit)
        layout.addWidget(combobox)
        layout.addWidget(checkbox)
        layout.addWidget(radio_button1)
        layout.addWidget(radio_button2)
        layout.addWidget(radio_button3)

        # Tambahkan stretch untuk memberi ruang
        layout.addStretch()

        # Pasang Layout
        self.setLayout(layout)
        
        
    def fungsi_handler(self):
        print("Tombol ditekan!")

app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())