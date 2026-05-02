from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox,
    QTextEdit, QDateEdit, QPushButton, QLabel,
    QFrame, QMessageBox, QSpacerItem, QSizePolicy,
)
from PySide6.QtCore import Qt, QDate, Signal
from PySide6.QtGui import QFont

from utils.constants import (
    KATEGORI_BARANG, LOKASI_GUDANG, STATUS_BARANG,
    KONDISI_BARANG, APP_NAME, APP_VERSION,
    APP_DESCRIPTION, NAMA_MAHASISWA, NIM_MAHASISWA,
)


class DialogBarang(QDialog):
    data_saved = Signal()

    def __init__(self, parent=None, mode="tambah", data=None):

        super().__init__(parent)
        self.mode = mode
        self.edit_data = data
        self.result_data = None

        self._setup_ui()
        self._connect_signals()

        if mode == "edit" and data:
            self._populate_data(data)

    def _setup_ui(self):
        title = "Tambah Barang Baru" if self.mode == "tambah" else "Edit Data Barang"
        self.setWindowTitle(title)
        self.setMinimumWidth(520)
        self.setModal(True)

        # Layout utama
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(28, 24, 28, 24)

        # --- Header dialog ---
        label_title = QLabel(title)
        label_title.setObjectName("labelDialogTitle")
        main_layout.addWidget(label_title)

        # Garis pemisah
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setStyleSheet("color: #e2e8f0;")
        main_layout.addWidget(separator)

        # --- Form input ---
        form_layout = QFormLayout()
        form_layout.setSpacing(14)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow
        )

        # Field 1: Nama Barang (QLineEdit)
        self.input_nama = QLineEdit()
        self.input_nama.setPlaceholderText("Masukkan nama barang...")
        self.input_nama.setMaxLength(100)
        form_layout.addRow("Nama Barang *", self.input_nama)

        # Field 2: Kategori (QComboBox)
        self.input_kategori = QComboBox()
        self.input_kategori.addItems(KATEGORI_BARANG)
        form_layout.addRow("Kategori *", self.input_kategori)

        # Field 3: Jumlah/Stok (QSpinBox)
        self.input_jumlah = QSpinBox()
        self.input_jumlah.setRange(0, 999999)
        self.input_jumlah.setValue(0)
        self.input_jumlah.setSuffix(" unit")
        form_layout.addRow("Jumlah Stok *", self.input_jumlah)

        # Field 4: Harga Satuan (QDoubleSpinBox)
        self.input_harga = QDoubleSpinBox()
        self.input_harga.setRange(0, 999999999.99)
        self.input_harga.setDecimals(2)
        self.input_harga.setValue(0)
        self.input_harga.setPrefix("Rp ")
        self.input_harga.setSingleStep(1000)
        form_layout.addRow("Harga Satuan *", self.input_harga)

        # Field 5: Lokasi Gudang (QComboBox)
        self.input_lokasi = QComboBox()
        self.input_lokasi.addItems(LOKASI_GUDANG)
        form_layout.addRow("Lokasi *", self.input_lokasi)

        # Field 6: Kondisi Barang (QComboBox)
        self.input_kondisi = QComboBox()
        self.input_kondisi.addItems(KONDISI_BARANG)
        form_layout.addRow("Kondisi *", self.input_kondisi)

        # Field 7: Status (QComboBox)
        self.input_status = QComboBox()
        self.input_status.addItems(STATUS_BARANG)
        form_layout.addRow("Status *", self.input_status)

        # Field 8: Tanggal Masuk (QDateEdit) - hanya untuk mode tambah
        if self.mode == "tambah":
            self.input_tanggal = QDateEdit()
            self.input_tanggal.setCalendarPopup(True)
            self.input_tanggal.setDate(QDate.currentDate())
            self.input_tanggal.setDisplayFormat("dd/MM/yyyy")
            form_layout.addRow("Tanggal Masuk", self.input_tanggal)

        # Field 9: Deskripsi (QTextEdit)
        self.input_deskripsi = QTextEdit()
        self.input_deskripsi.setPlaceholderText(
            "Tambahkan catatan atau deskripsi barang..."
        )
        self.input_deskripsi.setMaximumHeight(90)
        form_layout.addRow("Deskripsi", self.input_deskripsi)

        main_layout.addLayout(form_layout)

        # --- Info label ---
        info_label = QLabel("* Field wajib diisi")
        info_label.setStyleSheet("color: #94a3b8; font-size: 11px; font-style: italic;")
        main_layout.addWidget(info_label)

        main_layout.addSpacerItem(
            QSpacerItem(0, 8, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        )

        # --- Tombol aksi ---
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)
        btn_layout.addStretch()

        self.btn_batal = QPushButton("Batal")
        self.btn_batal.setObjectName("btnBatal")
        self.btn_batal.setCursor(Qt.CursorShape.PointingHandCursor)

        self.btn_simpan = QPushButton(
            "💾  Simpan" if self.mode == "tambah" else "💾  Perbarui"
        )
        self.btn_simpan.setObjectName("btnSimpan")
        self.btn_simpan.setCursor(Qt.CursorShape.PointingHandCursor)

        btn_layout.addWidget(self.btn_batal)
        btn_layout.addWidget(self.btn_simpan)
        main_layout.addLayout(btn_layout)

    def _connect_signals(self):
        """Menghubungkan signal dan slot komponen dialog."""
        self.btn_simpan.clicked.connect(self._on_simpan)
        self.btn_batal.clicked.connect(self.reject)

        # Auto-update status berdasarkan jumlah stok
        self.input_jumlah.valueChanged.connect(self._auto_update_status)

    def _auto_update_status(self, value):
        if value == 0:
            self.input_status.setCurrentText("Habis")
        elif value <= 10:
            self.input_status.setCurrentText("Stok Menipis")
        else:
            self.input_status.setCurrentText("Tersedia")

    def _populate_data(self, data):
        self.input_nama.setText(data.get("nama_barang", ""))
        self.input_kategori.setCurrentText(data.get("kategori", ""))
        self.input_jumlah.setValue(data.get("jumlah", 0))
        self.input_harga.setValue(data.get("harga", 0.0))
        self.input_lokasi.setCurrentText(data.get("lokasi", ""))
        self.input_kondisi.setCurrentText(data.get("kondisi", "Baru"))
        self.input_status.setCurrentText(data.get("status", "Tersedia"))
        self.input_deskripsi.setPlainText(data.get("deskripsi", ""))

    def _on_simpan(self):
        # Validasi: nama barang wajib diisi
        nama = self.input_nama.text().strip()
        if not nama:
            QMessageBox.warning(
                self,
                "Validasi Gagal",
                "Nama barang tidak boleh kosong!\nSilakan isi nama barang terlebih dahulu.",
            )
            self.input_nama.setFocus()
            return

        # Siapkan data hasil
        from datetime import datetime

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.result_data = {
            "nama_barang": nama,
            "kategori": self.input_kategori.currentText(),
            "jumlah": self.input_jumlah.value(),
            "harga": self.input_harga.value(),
            "lokasi": self.input_lokasi.currentText(),
            "kondisi": self.input_kondisi.currentText(),
            "status": self.input_status.currentText(),
            "deskripsi": self.input_deskripsi.toPlainText().strip(),
            "tanggal_update": now,
        }

        # Tambahkan tanggal masuk untuk barang baru
        if self.mode == "tambah":
            self.result_data["tanggal_masuk"] = (
                self.input_tanggal.date().toString("yyyy-MM-dd")
            )

        self.data_saved.emit()
        self.accept()

    def get_data(self) -> dict:
        return self.result_data


