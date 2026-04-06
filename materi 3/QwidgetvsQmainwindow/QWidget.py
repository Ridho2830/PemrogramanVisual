import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton

class SimpleWindow(QWidget):
    """Window sederhana menggunakan QWidget"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QWidget Example")
        self.setGeometry(100, 100, 300, 200)

        # Layout harus dibuat manual
        layout = QVBoxLayout(self)
        label = QLabel("Ini adalah QWidget sederhana")
        button = QPushButton("Klik Saya")
        layout.addWidget(label)
        layout.addWidget(button)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()
    sys.exit(app.exec())
