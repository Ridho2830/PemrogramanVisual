import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Even Driven")
        self.setGeometry(100, 100, 300, 200)
        
        # Membuat button
        self.button = QPushButton("Klik Saya", self)
        self.button.setGeometry(100, 80, 100, 30)
        
        #Menghubungkan event klik ke fungsi handler
        self.button.clicked.connect(self.on_button_clicked)
        
    def on_button_clicked(self):
        print("Button telah diklik!")
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
        