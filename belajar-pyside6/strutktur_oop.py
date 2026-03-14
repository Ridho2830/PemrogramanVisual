import sys
from PySide6.QtWidgets import QApplication, QWidget

# Class Utama untuk membuat jendela aplikasi
class MainWindow(QWidget):
    
    def __init__(self):
        
        # Memanggil konstruktor dari kelas induk (QWidget)
        super().__init__()
        # Memanggil metode untuk mengatur tampilan UI
        self.setup_ui()

    def setup_ui(self):
        # Method untuk mengatur tampilan UI
        self.setWindowTitle("Aplikasi Pertama")
        self.resize(400, 300)
        self.setMinimumSize(200, 150)
        
def main():
    # Main function untuk menjalankan aplikasi
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())       
            
            
if __name__ == "__main__":
    main()