import sys
from PySide6.QtWidgets import QApplication, QWidget

#1 . Buat Objek QApplication
app = QApplication(sys.argv)

#2. Jendela
window = QWidget()
window.setWindowTitle("Aplikasi Pertama")
window.resize(400, 300)

#3 Tampilkan Jendela
window.show()

#4. Jalankan Aplikasix
sys.exit(app.exec())