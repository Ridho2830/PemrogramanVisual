import sys
from PySide6.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout)
from PySide6.QtCore import Qt

class CounterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Counter App")
        self.counter = 0
        self.resize(300, 200)
        
        # Label untuk menampilkan nilai counter
        self.counter_label = QLabel(f"Counter: {self.counter}")
        self.counter_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.counter_label.setStyleSheet("""
                                        font-size: 20px; 
                                        font-weight: bold;
                                        padding: 20px;
                                        background-color: black;
                                        border: 2px solid blue;
                                        """)
        
        # Tombol tambah
        self.tombol_tambah = QPushButton("+ Tambah")
        self.tombol_tambah.setStyleSheet("""
                                        padding: 15px;
                                        font-size: 16px;
                                        background-color: #3498db;
                                        border: 2px solid blue;
                                        bodrer: none;
                                        bodrer-radius: 5px;
                                        """)
        self.tombol_tambah.clicked.connect(self.tambah_counter)
        
        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.counter_label)
        layout.addWidget(self.tombol_tambah)
        self.setLayout(layout)
        
    def tambah_counter(self):
        self.counter += 1
        self.counter_label.setText(f"Counter: {self.counter}")

app = QApplication(sys.argv)
window = CounterApp()
window.show()
sys.exit(app.exec())
        