class DialogTentang(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("Tentang Aplikasi")
        self.setFixedSize(480, 420)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(32, 28, 32, 28)

        # Icon / Emoji
        icon_label = QLabel("📦")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 48px;")
        layout.addWidget(icon_label)

        # Nama aplikasi
        app_label = QLabel(APP_NAME)
        app_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_label.setStyleSheet(
            "font-size: 20px; font-weight: bold; color: #0f172a;"
        )
        layout.addWidget(app_label)

        # Versi
        version_label = QLabel(f"Versi {APP_VERSION}")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("font-size: 12px; color: #94a3b8;")
        layout.addWidget(version_label)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setStyleSheet("color: #e2e8f0;")
        layout.addWidget(sep)

        # Deskripsi
        desc_label = QLabel(APP_DESCRIPTION)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setStyleSheet(
            "font-size: 12px; color: #64748b; line-height: 1.6; padding: 4px 8px;"
        )
        layout.addWidget(desc_label)

        # Separator
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setStyleSheet("color: #e2e8f0;")
        layout.addWidget(sep2)

        # Info mahasiswa
        info_frame = QFrame()
        info_frame.setStyleSheet(
            """
            QFrame {
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 10px;
                padding: 12px;
            }
            """
        )
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(6)

        dev_title = QLabel("👨‍💻  Dikembangkan oleh")
        dev_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dev_title.setStyleSheet(
            "font-size: 11px; color: #94a3b8; font-weight: bold;"
        )
        info_layout.addWidget(dev_title)

        nama_label = QLabel(NAMA_MAHASISWA)
        nama_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nama_label.setStyleSheet(
            "font-size: 16px; font-weight: bold; color: #0284c7;"
        )
        info_layout.addWidget(nama_label)

        nim_label = QLabel(f"NIM: {NIM_MAHASISWA}")
        nim_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nim_label.setStyleSheet("font-size: 13px; color: #64748b;")
        info_layout.addWidget(nim_label)

        layout.addWidget(info_frame)

        layout.addStretch()

        # Tombol tutup
        btn_tutup = QPushButton("Tutup")
        btn_tutup.setObjectName("btnBatal")
        btn_tutup.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_tutup.clicked.connect(self.accept)

        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(btn_tutup)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
