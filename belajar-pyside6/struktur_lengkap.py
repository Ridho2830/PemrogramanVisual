import sys
from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtCore import Qt

#Class Utama Aplikasi

class MainWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        self.setWindowTitle("Aplikasi Pertama")
        self.resize(400, 300)
        self.setMinimumSize(200, 150)
        self.center_on_screen()
        self.setStyleSheet("background-color: #f0f0f0;")
    
    def setup_connections(self):
        pass
    
    def center_on_screen(self):
        screen_geometry = QApplication.primaryScreen().geometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
if __name__ == "__main__":
    main()            
