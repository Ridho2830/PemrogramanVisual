# ==========================================
# Nama  : Rafly Ridho' Sukardi
# NIM   : F1D02310134
# Kelas : D
# ==========================================

from PySide6.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import pandas as pd

# ── Palet Warna Tema ──────────────────────────────────────────────────────────
BG_COLOR    = "#0F1923"
PANEL_COLOR = "#1A2535"
ACCENT1     = "#4FC3F7"   # biru muda
ACCENT2     = "#81C784"   # hijau
ACCENT3     = "#FFB74D"   # oranye
ACCENT4     = "#EF5350"   # merah
TEXT_COLOR  = "#E0E0E0"
GRID_COLOR  = "#2A3A4A"

PALETTE = [ACCENT1, ACCENT2, ACCENT3, ACCENT4,
           "#CE93D8", "#F48FB1", "#80DEEA", "#FFCC02"]


def _apply_dark_style(ax, fig):
    fig.patch.set_facecolor(PANEL_COLOR)
    ax.set_facecolor(PANEL_COLOR)
    ax.tick_params(colors=TEXT_COLOR, labelsize=9)
    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.yaxis.label.set_color(TEXT_COLOR)
    ax.title.set_color(TEXT_COLOR)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_COLOR)
    ax.grid(color=GRID_COLOR, linestyle="--", linewidth=0.5, alpha=0.7)


class ChartCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig = Figure(facecolor=PANEL_COLOR, tight_layout=True)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.updateGeometry()

    def _clear(self):
        self.fig.clear()

    # ── Chart 1: Pie – Booking per Status ────────────────────────────────────
    def plot_pie_status(self, df: pd.DataFrame):
        self._clear()
        ax = self.fig.add_subplot(111)
        ax.set_facecolor(PANEL_COLOR)
        self.fig.patch.set_facecolor(PANEL_COLOR)

        colors = {"Disetujui": ACCENT2, "Pending": ACCENT3, "Ditolak": ACCENT4}
        pie_colors = [colors.get(s, ACCENT1) for s in df["status"]]

        wedges, texts, autotexts = ax.pie(
            df["jumlah"],
            labels=df["status"],
            autopct="%1.1f%%",
            colors=pie_colors,
            startangle=140,
            pctdistance=0.75,
            wedgeprops=dict(width=0.55, edgecolor=PANEL_COLOR, linewidth=2),
        )
        for t in texts:
            t.set_color(TEXT_COLOR)
            t.set_fontsize(10)
        for at in autotexts:
            at.set_color(BG_COLOR)
            at.set_fontweight("bold")
            at.set_fontsize(9)

        ax.set_title("Distribusi Status Booking", color=TEXT_COLOR,
                     fontsize=13, fontweight="bold", pad=15)
        self.draw()

    # ── Chart 2: Bar – Booking per Prodi ─────────────────────────────────────
    def plot_bar_prodi(self, df: pd.DataFrame):
        self._clear()
        ax = self.fig.add_subplot(111)
        _apply_dark_style(ax, self.fig)

        bars = ax.barh(df["prodi"], df["jumlah"],
                       color=PALETTE[:len(df)], edgecolor=PANEL_COLOR, height=0.6)

        ax.set_xlabel("Jumlah Booking", color=TEXT_COLOR)
        ax.set_title("Booking per Program Studi", color=TEXT_COLOR,
                     fontsize=13, fontweight="bold")
        ax.invert_yaxis()

        for bar in bars:
            w = bar.get_width()
            ax.text(w + 0.2, bar.get_y() + bar.get_height() / 2,
                    str(int(w)), va="center", color=TEXT_COLOR, fontsize=9)

        ax.set_axisbelow(True)
        ax.grid(axis="x", color=GRID_COLOR, linestyle="--", linewidth=0.5)
        ax.grid(axis="y", visible=False)
        self.draw()

    # ── Chart 3: Bar – Booking per Ruangan ───────────────────────────────────
    def plot_bar_room(self, df: pd.DataFrame):
        self._clear()
        ax = self.fig.add_subplot(111)
        _apply_dark_style(ax, self.fig)

        bars = ax.bar(df["kode_ruang"], df["jumlah"],
                      color=ACCENT1, edgecolor=PANEL_COLOR, width=0.6)

        ax.set_xlabel("Kode Ruangan", color=TEXT_COLOR)
        ax.set_ylabel("Jumlah Booking", color=TEXT_COLOR)
        ax.set_title("Booking per Ruangan", color=TEXT_COLOR,
                     fontsize=13, fontweight="bold")

        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + 0.2,
                    str(int(h)), ha="center", color=TEXT_COLOR, fontsize=9)

        ax.set_axisbelow(True)
        ax.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.5)
        ax.grid(axis="x", visible=False)
        self.draw()

    # ── Chart 4: Line – Trend Bulanan ────────────────────────────────────────
    def plot_line_monthly(self, df: pd.DataFrame):
        self._clear()
        ax = self.fig.add_subplot(111)
        _apply_dark_style(ax, self.fig)

        ax.plot(df["bulan"], df["jumlah"],
                color=ACCENT3, linewidth=2.5, marker="o",
                markersize=7, markerfacecolor=ACCENT4, markeredgecolor=PANEL_COLOR)
        ax.fill_between(df["bulan"], df["jumlah"],
                        color=ACCENT3, alpha=0.15)

        ax.set_xlabel("Bulan", color=TEXT_COLOR)
        ax.set_ylabel("Jumlah Booking", color=TEXT_COLOR)
        ax.set_title("Tren Booking per Bulan", color=TEXT_COLOR,
                     fontsize=13, fontweight="bold")
        ax.tick_params(axis="x", rotation=45)
        ax.set_axisbelow(True)
        self.draw()

    # ── Chart 5: Bar – Booking per Sesi ──────────────────────────────────────
    def plot_bar_sesi(self, df: pd.DataFrame):
        self._clear()
        ax = self.fig.add_subplot(111)
        _apply_dark_style(ax, self.fig)

        bars = ax.bar(df["sesi"], df["jumlah"],
                      color=ACCENT2, edgecolor=PANEL_COLOR, width=0.5)

        ax.set_xlabel("Sesi Waktu", color=TEXT_COLOR)
        ax.set_ylabel("Jumlah Booking", color=TEXT_COLOR)
        ax.set_title("Booking per Sesi Waktu", color=TEXT_COLOR,
                     fontsize=13, fontweight="bold")
        ax.tick_params(axis="x", rotation=30)

        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, h + 0.2,
                    str(int(h)), ha="center", color=TEXT_COLOR, fontsize=9)

        ax.set_axisbelow(True)
        ax.grid(axis="y", color=GRID_COLOR, linestyle="--", linewidth=0.5)
        ax.grid(axis="x", visible=False)
        self.draw()


class ChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.canvas = ChartCanvas(self)
        layout.addWidget(self.canvas)

    def render(self, chart_type: str, filter_status: str = "Semua"):
        from data.data_loader import (
            bookings_by_status, bookings_by_prodi,
            bookings_by_room, bookings_by_month, bookings_by_sesi,
            get_all_bookings,
        )

        if chart_type == "Pie – Status":
            df = bookings_by_status()
            if filter_status != "Semua":
                df = df[df["status"] == filter_status]
            self.canvas.plot_pie_status(df)

        elif chart_type == "Bar – Program Studi":
            df = bookings_by_prodi()
            self.canvas.plot_bar_prodi(df)

        elif chart_type == "Bar – Ruangan":
            df = bookings_by_room()
            self.canvas.plot_bar_room(df)

        elif chart_type == "Line – Tren Bulanan":
            df = bookings_by_month()
            self.canvas.plot_line_monthly(df)

        elif chart_type == "Bar – Sesi Waktu":
            df = bookings_by_sesi()
            self.canvas.plot_bar_sesi(df)

    def export_png(self, path: str):
        self.canvas.fig.savefig(path, dpi=150, bbox_inches="tight",
                                facecolor=PANEL_COLOR)
