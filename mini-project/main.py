"""
main.py - Entry point aplikasi InvenTrack
Sistem Manajemen Inventaris berbasis PySide6 + SQLite

Struktur Project (Separation of Concerns):
├── main.py              # Entry point aplikasi
├── database/
│   └── db_manager.py    # Modul pengelolaan database SQLite
├── ui/
│   ├── main_window.py   # Jendela utama (tampilan data)
│   └── dialogs.py       # Dialog tambah/edit & tentang
├── styles/
│   └── style.qss        # Stylesheet QSS eksternal
└── utils/
    └── constants.py      # Konstanta dan konfigurasi
"""

import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFont

from ui.main_window import MainWindow


def load_stylesheet(app: QApplication):
    style_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "styles", "style.qss"
    )
    try:
        with open(style_path, "r", encoding="utf-8") as f:
            qss = f.read()
            app.setStyleSheet(qss)
            print(f"[INFO] Stylesheet berhasil dimuat dari: {style_path}")
    except FileNotFoundError:
        print(f"[WARNING] File stylesheet tidak ditemukan: {style_path}")
    except Exception as e:
        print(f"[ERROR] Gagal memuat stylesheet: {e}")


def main():
    """Fungsi utama untuk menjalankan aplikasi."""
    app = QApplication(sys.argv)

    # Set font default
    default_font = QFont("Segoe UI", 10)
    app.setFont(default_font)

    # Muat stylesheet QSS dari file eksternal
    load_stylesheet(app)

    # Buat dan tampilkan jendela utama
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
