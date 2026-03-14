import sys
from PySide6.QtWidgets import QApplication, QFormLayout, QLineEdit, QWidget

class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Contoh QBoxLayout")
        self.resize(300, 150)

        # Buat Layout
        layout = QFormLayout()

        # Tambahkan Widget ke Layout
        layout.addRow("Nama:", QLineEdit())
        layout.addRow("Email:", QLineEdit())
        layout.addRow("Password:", QLineEdit())

        # Pasang Layout
        self.setLayout(layout)


app = QApplication(sys.argv)
window = Window()
window.show()
sys.exit(app.exec())