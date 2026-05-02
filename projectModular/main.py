import sys
from PySide6.QtWidgets import QApplication

# Import dari module kita
from database.database import DatabaseManager
from frontend.main_window import MainWindow


def main():
    # 1. Buat aplikasi
    app = QApplication(sys.argv)
    
    # 2. Buat database manager
    db = DatabaseManager('data_mahasiswa.db', 'projectModular/database/')
    
    # 3. Buat window, kirim db sebagai parameter
    window = MainWindow(db)
    window.show()
    
    # 4. Jalankan
    sys.exit(app.exec())


if __name__ == "__main__":
    main()