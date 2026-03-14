import sys
from PySide6.QtWidgets import QApplication, QWidget

# Buat App
class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        # Konfigurasi Window
        self.setWindowTitle("Contoh Window")
        self.resize(400, 300)
    
def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec())
if __name__ == "__main__":    
    main()