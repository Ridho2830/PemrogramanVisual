# ==========================================
# Nama  : Rafly Ridho' Sukardi
# NIM   : F1D02310134
# Kelas : D
# ==========================================

"""
main_window.py
Window utama dashboard booking ruangan kelas kampus.
Menggabungkan QTableWidget, ChartWidget, filter, CRUD, export PNG.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget, QTableWidgetItem,
    QComboBox, QSplitter, QFrame, QFileDialog, QMessageBox,
    QHeaderView, QAbstractItemView, QScrollArea, QSizePolicy
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QFont, QIcon

from ui.chart_widget import ChartWidget
from ui.crud_dialog import BookingDialog
from data import data_loader


# ─── STYLE SHEET GLOBAL ──────────────────────────────────────────────────────
QSS = """
QMainWindow, QWidget#root {
    background: #0F1923;
}
QSplitter::handle {
    background: #2A3A4A;
    width: 2px;
}
QScrollBar:vertical {
    background: #1A2535;
    width: 8px;
    border-radius: 4px;
}
QScrollBar::handle:vertical {
    background: #2A3A4A;
    border-radius: 4px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }

QTableWidget {
    background: #1A2535;
    color: #E0E0E0;
    gridline-color: #2A3A4A;
    border: none;
    font-size: 13px;
    selection-background-color: #1E3A5F;
    selection-color: #4FC3F7;
    alternate-background-color: #162030;
}
QHeaderView::section {
    background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1A2535, stop:1 #0F1923);
    color: #4FC3F7;
    padding: 8px 6px;
    border: none;
    border-bottom: 2px solid #4FC3F7;
    font-weight: bold;
    font-size: 13px;
}
QTableWidget::item { padding: 6px 6px; }

QComboBox {
    background: #1A2535;
    color: #E0E0E0;
    border: 1px solid #2A3A4A;
    border-radius: 6px;
    padding: 5px 10px;
    font-size: 12px;
    min-width: 140px;
}
QComboBox:hover { border: 1px solid #4FC3F7; }
QComboBox::drop-down { border: none; width: 20px; }
QComboBox QAbstractItemView {
    background: #1A2535;
    color: #E0E0E0;
    selection-background-color: #4FC3F7;
    selection-color: #0F1923;
}

QLabel#stat_val {
    color: #4FC3F7;
    font-size: 22px;
    font-weight: bold;
}
QLabel#stat_lbl {
    color: #78909C;
    font-size: 11px;
}
"""

BTN_PRIMARY = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4FC3F7, stop:1 #0288D1);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 12px;
    }
    QPushButton:hover { background: #81D4FA; }
    QPushButton:pressed { background: #29B6F6; }
"""

