import csv
import sqlite3
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLineEdit,
    QLabel, QFormLayout, QMessageBox, QHeaderView, QFileDialog
)

# Import dari module kita sendiri
from backend.validator import Validator


class MainWindow(QMainWindow):
    """MainWindow untuk CRUD Mahasiswa.
    File ini TIDAK boleh ada kode SQL langsung."""
    
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("CRUD Mahasiswa - Modular")
        self.setGeometry(100, 100, 600, 500)
        
        # Terima DatabaseManager dari luar (dari main.py)
        self.db = db
        self.selected_id = None
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Form Input
        form = QFormLayout()
        self.nim_input = QLineEdit()
        self.nim_input.setPlaceholderText("8 digit angka")
        self.nama_input = QLineEdit()
        self.nama_input.setPlaceholderText("Nama lengkap")
        form.addRow("NIM:", self.nim_input)
        form.addRow("Nama:", self.nama_input)
        layout.addLayout(form)
        
        # Tombol
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
        
        self.btn_export = QPushButton("Export CSV")
        self.btn_export.clicked.connect(self.export_csv)
        btn_layout.addWidget(self.btn_export)
        
        layout.addLayout(btn_layout)
        
        # Search
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Cari:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ketik nama atau NIM...")
        self.search_input.textChanged.connect(self.cari_data)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Tabel
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "NIM", "Nama"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.clicked.connect(self.isi_form_dari_tabel)
        layout.addWidget(self.table)
        
        self.statusBar().showMessage("Siap")
    
    # ---- Operasi Data (memanggil DB dan Validator) ----
    
    def load_data(self):
        data = self.db.ambil_semua()
        self.tampilkan_ke_tabel(data)
        self.statusBar().showMessage(f"Total: {len(data)} mahasiswa")
    
    def tampilkan_ke_tabel(self, data):
        self.table.setRowCount(0)
        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(row_data['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(row_data['nim']))
            self.table.setItem(row, 2, QTableWidgetItem(row_data['nama']))
    
    def simpan_data(self):
        nim = self.nim_input.text().strip()
        nama = self.nama_input.text().strip()
        
        # Validasi menggunakan Validator (dari logic/validator.py)
        valid, errors = Validator.validasi_semua(nim, nama)
        if not valid:
            QMessageBox.warning(self, "Validasi Gagal", "\n".join(errors))
            return
        
        try:
            if self.selected_id:
                self.db.update(self.selected_id, nim, nama)
                QMessageBox.information(self, "Sukses", "Data berhasil diupdate!")
            else:
                self.db.tambah(nim, nama)
                QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan!")
            
            self.batal_edit()
            self.load_data()
        
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "NIM sudah terdaftar!")
    
    def hapus_data(self):
        if not self.selected_id:
            QMessageBox.warning(self, "Peringatan", "Pilih data dulu!")
            return
        
        reply = QMessageBox.question(self, "Konfirmasi", "Yakin hapus data ini?")
        if reply == QMessageBox.Yes:
            self.db.hapus(self.selected_id)
            self.batal_edit()
            self.load_data()
    
    def cari_data(self):
        keyword = self.search_input.text().strip()
        data = self.db.cari(keyword) if keyword else self.db.ambil_semua()
        self.tampilkan_ke_tabel(data)
    
    def isi_form_dari_tabel(self):
        row = self.table.currentRow()
        if row >= 0:
            self.selected_id = int(self.table.item(row, 0).text())
            self.nim_input.setText(self.table.item(row, 1).text())
            self.nama_input.setText(self.table.item(row, 2).text())
            self.btn_simpan.setText("Update")
    
    def batal_edit(self):
        self.selected_id = None
        self.nim_input.clear()
        self.nama_input.clear()
        self.btn_simpan.setText("Simpan")
        self.table.clearSelection()
    
    def export_csv(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Export CSV", "mahasiswa.csv", "CSV Files (*.csv)"
        )
        if not filepath:
            return
        
        try:
            data = self.db.ambil_semua()
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'NIM', 'Nama'])
                for r in data:
                    writer.writerow([r['id'], r['nim'], r['nama']])
            QMessageBox.information(self, "Sukses", f"Export berhasil!\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
