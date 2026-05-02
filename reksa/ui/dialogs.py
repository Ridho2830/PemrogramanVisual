"""
dialogs.py — Dialog tambah/edit koleksi serta dialog Tentang Aplikasi.
Form input menggunakan berbagai komponen PySide6 sesuai kebutuhan.
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QComboBox, QSpinBox, QTextEdit,
    QPushButton, QLabel, QFrame, QMessageBox,
    QSpacerItem, QSizePolicy,
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from utils.constants import (
    TIPE_KOLEKSI, GENRE_LIST, STATUS_KOLEKSI,
    RATING_LIST, FORMAT_MEDIA,
    APP_NAME, APP_VERSION, APP_DESCRIPTION,
    NAMA_MAHASISWA, NIM_MAHASISWA,
)


class DialogKoleksi(QDialog):
    """Dialog untuk menambah atau mengedit entri koleksi manga/anime."""

    data_saved = Signal()

    def __init__(self, parent=None, mode="tambah", data=None):
        super().__init__(parent)
        self.mode = mode
        self.edit_data = data
        self.result_data = None

        self._setup_ui()
        self._connect_signals()

        # Isi form bila mode edit
        if mode == "edit" and data:
            self._populate_data(data)

    # ================================================================
    # SETUP UI
    # ================================================================
    def _setup_ui(self):
        title = (
            "✨  Tambah Koleksi Baru"
            if self.mode == "tambah"
            else "✏️  Edit Koleksi"
        )
        self.setWindowTitle(title)
        self.setMinimumWidth(540)
        self.setModal(True)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(14)
        main_layout.setContentsMargins(28, 24, 28, 24)

        # --- Header ---
        label_title = QLabel(title)
        label_title.setObjectName("labelDialogTitle")
        main_layout.addWidget(label_title)

        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setObjectName("dialogSeparator")
        main_layout.addWidget(separator)

        # --- Form Input (minimal 5 field + 3 tambahan) ---
        form_layout = QFormLayout()
        form_layout.setSpacing(12)
        form_layout.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        form_layout.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow
        )

        # Field 1: Judul (QLineEdit)
        self.input_judul = QLineEdit()
        self.input_judul.setPlaceholderText("Contoh: Attack on Titan")
        self.input_judul.setMaxLength(150)
        form_layout.addRow("Judul *", self.input_judul)

        # Field 2: Tipe Koleksi (QComboBox)
        self.input_tipe = QComboBox()
        self.input_tipe.addItems(TIPE_KOLEKSI)
        form_layout.addRow("Tipe *", self.input_tipe)

        # Field 3: Genre (QComboBox)
        self.input_genre = QComboBox()
        self.input_genre.addItems(GENRE_LIST)
        form_layout.addRow("Genre *", self.input_genre)

        # Field 4: Episode / Chapter (QSpinBox)
        self.input_episode = QSpinBox()
        self.input_episode.setRange(0, 99999)
        self.input_episode.setValue(0)
        self.input_episode.setSuffix(" eps/ch")
        form_layout.addRow("Episode / Chapter *", self.input_episode)

        # Field 5: Status (QComboBox)
        self.input_status = QComboBox()
        self.input_status.addItems(STATUS_KOLEKSI)
        form_layout.addRow("Status *", self.input_status)

        # Field 6: Rating (QComboBox)
        self.input_rating = QComboBox()
        self.input_rating.addItems(RATING_LIST)
        form_layout.addRow("Rating", self.input_rating)

        # Field 7: Format Media (QComboBox)
        self.input_format = QComboBox()
        self.input_format.addItems(FORMAT_MEDIA)
        form_layout.addRow("Format Media", self.input_format)

        # Field 8: Catatan (QTextEdit)
        self.input_catatan = QTextEdit()
        self.input_catatan.setPlaceholderText(
            "Tambahkan catatan, review singkat, atau pendapat pribadi..."
        )
        self.input_catatan.setMaximumHeight(85)
        form_layout.addRow("Catatan", self.input_catatan)

        main_layout.addLayout(form_layout)

        # --- Info label ---
        info_label = QLabel("* Field wajib diisi")
        info_label.setObjectName("labelInfoRequired")
        main_layout.addWidget(info_label)

        main_layout.addSpacerItem(
            QSpacerItem(0, 6, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        )

        # --- Tombol Aksi ---
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

    # ================================================================
    # SIGNAL & SLOT
    # ================================================================
    def _connect_signals(self):
        """Menghubungkan signal dan slot komponen dialog."""
        self.btn_simpan.clicked.connect(self._on_simpan)
        self.btn_batal.clicked.connect(self.reject)

        # Otomatis ubah suffix episode/chapter berdasarkan tipe
        self.input_tipe.currentTextChanged.connect(self._update_suffix)

    def _update_suffix(self, tipe: str):
        """Menyesuaikan suffix SpinBox berdasarkan tipe koleksi."""
        if tipe in ("Manga", "Manhwa", "Manhua", "Light Novel"):
            self.input_episode.setSuffix(" chapter")
        else:
            self.input_episode.setSuffix(" episode")

    # ================================================================
    # POPULATE (mode edit)
    # ================================================================
    def _populate_data(self, data: dict):
        """Mengisi form dengan data yang sudah ada (mode edit)."""
        self.input_judul.setText(data.get("judul", ""))
        self.input_tipe.setCurrentText(data.get("tipe", "Manga"))
        self.input_genre.setCurrentText(data.get("genre", "Action"))
        self.input_episode.setValue(data.get("episode_chapter", 0))
        self.input_status.setCurrentText(
            data.get("status", "Rencana Tonton/Baca")
        )
        self.input_rating.setCurrentText(
            data.get("rating", "Belum Dirating")
        )
        self.input_format.setCurrentText(
            data.get("format_media", "TV Series")
        )
        self.input_catatan.setPlainText(data.get("catatan", ""))

    # ================================================================
    # SIMPAN DATA
    # ================================================================
    def _on_simpan(self):
        """Validasi dan simpan data koleksi."""
        judul = self.input_judul.text().strip()
        if not judul:
            QMessageBox.warning(
                self,
                "Validasi Gagal",
                "Judul koleksi tidak boleh kosong!\n"
                "Silakan isi judul terlebih dahulu.",
            )
            self.input_judul.setFocus()
            return

        from datetime import datetime
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.result_data = {
            "judul": judul,
            "tipe": self.input_tipe.currentText(),
            "genre": self.input_genre.currentText(),
            "episode_chapter": self.input_episode.value(),
            "status": self.input_status.currentText(),
            "rating": self.input_rating.currentText(),
            "format_media": self.input_format.currentText(),
            "catatan": self.input_catatan.toPlainText().strip(),
            "tanggal_update": now,
        }

        # Tanggal ditambahkan hanya saat Create
        if self.mode == "tambah":
            self.result_data["tanggal_ditambahkan"] = now

        self.data_saved.emit()
        self.accept()

    def get_data(self) -> dict:
        """Mengembalikan dictionary data hasil form."""
        return self.result_data


# ====================================================================
# DIALOG TENTANG APLIKASI
# ====================================================================
class DialogTentang(QDialog):
    """Dialog informasi tentang aplikasi, termasuk identitas mahasiswa."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._setup_ui()

    def _setup_ui(self):
        self.setWindowTitle("Tentang Aplikasi")
        self.setFixedSize(500, 460)
        self.setModal(True)

        layout = QVBoxLayout(self)
        layout.setSpacing(14)
        layout.setContentsMargins(32, 28, 32, 28)

        # Icon besar
        icon_label = QLabel("🎌")
        icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon_label.setStyleSheet("font-size: 52px;")
        layout.addWidget(icon_label)

        # Nama aplikasi
        app_label = QLabel(APP_NAME)
        app_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        app_label.setObjectName("aboutAppName")
        layout.addWidget(app_label)

        # Versi
        version_label = QLabel(f"Versi {APP_VERSION}")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setObjectName("aboutVersion")
        layout.addWidget(version_label)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        sep.setObjectName("dialogSeparator")
        layout.addWidget(sep)

        # Deskripsi
        desc_label = QLabel(APP_DESCRIPTION)
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc_label.setObjectName("aboutDescription")
        layout.addWidget(desc_label)

        # Separator
        sep2 = QFrame()
        sep2.setFrameShape(QFrame.Shape.HLine)
        sep2.setObjectName("dialogSeparator")
        layout.addWidget(sep2)

        # Info mahasiswa dalam frame
        info_frame = QFrame()
        info_frame.setObjectName("frameInfoDev")
        info_layout = QVBoxLayout(info_frame)
        info_layout.setSpacing(6)

        dev_title = QLabel("👨‍💻  Dikembangkan oleh")
        dev_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        dev_title.setObjectName("aboutDevTitle")
        info_layout.addWidget(dev_title)

        nama_label = QLabel(NAMA_MAHASISWA)
        nama_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nama_label.setObjectName("aboutDevName")
        info_layout.addWidget(nama_label)

        nim_label = QLabel(f"NIM: {NIM_MAHASISWA}")
        nim_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nim_label.setObjectName("aboutDevNim")
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
