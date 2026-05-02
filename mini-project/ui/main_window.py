
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel,
    QFrame, QLineEdit, QComboBox, QMenuBar, QMenu,
    QStatusBar, QMessageBox, QHeaderView, QSpacerItem,
    QSizePolicy, QAbstractItemView,
)
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QAction, QColor

from database.db_manager import DatabaseManager
from ui.dialogs import DialogBarang, DialogTentang
from utils.constants import (
    APP_NAME, NAMA_MAHASISWA, NIM_MAHASISWA, KATEGORI_BARANG,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = DatabaseManager()

        self.setWindowTitle(APP_NAME)
        self.setMinimumSize(1100, 700)
        self.resize(1280, 780)

        self._setup_menubar()
        self._setup_ui()
        self._setup_statusbar()
        self._connect_signals()

        # Muat data awal
        self._refresh_data()

    # ================================================================
    # SETUP MENU BAR
    # ================================================================
    def _setup_menubar(self):
        menubar = self.menuBar()

        # Menu File
        menu_file = QMenu("File", self)
        menubar.addMenu(menu_file)

        action_tambah = QAction("➕  Tambah Barang", self)
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

        # Menu Tentang
        menu_tentang = QMenu("Tentang", self)
        menubar.addMenu(menu_tentang)

        action_about = QAction("ℹ️  Tentang Aplikasi", self)
        action_about.triggered.connect(self._show_about)
        menu_tentang.addAction(action_about)

    # ================================================================
    # SETUP UI
    # ================================================================
    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(24, 20, 24, 16)

        # --- HEADER ---
        main_layout.addLayout(self._create_header())

        # --- STATISTIK CARDS ---
        main_layout.addLayout(self._create_stat_cards())

        # --- TOOLBAR (Search, Filter, Buttons) ---
        main_layout.addWidget(self._create_toolbar())

        # --- TABEL DATA ---
        main_layout.addWidget(self._create_table())

    def _create_header(self) -> QHBoxLayout:
        header_layout = QHBoxLayout()

        # Kiri: Judul dan subtitle
        left_layout = QVBoxLayout()
        left_layout.setSpacing(2)

        label_judul = QLabel("📦  InvenTrack")
        label_judul.setObjectName("labelJudul")
        left_layout.addWidget(label_judul)

        label_subtitle = QLabel("Sistem Manajemen Inventaris Modern")
        label_subtitle.setObjectName("labelSubtitle")
        left_layout.addWidget(label_subtitle)

        header_layout.addLayout(left_layout)
        header_layout.addStretch()

        # Kanan: Identitas mahasiswa (tidak bisa diedit)
        label_identitas = QLabel(
            f"👤  {NAMA_MAHASISWA}  •  NIM: {NIM_MAHASISWA}"
        )
        label_identitas.setObjectName("labelIdentitas")
        header_layout.addWidget(label_identitas)

        return header_layout

    def _create_stat_cards(self) -> QHBoxLayout:
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(12)

        # Definisi kartu statistik
        stat_configs = [
            ("📊", "Total Jenis", "stat_total_jenis", "#0369a1"),
            ("📦", "Total Stok", "stat_total_stok", "#15803d"),
            ("💰", "Nilai Inventaris", "stat_total_nilai", "#c2410c"),
            ("⚠️", "Stok Menipis", "stat_menipis", "#a16207"),
            ("🚫", "Stok Habis", "stat_habis", "#dc2626"),
        ]

        self.stat_labels = {}

        for icon, title, key, accent_color in stat_configs:
            frame = QFrame()
            frame.setObjectName("frameStat")
            frame.setMinimumHeight(95)

            frame_layout = QHBoxLayout(frame)
            frame_layout.setContentsMargins(16, 12, 16, 12)
            frame_layout.setSpacing(12)

            # Icon
            icon_label = QLabel(icon)
            icon_label.setObjectName("labelStatIcon")
            frame_layout.addWidget(icon_label)

            # Text container
            text_layout = QVBoxLayout()
            text_layout.setSpacing(2)

            title_label = QLabel(title.upper())
            title_label.setObjectName("labelStatTitle")
            text_layout.addWidget(title_label)

            value_label = QLabel("0")
            value_label.setObjectName("labelStatValue")
            value_label.setStyleSheet(f"color: {accent_color};")
            text_layout.addWidget(value_label)

            self.stat_labels[key] = value_label
            frame_layout.addLayout(text_layout)
            frame_layout.addStretch()

            stats_layout.addWidget(frame)

        return stats_layout

    def _create_toolbar(self) -> QFrame:
        toolbar_frame = QFrame()
        toolbar_frame.setObjectName("frameToolbar")

        toolbar_layout = QHBoxLayout(toolbar_frame)
        toolbar_layout.setContentsMargins(14, 10, 14, 10)
        toolbar_layout.setSpacing(10)

        # Pencarian
        self.input_cari = QLineEdit()
        self.input_cari.setPlaceholderText("🔍  Cari barang...")
        self.input_cari.setMinimumWidth(260)
        self.input_cari.setClearButtonEnabled(True)
        toolbar_layout.addWidget(self.input_cari)

        # Filter kategori
        self.filter_kategori = QComboBox()
        self.filter_kategori.addItem("Semua Kategori")
        self.filter_kategori.addItems(KATEGORI_BARANG)
        self.filter_kategori.setMinimumWidth(180)
        toolbar_layout.addWidget(self.filter_kategori)

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
        self.btn_edit.setToolTip("Edit barang yang dipilih")
        toolbar_layout.addWidget(self.btn_edit)

        # Tombol Hapus
        self.btn_hapus = QPushButton("🗑️  Hapus")
        self.btn_hapus.setObjectName("btnHapus")
        self.btn_hapus.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_hapus.setToolTip("Hapus barang yang dipilih")
        toolbar_layout.addWidget(self.btn_hapus)

        # Tombol Tambah (primary)
        self.btn_tambah = QPushButton("➕  Tambah Barang")
        self.btn_tambah.setObjectName("btnTambah")
        self.btn_tambah.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_tambah.setToolTip("Tambah barang baru (Ctrl+N)")
        toolbar_layout.addWidget(self.btn_tambah)

        return toolbar_frame

    def _create_table(self) -> QTableWidget:
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            "ID", "Nama Barang", "Kategori", "Jumlah",
            "Harga (Rp)", "Lokasi", "Kondisi", "Status", "Tgl Masuk",
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

        # Atur lebar kolom
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(0, 50)
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(3, 80)
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(7, QHeaderView.ResizeMode.ResizeToContents)
        header.setSectionResizeMode(8, QHeaderView.ResizeMode.ResizeToContents)

        # Tinggi baris
        self.table.verticalHeader().setDefaultSectionSize(44)

        return self.table

    # ================================================================
    # SETUP STATUS BAR
    # ================================================================
    def _setup_statusbar(self):
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        self.statusbar.showMessage("✅  InvenTrack siap digunakan")

    # ================================================================
    # CONNECT SIGNALS & SLOTS
    # ================================================================
    def _connect_signals(self):
        # Tombol toolbar
        self.btn_tambah.clicked.connect(self._on_tambah)
        self.btn_edit.clicked.connect(self._on_edit)
        self.btn_hapus.clicked.connect(self._on_hapus)
        self.btn_refresh.clicked.connect(self._refresh_data)

        # Pencarian real-time
        self.input_cari.textChanged.connect(self._on_cari)

        # Filter kategori
        self.filter_kategori.currentTextChanged.connect(self._on_filter)

        # Double-click pada tabel untuk edit
        self.table.doubleClicked.connect(self._on_edit)

    # ================================================================
    # SLOT: OPERASI DATA
    # ================================================================
    def _on_tambah(self):
        dialog = DialogBarang(self, mode="tambah")
        if dialog.exec():
            data = dialog.get_data()
            if data and self.db.tambah_barang(data):
                self._refresh_data()
                self.statusbar.showMessage(
                    f"✅  Barang '{data['nama_barang']}' berhasil ditambahkan", 4000
                )
            else:
                QMessageBox.critical(
                    self, "Error",
                    "Gagal menambahkan barang ke database."
                )

    def _on_edit(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(
                self, "Pilih Barang",
                "Silakan pilih barang yang ingin diedit terlebih dahulu."
            )
            return

        # Ambil ID dari kolom pertama
        item_id = int(self.table.item(row, 0).text())
        barang = self.db.ambil_barang_by_id(item_id)

        if not barang:
            QMessageBox.warning(
                self, "Data Tidak Ditemukan",
                "Barang yang dipilih tidak ditemukan di database."
            )
            return

        # Konversi sqlite3.Row ke dict
        data = dict(barang)

        dialog = DialogBarang(self, mode="edit", data=data)
        if dialog.exec():
            new_data = dialog.get_data()
            if new_data and self.db.update_barang(item_id, new_data):
                self._refresh_data()
                self.statusbar.showMessage(
                    f"✅  Data '{new_data['nama_barang']}' berhasil diperbarui", 4000
                )
            else:
                QMessageBox.critical(
                    self, "Error",
                    "Gagal memperbarui data barang."
                )

    def _on_hapus(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(
                self, "Pilih Barang",
                "Silakan pilih barang yang ingin dihapus terlebih dahulu."
            )
            return

        item_id = int(self.table.item(row, 0).text())
        nama = self.table.item(row, 1).text()

        # Dialog konfirmasi (QMessageBox)
        reply = QMessageBox.question(
            self,
            "Konfirmasi Hapus",
            f"Apakah Anda yakin ingin menghapus barang:\n\n"
            f"📦  {nama}\n\n"
            f"Data yang dihapus tidak dapat dikembalikan.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.db.hapus_barang(item_id):
                self._refresh_data()
                self.statusbar.showMessage(
                    f"🗑️  Barang '{nama}' berhasil dihapus", 4000
                )
            else:
                QMessageBox.critical(
                    self, "Error",
                    "Gagal menghapus barang dari database."
                )

    def _on_cari(self, keyword: str):
        # Reset filter kategori saat pencarian aktif
        if keyword:
            self.filter_kategori.blockSignals(True)
            self.filter_kategori.setCurrentIndex(0)
            self.filter_kategori.blockSignals(False)
            results = self.db.cari_barang(keyword)
        else:
            results = self.db.ambil_semua_barang()

        self._populate_table(results)

    def _on_filter(self, kategori: str):
        # Reset pencarian saat filter aktif
        if kategori != "Semua Kategori":
            self.input_cari.blockSignals(True)
            self.input_cari.clear()
            self.input_cari.blockSignals(False)

        results = self.db.filter_by_kategori(kategori)
        self._populate_table(results)

    # ================================================================
    # REFRESH & POPULATE
    # ================================================================
    def _refresh_data(self):
        # Reset pencarian dan filter
        self.input_cari.blockSignals(True)
        self.input_cari.clear()
        self.input_cari.blockSignals(False)

        self.filter_kategori.blockSignals(True)
        self.filter_kategori.setCurrentIndex(0)
        self.filter_kategori.blockSignals(False)

        data = self.db.ambil_semua_barang()
        self._populate_table(data)
        self._update_statistik()

    def _populate_table(self, data: list):
        self.table.setRowCount(0)

        for row_data in data:
            row = self.table.rowCount()
            self.table.insertRow(row)

            # Kolom: ID, Nama, Kategori, Jumlah, Harga, Lokasi, Kondisi, Status, Tgl Masuk
            fields = [
                str(row_data["id"]),
                row_data["nama_barang"],
                row_data["kategori"],
                str(row_data["jumlah"]),
                f'{row_data["harga"]:,.2f}',
                row_data["lokasi"],
                row_data["kondisi"],
                row_data["status"],
                row_data["tanggal_masuk"],
            ]

            for col, value in enumerate(fields):
                item = QTableWidgetItem(value)

                # Rata tengah untuk kolom numerik
                if col in (0, 3):
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignCenter
                    )
                elif col == 4:
                    item.setTextAlignment(
                        Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter
                    )

                # Warna status (disesuaikan untuk tema light)
                if col == 7:
                    status = value
                    if status == "Habis":
                        item.setForeground(QColor("#dc2626"))
                    elif status == "Stok Menipis":
                        item.setForeground(QColor("#a16207"))
                    elif status == "Tersedia":
                        item.setForeground(QColor("#15803d"))

                self.table.setItem(row, col, item)

        # Update jumlah di status bar
        self.statusbar.showMessage(
            f"📋  Menampilkan {self.table.rowCount()} barang"
        )

    def _update_statistik(self):
        stats = self.db.get_statistik()

        self.stat_labels["stat_total_jenis"].setText(
            str(stats["total_barang"])
        )
        self.stat_labels["stat_total_stok"].setText(
            str(stats["total_stok"])
        )
        self.stat_labels["stat_total_nilai"].setText(
            f'Rp {stats["total_nilai"]:,.0f}'
        )
        self.stat_labels["stat_menipis"].setText(
            str(stats["stok_menipis"])
        )
        self.stat_labels["stat_habis"].setText(
            str(stats["habis"])
        )

    # ================================================================
    # DIALOG TENTANG
    # ================================================================
    def _show_about(self):
        dialog = DialogTentang(self)
        dialog.exec()

    # ================================================================
    # OVERRIDE: CLOSE EVENT
    # ================================================================
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Konfirmasi Keluar",
            "Apakah Anda yakin ingin menutup InvenTrack?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.db.close()
            event.accept()
        else:
            event.ignore()