BTN_DANGER = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #EF5350, stop:1 #C62828);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 12px;
    }
    QPushButton:hover { background: #EF9A9A; }
"""

BTN_WARNING = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #FFB74D, stop:1 #F57C00);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
        font-size: 12px;
    }
    QPushButton:hover { background: #FFCC80; }
"""

BTN_SECONDARY = """
    QPushButton {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #37474F, stop:1 #263238);
        color: #E0E0E0;
        border: 1px solid #455A64;
        border-radius: 6px;
        padding: 8px 16px;
        font-size: 12px;
        font-weight: bold;
    }
    QPushButton:hover { background: #546E7A; }
"""


# ─── STAT CARD ────────────────────────────────────────────────────────────────
class StatCard(QFrame):
    def __init__(self, icon: str, label: str, value: str, color: str, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QFrame {{
                background: #1A2535;
                border-radius: 12px;
                border-left: 4px solid {color};
            }}
        """)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.setFixedHeight(84)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 10, 14, 10)
        layout.setSpacing(2)

        top = QHBoxLayout()
        ico = QLabel(icon)
        ico.setStyleSheet(f"font-size:20px; background:transparent;")
        top.addWidget(ico)
        top.addStretch()

        self.val_lbl = QLabel(value)
        self.val_lbl.setObjectName("stat_val")
        self.val_lbl.setStyleSheet(f"color:{color}; font-size:22px; font-weight:bold; background:transparent;")

        lbl = QLabel(label)
        lbl.setObjectName("stat_lbl")
        lbl.setStyleSheet("color:#78909C; font-size:11px; background:transparent;")

        layout.addLayout(top)
        layout.addWidget(self.val_lbl)
        layout.addWidget(lbl)

    def update_value(self, v: str):
        self.val_lbl.setText(v)


# ─── MAIN WINDOW ─────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📅  Dashboard Booking Ruangan Kelas – Kampus")
        self.setMinimumSize(1200, 720)
        self.setStyleSheet(QSS)

        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        root_layout = QVBoxLayout(root)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        root_layout.addWidget(self._build_header())

        body = QWidget()
        body.setStyleSheet("background:#0F1923;")
        body_layout = QVBoxLayout(body)
        body_layout.setContentsMargins(16, 12, 16, 12)
        body_layout.setSpacing(12)

        body_layout.addLayout(self._build_stat_cards())
        body_layout.addWidget(self._build_splitter())

        root_layout.addWidget(body)
        self._refresh()

    # ── Header ────────────────────────────────────────────────────────────────
    def _build_header(self):
        header = QFrame()
        header.setFixedHeight(56)
        header.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0D47A1, stop:1 #0F1923);
                border-bottom: 2px solid #4FC3F7;
            }
        """)
        h = QHBoxLayout(header)
        h.setContentsMargins(20, 0, 20, 0)

        title = QLabel("🏫  Dashboard Booking Ruangan Kelas")
        title.setStyleSheet("color:#E0E0E0; font-size:16px; font-weight:bold;")
        sub = QLabel("Sistem Manajemen Peminjaman Ruangan Kampus")
        sub.setStyleSheet("color:#78909C; font-size:11px;")

        left = QVBoxLayout()
        left.setSpacing(0)
        left.addWidget(title)
        left.addWidget(sub)
        h.addLayout(left)
        h.addStretch()

        ver = QLabel("v1.0  •  SQLite + PySide6 + Matplotlib")
        ver.setStyleSheet("color:#546E7A; font-size:10px;")
        h.addWidget(ver)

        return header

    # ── Stat Cards ────────────────────────────────────────────────────────────
    def _build_stat_cards(self):
        row = QHBoxLayout()
        row.setSpacing(12)

        self.card_total    = StatCard("📋", "Total Booking",  "–", "#4FC3F7")
        self.card_disetujui= StatCard("✅", "Disetujui",      "–", "#81C784")
        self.card_pending  = StatCard("⏳", "Pending",         "–", "#FFB74D")
        self.card_ditolak  = StatCard("❌", "Ditolak",         "–", "#EF5350")
        self.card_ruangan  = StatCard("🏠", "Total Ruangan",  "–", "#CE93D8")

        for c in [self.card_total, self.card_disetujui, self.card_pending,
                  self.card_ditolak, self.card_ruangan]:
            row.addWidget(c)
        return row

    def _update_stat_cards(self):
        s = data_loader.summary_stats()
        self.card_total.update_value(str(s["total"]))
        self.card_disetujui.update_value(str(s["disetujui"]))
        self.card_pending.update_value(str(s["pending"]))
        self.card_ditolak.update_value(str(s["ditolak"]))
        self.card_ruangan.update_value(str(s["total_ruangan"]))

    # ── Splitter: Tabel kiri | Panel kanan ────────────────────────────────────
    def _build_splitter(self):
        splitter = QSplitter(Qt.Horizontal)
        splitter.setChildrenCollapsible(False)

        splitter.addWidget(self._build_table_panel())
        splitter.addWidget(self._build_chart_panel())
        splitter.setSizes([600, 560])
        return splitter

    # ── Panel Tabel ───────────────────────────────────────────────────────────
    def _build_table_panel(self):
        panel = QFrame()
        panel.setStyleSheet("QFrame { background:#1A2535; border-radius:12px; }")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Toolbar
        toolbar = QHBoxLayout()
        lbl = QLabel("📄  Data Booking")
        lbl.setStyleSheet("color:#4FC3F7; font-size:13px; font-weight:bold;")
        toolbar.addWidget(lbl)
        toolbar.addStretch()

        # Filter status
        self.cmb_filter_tbl = QComboBox()
        for s in ["Semua", "Disetujui", "Pending", "Ditolak"]:
            self.cmb_filter_tbl.addItem(s)
        self.cmb_filter_tbl.currentTextChanged.connect(self._filter_table)

        btn_add = QPushButton("+ Tambah")
        btn_add.setStyleSheet(BTN_PRIMARY)
        btn_add.clicked.connect(self._add_booking)

        btn_edit = QPushButton("✏ Edit")
        btn_edit.setStyleSheet(BTN_WARNING)
        btn_edit.clicked.connect(self._edit_booking)

        btn_del = QPushButton("🗑 Hapus")
        btn_del.setStyleSheet(BTN_DANGER)
        btn_del.clicked.connect(self._delete_booking)

        btn_refresh = QPushButton("↻ Refresh")
        btn_refresh.setStyleSheet(BTN_SECONDARY)
        btn_refresh.clicked.connect(self._refresh)

        for w in [self.cmb_filter_tbl, btn_add, btn_edit, btn_del, btn_refresh]:
            toolbar.addWidget(w)

        layout.addLayout(toolbar)

        # Tabel
        cols = ["ID", "Ruangan", "Gedung", "Kapasitas",
                "Peminjam", "Prodi", "Tanggal", "Sesi", "Keperluan", "Status"]
        self.table = QTableWidget(0, len(cols))
        self.table.setHorizontalHeaderLabels(cols)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.verticalHeader().setVisible(False)
        self.table.setColumnWidth(0, 40)
        self.table.setColumnWidth(1, 70)
        self.table.setColumnWidth(2, 80)
        self.table.setColumnWidth(3, 75)
        self.table.setColumnWidth(5, 150)
        layout.addWidget(self.table)

        return panel

    # ── Panel Chart ───────────────────────────────────────────────────────────
    def _build_chart_panel(self):
        panel = QFrame()
        panel.setStyleSheet("QFrame { background:#1A2535; border-radius:12px; }")
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # Toolbar chart
        toolbar = QHBoxLayout()
        lbl = QLabel("📊  Visualisasi Chart")
        lbl.setStyleSheet("color:#4FC3F7; font-size:13px; font-weight:bold;")
        toolbar.addWidget(lbl)
        toolbar.addStretch()

        self.cmb_chart = QComboBox()
        for c in ["Pie – Status", "Bar – Program Studi", "Bar – Ruangan",
                  "Line – Tren Bulanan", "Bar – Sesi Waktu"]:
            self.cmb_chart.addItem(c)
        self.cmb_chart.currentTextChanged.connect(self._render_chart)

        self.cmb_filter_chart = QComboBox()
        for s in ["Semua", "Disetujui", "Pending", "Ditolak"]:
            self.cmb_filter_chart.addItem(s)
        self.cmb_filter_chart.currentTextChanged.connect(self._render_chart)

        btn_export = QPushButton("💾 Export PNG")
        btn_export.setStyleSheet(BTN_PRIMARY)
        btn_export.clicked.connect(self._export_chart)

        for w in [self.cmb_chart, self.cmb_filter_chart, btn_export]:
            toolbar.addWidget(w)

        layout.addLayout(toolbar)

        self.chart_widget = ChartWidget()
        layout.addWidget(self.chart_widget)

        return panel

    # ── Refresh ───────────────────────────────────────────────────────────────
    def _refresh(self):
        self._df = data_loader.get_all_bookings()
        self._filter_table()
        self._render_chart()
        self._update_stat_cards()

    # ── Isi Tabel ─────────────────────────────────────────────────────────────
    def _filter_table(self):
        status = self.cmb_filter_tbl.currentText()
        df = self._df if status == "Semua" else self._df[self._df["status"] == status]
        self._populate_table(df)

    def _populate_table(self, df):
        self.table.setRowCount(0)
        status_color = {
            "Disetujui": "#81C784",
            "Pending":   "#FFB74D",
            "Ditolak":   "#EF5350",
        }
        cols_map = ["id", "kode_ruang", "gedung", "kapasitas",
                    "peminjam", "prodi", "tanggal", "sesi", "keperluan", "status"]

        for _, row in df.iterrows():
            r = self.table.rowCount()
            self.table.insertRow(r)
            for c, col in enumerate(cols_map):
                val = str(row[col])
                item = QTableWidgetItem(val)
                item.setTextAlignment(Qt.AlignCenter)
                if col == "status":
                    item.setForeground(QColor(status_color.get(val, "#E0E0E0")))
                    item.setFont(QFont("", -1, QFont.Bold))
                self.table.setItem(r, c, item)

        self.table.resizeRowsToContents()

    # ── Render Chart ──────────────────────────────────────────────────────────
    def _render_chart(self):
        chart_type   = self.cmb_chart.currentText()
        filter_status= self.cmb_filter_chart.currentText()
        self.chart_widget.render(chart_type, filter_status)

    # ── CRUD Actions ──────────────────────────────────────────────────────────
    def _add_booking(self):
        dlg = BookingDialog(self)
        if dlg.exec():
            self._refresh()

    def _edit_booking(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Pilih Baris",
                                "Pilih baris booking yang ingin diedit terlebih dahulu.")
            return
        bid = int(self.table.item(row, 0).text())
        dlg = BookingDialog(self, booking_id=bid)
        if dlg.exec():
            self._refresh()

    def _delete_booking(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Pilih Baris",
                                "Pilih baris booking yang ingin dihapus terlebih dahulu.")
            return
        bid = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(
            self, "Konfirmasi Hapus",
            f"Hapus booking ID {bid}?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            data_loader.delete_booking(bid)
            self._refresh()

    # ── Export PNG ────────────────────────────────────────────────────────────
    def _export_chart(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Simpan Chart sebagai PNG", "chart.png",
            "PNG Image (*.png)"
        )
        if path:
            self.chart_widget.export_png(path)
            QMessageBox.information(self, "Berhasil", f"Chart tersimpan:\n{path}")
