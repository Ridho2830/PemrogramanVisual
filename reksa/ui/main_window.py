"""
main_window.py — Jendela utama aplikasi OtakuVault.
Menampilkan data koleksi dalam tabel, menyediakan toolbar pencarian/filter,
serta kartu statistik ringkasan koleksi.
"""

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel,
    QFrame, QLineEdit, QComboBox, QMenu,
    QStatusBar, QMessageBox, QHeaderView,
    QAbstractItemView,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QColor

from database.db_manager import DatabaseManager
from ui.dialogs import DialogKoleksi, DialogTentang
from utils.constants import (
    APP_NAME, NAMA_MAHASISWA, NIM_MAHASISWA,
    TIPE_KOLEKSI, STATUS_KOLEKSI,
)


class MainWindow(QMainWindow):
    """Jendela utama OtakuVault — Koleksi Manga & Anime."""

    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()

        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(1100, 720)
        self.resize(1300, 800)

        self._setup_menubar()
        self._setup_ui()
        self._setup_statusbar()
        self._connect_signals()

        # Muat data pertama kali
        self._refresh_data()

    # ================================================================
    # MENU BAR
    # ================================================================
    def _setup_menubar(self):
        """Menyiapkan menu bar utama."""
        menubar = self.menuBar()

        # --- Menu File ---
        menu_file = QMenu("File", self)
        menubar.addMenu(menu_file)

        action_tambah = QAction("✨  Tambah Koleksi", self)
        action_tambah.setShortcut("Ctrl+N")
        action_tambah.triggered.connect(self._on_tambah)
        menu_file.addAction(action_tambah)

        action_refresh = QAction("🔄  Refresh Data", self)
        action_refresh.setShortcut("F5")
        action_refresh.triggered.connect(self._refresh_data)
        menu_file.addAction(action_refresh)

        menu_file.addSeparator()

        action_keluar = QAction("🚪  Keluar", self)
        action_keluar.setShortcut("Ctrl+Q")
        action_keluar.triggered.connect(self.close)
        menu_file.addAction(action_keluar)

        # --- Menu Tentang ---
        menu_tentang = QMenu("Tentang", self)
        menubar.addMenu(menu_tentang)

        action_about = QAction("ℹ️  Tentang Aplikasi", self)
        action_about.triggered.connect(self._show_about)
        menu_tentang.addAction(action_about)

    # ================================================================
    # SETUP UI UTAMA
    # ================================================================
    def _setup_ui(self):
        """Menyusun seluruh komponen antarmuka utama."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(24, 20, 24, 16)

        # Header (judul + identitas)
        main_layout.addLayout(self._create_header())

        # Statistik cards
        main_layout.addLayout(self._create_stat_cards())

        # Toolbar (search, filter, tombol)
        main_layout.addWidget(self._create_toolbar())

        # Tabel data utama
        main_layout.addWidget(self._create_table())

    def _create_header(self) -> QHBoxLayout:
        """Membuat header dengan judul aplikasi dan identitas mahasiswa."""
        header_layout = QHBoxLayout()

        # Kiri: Judul & subtitle
        left_layout = QVBoxLayout()
        left_layout.setSpacing(2)

        label_judul = QLabel("🎌  OtakuVault")
        label_judul.setObjectName("labelJudul")
        left_layout.addWidget(label_judul)

        label_subtitle = QLabel("Kelola Koleksi Manga & Anime Favoritmu")
        label_subtitle.setObjectName("labelSubtitle")
        left_layout.addWidget(label_subtitle)

        header_layout.addLayout(left_layout)
        header_layout.addStretch()

        # Kanan: Identitas mahasiswa (tidak bisa diedit — QLabel)
        label_identitas = QLabel(
            f"👤  {NAMA_MAHASISWA}  •  NIM: {NIM_MAHASISWA}"
        )
        label_identitas.setObjectName("labelIdentitas")
        header_layout.addWidget(label_identitas)

        return header_layout

    def _create_stat_cards(self) -> QHBoxLayout:
        """Membuat baris kartu statistik ringkasan."""
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)

        stat_configs = [
            ("📚", "Total Koleksi",   "stat_total",     "#6d28d9"),
            ("📖", "Manga",           "stat_manga",     "#0284c7"),
            ("📺", "Anime",           "stat_anime",     "#c026d3"),
            ("▶️",  "Sedang Diikuti",  "stat_ongoing",   "#ea580c"),
            ("✅", "Selesai",         "stat_selesai",   "#16a34a"),
        ]

        self.stat_labels = {}

        for icon, title, key, accent in stat_configs:
            frame = QFrame()
            frame.setObjectName("frameStat")
            frame.setMinimumHeight(95)

            frame_layout = QHBoxLayout(frame)
            frame_layout.setContentsMargins(16, 12, 16, 12)
            frame_layout.setSpacing(12)

            icon_label = QLabel(icon)
            icon_label.setObjectName("labelStatIcon")
            frame_layout.addWidget(icon_label)

            text_layout = QVBoxLayout()
            text_layout.setSpacing(2)

            title_label = QLabel(title.upper())
            title_label.setObjectName("labelStatTitle")
            text_layout.addWidget(title_label)

            value_label = QLabel("0")
            value_label.setObjectName("labelStatValue")
            value_label.setStyleSheet(f"color: {accent};")
            text_layout.addWidget(value_label)

            self.stat_labels[key] = value_label
            frame_layout.addLayout(text_layout)
            frame_layout.addStretch()

            stats_layout.addWidget(frame)

        return stats_layout

    def _create_toolbar(self) -> QFrame:
        """Membuat toolbar dengan pencarian, filter, dan tombol aksi."""
        toolbar_frame = QFrame()
        toolbar_frame.setObjectName("frameToolbar")

        toolbar_layout = QHBoxLayout(toolbar_frame)
        toolbar_layout.setContentsMargins(14, 10, 14, 10)
        toolbar_layout.setSpacing(10)

        # Pencarian
        self.input_cari = QLineEdit()
        self.input_cari.setPlaceholderText("🔍  Cari judul, tipe, genre...")
        self.input_cari.setMinimumWidth(260)
        self.input_cari.setClearButtonEnabled(True)
        toolbar_layout.addWidget(self.input_cari)

        # Filter tipe
        self.filter_tipe = QComboBox()
        self.filter_tipe.addItem("Semua Tipe")
        self.filter_tipe.addItems(TIPE_KOLEKSI)
        self.filter_tipe.setMinimumWidth(150)
        toolbar_layout.addWidget(self.filter_tipe)

        # Filter status
        self.filter_status = QComboBox()
        self.filter_status.addItem("Semua Status")
        self.filter_status.addItems(STATUS_KOLEKSI)
        self.filter_status.setMinimumWidth(180)
        toolbar_layout.addWidget(self.filter_status)

        toolbar_layout.addStretch()

        # Tombol Refresh
        self.btn_refresh = QPushButton("🔄  Refresh")
        self.btn_refresh.setObjectName("btnRefresh")
        self.btn_refresh.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_refresh.setToolTip("Muat ulang data (F5)")
        toolbar_layout.addWidget(self.btn_refresh)

        # Tombol Edit
        self.btn_edit = QPushButton("✏️  Edit")
        self.btn_edit.setObjectName("btnEdit")
        self.btn_edit.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_edit.setToolTip("Edit koleksi yang dipilih")
        toolbar_layout.addWidget(self.btn_edit)

        # Tombol Hapus
        self.btn_hapus = QPushButton("🗑️  Hapus")
        self.btn_hapus.setObjectName("btnHapus")
        self.btn_hapus.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_hapus.setToolTip("Hapus koleksi yang dipilih")
        toolbar_layout.addWidget(self.btn_hapus)

        # Tombol Tambah (primary)
        self.btn_tambah = QPushButton("✨  Tambah Koleksi")
        self.btn_tambah.setObjectName("btnTambah")
        self.btn_tambah.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_tambah.setToolTip("Tambah koleksi baru (Ctrl+N)")
        toolbar_layout.addWidget(self.btn_tambah)

        return toolbar_frame

    def _create_table(self) -> QTableWidget:
        """Membuat tabel untuk menampilkan data koleksi."""
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Judul", "Tipe", "Genre",
            "Eps/Ch", "Status", "Rating", "Format", "Ditambahkan",
        ])

        # Konfigurasi tabel
        self.table.setAlternatingRowColors(False)
        self.table.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.table.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.table.setEditTriggers(
            QAbstractItemView.EditTrigger.NoEditTriggers
        )
        self.table.verticalHeader().setVisible(False)
        self.table.setShowGrid(False)

        # Lebar kolom
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 50)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(4, 75)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)

        self.table.verticalHeader().setDefaultSectionSize(44)

        return self.table

    # ================================================================
    # STATUS BAR
    # ================================================================
    def _setup_statusbar(self):
        """Menyiapkan status bar bawah."""
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("✅  OtakuVault siap digunakan")

    # ================================================================
    # CONNECT SIGNALS & SLOTS
    # ================================================================
    def _connect_signals(self):
        """Menghubungkan seluruh signal ke slot yang sesuai."""
        # Tombol
        self.btn_tambah.clicked.connect(self._on_tambah)
        self.btn_edit.clicked.connect(self._on_edit)
        self.btn_hapus.clicked.connect(self._on_hapus)
        self.btn_refresh.clicked.connect(self._refresh_data)

        # Pencarian real-time
        self.input_cari.textChanged.connect(self._on_cari)

        # Filter
        self.filter_tipe.currentTextChanged.connect(self._on_filter_tipe)
        self.filter_status.currentTextChanged.connect(self._on_filter_status)

        # Double-click pada baris untuk edit
        self.table.doubleClicked.connect(self._on_edit)

    # ================================================================
    # SLOT: TAMBAH KOLEKSI
    # ================================================================
    def _on_tambah(self):
        """Membuka dialog tambah koleksi baru."""
        dialog = DialogKoleksi(self, mode="tambah")
        if dialog.exec():
            data = dialog.get_data()
            if data and self.db.tambah_koleksi(data):
                self._refresh_data()
                self.statusbar.showMessage(
                    f"✅  '{data['judul']}' berhasil ditambahkan ke koleksi", 4000
                )
            else:
                QMessageBox.critical(
                    self, "Error",
                    "Gagal menambahkan koleksi ke database."
                )

    # ================================================================
    # SLOT: EDIT KOLEKSI
    # ================================================================
    def _on_edit(self):
        """Membuka dialog edit untuk koleksi yang dipilih."""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(
                self, "Pilih Koleksi",
                "Silakan pilih koleksi yang ingin diedit terlebih dahulu."
            )
            return

        item_id = int(self.table.item(row, 0).text())
        koleksi = self.db.ambil_koleksi_by_id(item_id)

        if not koleksi:
            QMessageBox.warning(
                self, "Data Tidak Ditemukan",
                "Koleksi yang dipilih tidak ditemukan di database."
            )
            return

        data = dict(koleksi)
        dialog = DialogKoleksi(self, mode="edit", data=data)
        if dialog.exec():
            new_data = dialog.get_data()
            if new_data and self.db.update_koleksi(item_id, new_data):
                self._refresh_data()
                self.statusbar.showMessage(
                    f"✅  '{new_data['judul']}' berhasil diperbarui", 4000
                )
            else:
                QMessageBox.critical(
                    self, "Error",
                    "Gagal memperbarui data koleksi."
                )

    # ================================================================
    # SLOT: HAPUS KOLEKSI
    # ================================================================
    def _on_hapus(self):
        """Menghapus koleksi yang dipilih dengan konfirmasi."""
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(
                self, "Pilih Koleksi",
                "Silakan pilih koleksi yang ingin dihapus terlebih dahulu."
            )
            return

        item_id = int(self.table.item(row, 0).text())
        judul = self.table.item(row, 1).text()

        # Dialog konfirmasi (QMessageBox)
        reply = QMessageBox.question(
            self,
            "Konfirmasi Hapus",
            f"Apakah kamu yakin ingin menghapus koleksi:\n\n"
            f"🎌  {judul}\n\n"
            f"Data yang dihapus tidak dapat dikembalikan.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.db.hapus_koleksi(item_id):
                self._refresh_data()
                self.statusbar.showMessage(
                    f"🗑️  '{judul}' berhasil dihapus dari koleksi", 4000
                )
            else:
                QMessageBox.critical(
                    self, "Error",
                    "Gagal menghapus koleksi dari database."
                )

    # ================================================================
    # SLOT: PENCARIAN
    # ================================================================
    def _on_cari(self, keyword: str):
        """Mencari koleksi secara real-time berdasarkan kata kunci."""
        if keyword:
            # Reset filter saat pencarian aktif
            self.filter_tipe.blockSignals(True)
            self.filter_tipe.setCurrentIndex(0)
            self.filter_tipe.blockSignals(False)

            self.filter_status.blockSignals(True)
            self.filter_status.setCurrentIndex(0)
            self.filter_status.blockSignals(False)

            results = self.db.cari_koleksi(keyword)
        else:
            results = self.db.ambil_semua_koleksi()

        self._populate_table(results)

    # ================================================================
    # SLOT: FILTER TIPE
    # ================================================================
    def _on_filter_tipe(self, tipe: str):
        """Filter koleksi berdasarkan tipe yang dipilih."""
        # Reset pencarian dan filter status
        self.input_cari.blockSignals(True)
        self.input_cari.clear()
        self.input_cari.blockSignals(False)

        self.filter_status.blockSignals(True)
        self.filter_status.setCurrentIndex(0)
        self.filter_status.blockSignals(False)

        results = self.db.filter_by_tipe(tipe)
        self._populate_table(results)

    # ================================================================
    # SLOT: FILTER STATUS
    # ================================================================
    def _on_filter_status(self, status: str):
        """Filter koleksi berdasarkan status yang dipilih."""
        # Reset pencarian dan filter tipe
        self.input_cari.blockSignals(True)
        self.input_cari.clear()
        self.input_cari.blockSignals(False)

        self.filter_tipe.blockSignals(True)
        self.filter_tipe.setCurrentIndex(0)
        self.filter_tipe.blockSignals(False)

        results = self.db.filter_by_status(status)
        self._populate_table(results)

    # ================================================================
    # REFRESH & POPULATE
    # ================================================================
    def _refresh_data(self):
        """Memuat ulang seluruh data dan mereset filter/pencarian."""
        # Reset semua input filter
        self.input_cari.blockSignals(True)
        self.input_cari.clear()
        self.input_cari.blockSignals(False)

        self.filter_tipe.blockSignals(True)
        self.filter_tipe.setCurrentIndex(0)
        self.filter_tipe.blockSignals(False)

        self.filter_status.blockSignals(True)
        self.filter_status.setCurrentIndex(0)
        self.filter_status.blockSignals(False)

        data = self.db.ambil_semua_koleksi()
        self._populate_table(data)
        self._update_statistik()

    def _populate_table(self, data: list):
        """Mengisi tabel dengan data koleksi dari database."""
        self.table.setRowCount(0)

        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)

            fields = [
                str(row_data["id"]),
                row_data["judul"],
                row_data["tipe"],
                row_data["genre"],
                str(row_data["episode_chapter"]),
                row_data["status"],
                row_data["rating"],
                row_data["format_media"],
                row_data["tanggal_ditambahkan"],
            ]

            for col, value in enumerate(fields):
                item = QTableWidgetItem(value)

                # Rata tengah untuk ID dan episode/chapter
                if col in (0, 4):
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter
                    )

                # Warna status
                if col == 5:
                    status = value
                    if status == "Selesai":
                        item.setForeground(QColor("#16a34a"))
                    elif status == "Sedang Ditonton/Dibaca":
                        item.setForeground(QColor("#ea580c"))
                    elif status == "Dropped":
                        item.setForeground(QColor("#dc2626"))
                    elif status == "Tertunda (On Hold)":
                        item.setForeground(QColor("#a16207"))
                    elif status == "Rencana Tonton/Baca":
                        item.setForeground(QColor("#6d28d9"))

                # Warna rating (bintang = emas)
                if col == 6 and value != "Belum Dirating":
                    item.setForeground(QColor("#b45309"))

                self.table.setItem(row, col, item)

        self.statusbar.showMessage(
            f"📋  Menampilkan {self.table.rowCount()} koleksi"
        )

    def _update_statistik(self):
        """Memperbarui kartu statistik ringkasan."""
        stats = self.db.get_statistik()

        self.stat_labels["stat_total"].setText(
            str(stats["total_koleksi"])
        )
        self.stat_labels["stat_manga"].setText(
            str(stats["total_manga"])
        )
        self.stat_labels["stat_anime"].setText(
            str(stats["total_anime"])
        )
        self.stat_labels["stat_ongoing"].setText(
            str(stats["sedang_diikuti"])
        )
        self.stat_labels["stat_selesai"].setText(
            str(stats["sudah_selesai"])
        )

    # ================================================================
    # DIALOG TENTANG
    # ================================================================
    def _show_about(self):
        """Menampilkan dialog Tentang Aplikasi."""
        dialog = DialogTentang(self)
        dialog.exec()

    # ================================================================
    # CLOSE EVENT — Konfirmasi keluar
    # ================================================================
    def closeEvent(self, event):
        """Override close event dengan dialog konfirmasi."""
        reply = QMessageBox.question(
            self,
            "Konfirmasi Keluar",
            "Apakah kamu yakin ingin menutup OtakuVault?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db.close()
            event.accept()
        else:
            event.ignore()
