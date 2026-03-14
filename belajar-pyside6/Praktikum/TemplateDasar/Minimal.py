import sys
from PySide6.QtWidgets import QApplication, QWidget

# Buat App
app = QApplication(sys.argv)

# Buat Window
window = QWidget()
window.setWindowTitle("Contoh Window")
window.resize(400, 300)
window.show()

# Jalankan App
sys.exit(app.exec())