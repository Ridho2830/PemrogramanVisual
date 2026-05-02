import csv
import sqlite3
from PySide6.QtWidgets import (
    QComboBox, QDoubleSpinBox, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLineEdit,
    QLabel, QFormLayout, QMessageBox, QHeaderView, QFileDialog, QSpinBox
)

# Import dari module kita sendiri
from backend.validator import Validator


class MainWindow(QMainWindow):
    """MainWindow untuk CRUD Mahasiswa.
    File ini TIDAK boleh ada kode SQL langsung."""
    
    def __init__(self, db):
        super().__init__()
        self.setWindowTitle("CRUD Film - Modular")
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
        self.judul = QLineEdit()
        self.judul.setPlaceholderText("Judul film")
        self.sutradara = QLineEdit()
        self.sutradara.setPlaceholderText("Sutradara")
        self.tahun_rilis = QSpinBox()
        self.tahun_rilis.setRange(1945, 2023)
        self.durasi = QLineEdit()
        self.durasi.setPlaceholderText("Durasi (menit)")
        self.rating = QDoubleSpinBox()
        self.rating.setRange(0, 10)
        self.rating.setDecimals(1)
        self.genre = QComboBox()
        self.genre.setPlaceholderText("Genre")
        self.genre.addItems(["Aksi", "Komedi", "Drama", "Horror", "Romansa"])
        form.addRow("Judul:", self.judul)
        form.addRow("Sutradara:", self.sutradara)
        form.addRow("Tahun Rilis:", self.tahun_rilis)
        form.addRow("Durasi:", self.durasi)
        form.addRow("Rating:", self.rating)
        form.addRow("Genre:", self.genre)
        layout.addLayout(form)
        
        # Tombol
        btn_layout = QHBoxLayout()
        
        self.btn_simpan = QPushButton("Simpan")
        self.btn_simpan.setObjectName("btn_simpan")
        self.btn_simpan.clicked.connect(self.simpan_data)
        btn_layout.addWidget(self.btn_simpan)
        
        self.btn_hapus = QPushButton("Hapus")
        self.btn_hapus.setObjectName("btn_hapus")
        self.btn_hapus.clicked.connect(self.hapus_data)
        btn_layout.addWidget(self.btn_hapus)
        
        self.btn_batal = QPushButton("Batal")
        self.btn_batal.setObjectName("btn_batal")
        self.btn_batal.clicked.connect(self.batal_edit)
        btn_layout.addWidget(self.btn_batal)
        
        self.btn_export = QPushButton("Export CSV")
        self.btn_export.setObjectName("btn_export")
        self.btn_export.clicked.connect(self.export_csv)
        btn_layout.addWidget(self.btn_export)
        
        layout.addLayout(btn_layout)
        
        # Search
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Cari:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Ketik judul atau sutradara...")
        self.search_input.textChanged.connect(self.cari_data)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Tabel
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["ID", "Judul", "Sutradara", "Tahun Rilis", "Durasi", "Rating", "Genre"])
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
        self.statusBar().showMessage(f"Total: {len(data)} film")
    
    def tampilkan_ke_tabel(self, data):
        self.table.setRowCount(0)
        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(row_data['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(row_data['judul_film']))
            self.table.setItem(row, 2, QTableWidgetItem(row_data['sutradara']))
            self.table.setItem(row, 3, QTableWidgetItem(str(row_data['tahun_rilis'])))
            self.table.setItem(row, 4, QTableWidgetItem(str(row_data['durasi'])))
            self.table.setItem(row, 5, QTableWidgetItem(str(row_data['rating'])))
            self.table.setItem(row, 6, QTableWidgetItem(row_data['genre']))
            
    def simpan_data(self):
        judul = self.judul.text().strip()
        sutradara = self.sutradara.text().strip()
        tahun_rilis = self.tahun_rilis.value()
        durasi = self.durasi.text().strip()
        rating = self.rating.value()
        genre = self.genre.currentText()
        
        
        # Validasi menggunakan Validator (dari logic/validator.py)
        valid, errors = Validator.validasi_semua(judul, sutradara, tahun_rilis, durasi, rating, genre)
        if not valid:
            QMessageBox.warning(self, "Validasi Gagal", "\n".join(errors))
            return
        
        try:
            if self.selected_id:
                self.db.update(self.selected_id, judul, sutradara, tahun_rilis, durasi, rating, genre)
                QMessageBox.information(self, "Sukses", "Data berhasil diupdate!")
            else:
                self.db.tambah(judul, sutradara, tahun_rilis, durasi, rating, genre)
                QMessageBox.information(self, "Sukses", "Data berhasil ditambahkan!")
            
            self.batal_edit()
            self.load_data()
        
        except sqlite3.IntegrityError:
            QMessageBox.warning(self, "Error", "Judul film sudah terdaftar!")
    
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
            self.judul.setText(self.table.item(row, 1).text())
            self.sutradara.setText(self.table.item(row, 2).text())
            self.tahun_rilis.setValue(int(self.table.item(row, 3).text()) if self.table.item(row, 3) else 0)
            self.durasi.setText(self.table.item(row, 4).text() if self.table.item(row, 4) else "0")
            self.rating.setValue(float(self.table.item(row, 5).text()) if self.table.item(row, 5) else 0)
            self.genre.setCurrentText(self.table.item(row, 6).text() if self.table.item(row, 6) else "")
            self.btn_simpan.setText("Update")
    
    def batal_edit(self):
        self.selected_id = None
        self.judul.clear()
        self.sutradara.clear()
        self.tahun_rilis.setValue(2023)
        self.durasi.clear()
        self.rating.setValue(0.0)
        self.genre.setCurrentIndex(0)
        self.btn_simpan.setText("Simpan")
        self.table.clearSelection()
    
    def export_csv(self):
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Export CSV", "films.csv", "CSV Files (*.csv)"
        )
        if not filepath:
            return
        
        try:
            data = self.db.ambil_semua()
            with open(filepath, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Judul', 'Sutradara', 'Tahun Rilis', 'Durasi', 'Rating', 'Genre'])
                for r in data:
                    writer.writerow([r['id'], r['judul_film'], r['sutradara'], r['tahun_rilis'], r['durasi'], r['rating'], r['genre']])
            QMessageBox.information(self, "Sukses", f"Export berhasil!\n{filepath}")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
