# ==========================================
# Nama  : Rafly Ridho' Sukardi
# NIM   : F1D02310134
# Kelas : D
# ==========================================

from PySide6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox,
    QDialogButtonBox, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
)
from PySide6.QtCore import Qt
from data import data_loader


STYLE_INPUT = """
    QLineEdit, QComboBox {
        background: #1A2535;
        color: #E0E0E0;
        border: 1px solid #2A3A4A;
        border-radius: 6px;
        padding: 6px 10px;
        font-size: 13px;
    }
    QLineEdit:focus, QComboBox:focus {
        border: 1px solid #4FC3F7;
    }
    QComboBox::drop-down { border: none; }
    QComboBox QAbstractItemView {
        background: #1A2535;
        color: #E0E0E0;
        selection-background-color: #4FC3F7;
        selection-color: #0F1923;
    }
"""

STYLE_BTN_OK = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4FC3F7, stop:1 #0288D1);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 24px;
        font-weight: bold;
        font-size: 13px;
    }
    QPushButton:hover { background: #81D4FA; }
"""

STYLE_BTN_CANCEL = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #37474F, stop:1 #263238);
        color: #E0E0E0;
        border: 1px solid #455A64;
        border-radius: 6px;
        padding: 8px 24px;
        font-size: 13px;
        font-weight: bold;
    }
    QPushButton:hover { background: #546E7A; }
"""


class BookingDialog(QDialog):
    """Dialog untuk tambah/edit booking."""

    def __init__(self, parent=None, booking_id=None):
        super().__init__(parent)
        self.booking_id = booking_id
        if self.booking_id:
            self.setWindowTitle("Edit Booking")
        else:
            self.setWindowTitle("Tambah Booking Baru")
        self.setMinimumWidth(420)
        self.setStyleSheet("background:#0F1923; color:#E0E0E0;")
        self._build_ui()
        if self.booking_id:
            self._load_data()

    def _load_data(self):
        booking = data_loader.get_booking_by_id(self.booking_id)
        if booking:
            idx = self.cmb_room.findData(booking['room_id'])
            if idx >= 0:
                self.cmb_room.setCurrentIndex(idx)
            self.txt_peminjam.setText(booking['peminjam'])
            self.cmb_prodi.setCurrentText(booking['prodi'])
            self.txt_tanggal.setText(booking['tanggal'])
            self.cmb_sesi.setCurrentText(booking['sesi'])
            self.cmb_keperluan.setCurrentText(booking['keperluan'])
            self.cmb_status.setCurrentText(booking['status'])

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        title = QLabel("📋  Formulir Booking Ruangan")
        title.setStyleSheet("font-size:15px; font-weight:bold; color:#4FC3F7; padding-bottom:4px;")
        layout.addWidget(title)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignRight)

        # Pilih ruangan
        rooms_df = data_loader.get_rooms()
        self.cmb_room = QComboBox()
        for _, r in rooms_df.iterrows():
            self.cmb_room.addItem(f"{r['kode_ruang']} – {r['gedung']}", r["id"])
        self.cmb_room.setStyleSheet(STYLE_INPUT)

        self.txt_peminjam = QLineEdit()
        self.txt_peminjam.setPlaceholderText("Nama lengkap")
        self.txt_peminjam.setStyleSheet(STYLE_INPUT)

        self.cmb_prodi = QComboBox()
        for p in ["Teknik Informatika", "Sistem Informasi", "Manajemen",
                  "Akuntansi", "Teknik Elektro", "Desain Komunikasi Visual",
                  "Psikologi", "Hukum"]:
            self.cmb_prodi.addItem(p)
        self.cmb_prodi.setStyleSheet(STYLE_INPUT)

        self.txt_tanggal = QLineEdit()
        self.txt_tanggal.setPlaceholderText("YYYY-MM-DD")
        self.txt_tanggal.setStyleSheet(STYLE_INPUT)

        self.cmb_sesi = QComboBox()
        for s in ["07:00-09:00", "09:00-11:00", "11:00-13:00",
                  "13:00-15:00", "15:00-17:00", "17:00-19:00"]:
            self.cmb_sesi.addItem(s)
        self.cmb_sesi.setStyleSheet(STYLE_INPUT)

        self.cmb_keperluan = QComboBox()
        for k in ["Kuliah Reguler", "Ujian Tengah Semester",
                  "Ujian Akhir Semester", "Seminar Tugas Akhir",
                  "Rapat Organisasi", "Workshop", "Praktikum"]:
            self.cmb_keperluan.addItem(k)
        self.cmb_keperluan.setStyleSheet(STYLE_INPUT)

        self.cmb_status = QComboBox()
        for s in ["Pending", "Disetujui", "Ditolak"]:
            self.cmb_status.addItem(s)
        self.cmb_status.setStyleSheet(STYLE_INPUT)

        lbl_style = "color:#B0BEC5; font-size:12px;"
        for label, widget in [
            ("Ruangan", self.cmb_room),
            ("Peminjam", self.txt_peminjam),
            ("Program Studi", self.cmb_prodi),
            ("Tanggal", self.txt_tanggal),
            ("Sesi", self.cmb_sesi),
            ("Keperluan", self.cmb_keperluan),
            ("Status", self.cmb_status),
        ]:
            lbl = QLabel(label)
            lbl.setStyleSheet(lbl_style)
            form.addRow(lbl, widget)

        layout.addLayout(form)

        # Tombol
        btn_row = QHBoxLayout()
        btn_row.addStretch()
        btn_cancel = QPushButton("Batal")
        btn_cancel.setStyleSheet(STYLE_BTN_CANCEL)
        btn_cancel.clicked.connect(self.reject)

        btn_ok = QPushButton("Simpan")
        btn_ok.setStyleSheet(STYLE_BTN_OK)
        btn_ok.clicked.connect(self._save)

        btn_row.addWidget(btn_cancel)
        btn_row.addWidget(btn_ok)
        layout.addLayout(btn_row)

    def _save(self):
        room_id   = self.cmb_room.currentData()
        peminjam  = self.txt_peminjam.text().strip()
        prodi     = self.cmb_prodi.currentText()
        tanggal   = self.txt_tanggal.text().strip()
        sesi      = self.cmb_sesi.currentText()
        keperluan = self.cmb_keperluan.currentText()
        status    = self.cmb_status.currentText()

        if not peminjam or not tanggal:
            return  # validasi minimal

        if hasattr(self, 'booking_id') and self.booking_id:
            data_loader.update_booking(self.booking_id, room_id, peminjam, prodi, tanggal, sesi, keperluan, status)
        else:
            data_loader.add_booking(room_id, peminjam, prodi,
                                    tanggal, sesi, keperluan, status)
        self.accept()
