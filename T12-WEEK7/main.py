# ==========================================
# Nama  : Rafly Ridho' Sukardi
# NIM   : F1D02310134
# Kelas : D
# ==========================================

"""
main.py
Entry point aplikasi Dashboard Booking Ruangan Kelas Kampus.
Jalankan dengan: python main.py
"""

import sys
import os

# Pastikan root project ada di sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

from data.seed_db import init_db
from ui.main_window import MainWindow


def main():
    # Inisialisasi database & seed data
    init_db()

    app = QApplication(sys.argv)
    app.setFont(QFont("Segoe UI", 10))
    app.setApplicationName("Dashboard Booking Ruangan")
    app.setOrganizationName("Kampus Demo")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
