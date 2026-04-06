import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton
)

class MainWindow(QMainWindow):
    """Window profesional menggunakan QMainWindow"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QMainWindow Example")
        self.setGeometry(100, 100, 600, 400)

        # Central widget diperlukan untuk QMainWindow
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        label = QLabel("Ini adalah QMainWindow")
        button = QPushButton("Klik Saya")
        layout.addWidget(label)
        layout.addWidget(button)

        # Built-in StatusBar
        self.statusBar().showMessage("Ready")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
