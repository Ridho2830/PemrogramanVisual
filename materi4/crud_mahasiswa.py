import sys
import sqlite3
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLineEdit,
    QLabel, QFormLayout, QMessageBox, QHeaderView
)
from PySide6.QtCore import Qt


# ============================================
# BAGIAN 1: DATABASE
# ============================================

class DatabaseManager:
    def __init__(self, db_name='data_mhs.db'):
        self.db_name = db_name
        self.create_table()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def create_table(self):
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS mahasiswa (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nim TEXT NOT NULL UNIQUE,
                    nama TEXT NOT NULL
                )
            ''')
    
    def tambah(self, nim, nama):
        with self.get_connection() as conn:
            conn.execute('INSERT INTO mahasiswa (nim, nama) VALUES (?, ?)', (nim, nama))
    
    def ambil_semua(self):
        with self.get_connection() as conn:
            return conn.execute('SELECT * FROM mahasiswa ORDER BY nama').fetchall()
    
    def cari(self, keyword):
        with self.get_connection() as conn:
            return conn.execute(
                'SELECT * FROM mahasiswa WHERE nama LIKE ? OR nim LIKE ?',
                (f'%{keyword}%', f'%{keyword}%')
            ).fetchall()
    
    def update(self, id, nim, nama):
        with self.get_connection() as conn:
            conn.execute('UPDATE mahasiswa SET nim=?, nama=? WHERE id=?', (nim, nama, id))
    
    def hapus(self, id):
        with self.get_connection() as conn:
            conn.execute('DELETE FROM mahasiswa WHERE id = ?', (id,))


# ============================================
# BAGIAN 2: MAIN WINDOW (UI + LOGIC)
# ============================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CRUD Mahasiswa Sederhana")
        self.setGeometry(100, 100, 600, 500)
        
        # Inisialisasi database
        self.db = DatabaseManager()
        
        # ID mahasiswa yang sedang di-edit (None = mode tambah)
        self.selected_id = None
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # ===== FORM INPUT =====
        form_layout = QFormLayout()
        
        self.nim_input = QLineEdit()
        self.nim_input.setPlaceholderText("Contoh: 12345678")
        form_layout.addRow("NIM:", self.nim_input)
        
        self.nama_input = QLineEdit()
        self.nama_input.setPlaceholderText("Contoh: Budi Santoso")
        form_layout.addRow("Nama:", self.nama_input)
        
        layout.addLayout(form_layout)
        
        # ===== TOMBOL AKSI =====
        btn_layout = QHBoxLayout()
        
        self.btn_simpan = QPushButton("Simpan")
        self.btn_simpan.clicked.connect(self.simpan_data)
        btn_layout.addWidget(self.btn_simpan)
        
        self.btn_hapus = QPushButton("Hapus")
        self.btn_hapus.clicked.connect(self.hapus_data)
        btn_layout.addWidget(self.btn_hapus)
        
        self.btn_batal = QPushButton("Batal")
        self.btn_batal.clicked.connect(self.batal_edit)
        btn_layout.addWidget(self.btn_batal)
        
        layout.addLayout(btn_layout)
        
        # ===== SEARCH =====
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Cari:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ketik nama atau NIM...")
        self.search_input.textChanged.connect(self.cari_data)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # ===== TABEL DATA =====
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "NIM", "Nama"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.clicked.connect(self.isi_form_dari_tabel)
        layout.addWidget(self.table)
        
        # Status bar
        self.statusBar().showMessage("Siap")
    
    # ============================
    # OPERASI CRUD
    # ============================
    
    def load_data(self):
        """Ambil semua data dari DB dan tampilkan ke tabel"""
        data = self.db.ambil_semua()
        self.tampilkan_ke_tabel(data)
        self.statusBar().showMessage(f"Total: {len(data)} mahasiswa")
    
    def tampilkan_ke_tabel(self, data):
        """Mengisi tabel dengan data"""
        self.table.setRowCount(0)  # Kosongkan tabel dulu
        
        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(row_data['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(row_data['nim']))
            self.table.setItem(row, 2, QTableWidgetItem(row_data['nama']))
    
    def simpan_data(self):
        """Simpan data baru atau update data yang sudah ada"""
        nim = self.nim_input.text().strip()
        nama = self.nama_input.text().strip()
        
        # Validasi sederhana
        if not nim or not nama:
            QMessageBox.warning(self, "Peringatan", "NIM dan Nama harus diisi!")
            return
        
        try:
            if self.selected_id:
                # MODE UPDATE
                self.db.update(self.selected_id, nim, nama)
                QMessageBox.information(self, "Sukses", "Data berhasil diupdate!")
            else:
                # MODE TAMBAH
                self.db.tambah(nim, nama)
                QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan!")
            
            self.batal_edit()   # Reset form
            self.load_data()    # Refresh tabel
        
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "NIM sudah terdaftar!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan:\n{e}")
    
    def hapus_data(self):
        """Hapus data yang dipilih di tabel"""
        if not self.selected_id:
            QMessageBox.warning(self, "Peringatan", "Pilih data di tabel yang akan dihapus!")
            return
        
        reply = QMessageBox.question(
            self, "Konfirmasi",
            "Yakin ingin menghapus data ini?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.db.hapus(self.selected_id)
            self.batal_edit()
            self.load_data()
            QMessageBox.information(self, "Sukses", "Data berhasil dihapus!")
    
    def cari_data(self):
        """Cari data berdasarkan keyword di search input"""
        keyword = self.search_input.text().strip()
        if keyword:
            data = self.db.cari(keyword)
        else:
            data = self.db.ambil_semua()
        self.tampilkan_ke_tabel(data)
    
    def isi_form_dari_tabel(self):
        """Saat baris di tabel diklik, isi form dengan data tersebut"""
        row = self.table.currentRow()
        if row >= 0:
            self.selected_id = int(self.table.item(row, 0).text())
            self.nim_input.setText(self.table.item(row, 1).text())
            self.nama_input.setText(self.table.item(row, 2).text())
            self.btn_simpan.setText("Update")
            self.statusBar().showMessage(f"Editing ID: {self.selected_id}")
    
    def batal_edit(self):
        """Reset form ke mode tambah"""
        self.selected_id = None
        self.nim_input.clear()
        self.nama_input.clear()
        self.btn_simpan.setText("Simpan")
        self.table.clearSelection()
        self.statusBar().showMessage("Siap")


# ============================================
# BAGIAN 3: MENJALANKAN APLIKASI
# ============================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())