"""
db_manager.py — Modul pengelolaan database SQLite untuk OtakuVault.
Menangani koneksi, pembuatan tabel, serta operasi CRUD koleksi manga/anime.
"""

import sqlite3
import os
from utils.constants import DB_NAME


class DatabaseManager:
    """Singleton manager untuk operasi database SQLite."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True

        # Path database di root project (sejajar main.py)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(base_dir, DB_NAME)
        self.connection = None
        self._connect()
        self._create_tables()

    def _connect(self):
        """Membuka koneksi ke file SQLite."""
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.connection.execute("PRAGMA foreign_keys = ON")
            print(f"[INFO] Database terhubung: {self.db_path}")
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal koneksi database: {e}")

    def _create_tables(self):
        """Membuat tabel koleksi jika belum ada."""
        query = """
        CREATE TABLE IF NOT EXISTS koleksi (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            judul TEXT NOT NULL,
            tipe TEXT NOT NULL,
            genre TEXT NOT NULL,
            episode_chapter INTEGER NOT NULL DEFAULT 0,
            status TEXT NOT NULL DEFAULT 'Rencana Tonton/Baca',
            rating TEXT NOT NULL DEFAULT 'Belum Dirating',
            format_media TEXT NOT NULL DEFAULT 'TV Series',
            catatan TEXT,
            tanggal_ditambahkan TEXT NOT NULL,
            tanggal_update TEXT NOT NULL
        )
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
            print("[INFO] Tabel 'koleksi' siap digunakan.")
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal membuat tabel: {e}")

    # ================================================================
    # OPERASI CREATE
    # ================================================================
    def tambah_koleksi(self, data: dict) -> bool:
        """Menyimpan entri koleksi baru ke database."""
        query = """
        INSERT INTO koleksi
            (judul, tipe, genre, episode_chapter, status, rating,
             format_media, catatan, tanggal_ditambahkan, tanggal_update)
        VALUES
            (:judul, :tipe, :genre, :episode_chapter, :status, :rating,
             :format_media, :catatan, :tanggal_ditambahkan, :tanggal_update)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, data)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal menambah koleksi: {e}")
            return False

    # ================================================================
    # OPERASI READ
    # ================================================================
    def ambil_semua_koleksi(self) -> list:
        """Mengambil seluruh koleksi, diurutkan berdasarkan ID."""
        query = "SELECT * FROM koleksi ORDER BY id DESC"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal mengambil data: {e}")
            return []

    def ambil_koleksi_by_id(self, item_id: int):
        """Mengambil satu koleksi berdasarkan ID."""
        query = "SELECT * FROM koleksi WHERE id = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (item_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal mengambil koleksi ID {item_id}: {e}")
            return None

    def cari_koleksi(self, keyword: str) -> list:
        """Mencari koleksi berdasarkan judul, tipe, atau genre."""
        query = """
        SELECT * FROM koleksi
        WHERE judul LIKE ? OR tipe LIKE ? OR genre LIKE ?
        ORDER BY id DESC
        """
        wildcard = f"%{keyword}%"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (wildcard, wildcard, wildcard))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal mencari koleksi: {e}")
            return []

    def filter_by_tipe(self, tipe: str) -> list:
        """Filter koleksi berdasarkan tipe (Manga, Anime, dll.)."""
        if tipe == "Semua Tipe":
            return self.ambil_semua_koleksi()
        query = "SELECT * FROM koleksi WHERE tipe = ? ORDER BY id DESC"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (tipe,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal filter tipe: {e}")
            return []

    def filter_by_status(self, status: str) -> list:
        """Filter koleksi berdasarkan status."""
        if status == "Semua Status":
            return self.ambil_semua_koleksi()
        query = "SELECT * FROM koleksi WHERE status = ? ORDER BY id DESC"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (status,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal filter status: {e}")
            return []

    # ================================================================
    # OPERASI UPDATE
    # ================================================================
    def update_koleksi(self, item_id: int, data: dict) -> bool:
        """Memperbarui data koleksi yang sudah ada."""
        query = """
        UPDATE koleksi SET
            judul = :judul,
            tipe = :tipe,
            genre = :genre,
            episode_chapter = :episode_chapter,
            status = :status,
            rating = :rating,
            format_media = :format_media,
            catatan = :catatan,
            tanggal_update = :tanggal_update
        WHERE id = :id
        """
        data["id"] = item_id
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, data)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal update koleksi ID {item_id}: {e}")
            return False

    # ================================================================
    # OPERASI DELETE
    # ================================================================
    def hapus_koleksi(self, item_id: int) -> bool:
        """Menghapus satu entri koleksi berdasarkan ID."""
        query = "DELETE FROM koleksi WHERE id = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (item_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal hapus koleksi ID {item_id}: {e}")
            return False

    # ================================================================
    # STATISTIK KOLEKSI
    # ================================================================
    def get_statistik(self) -> dict:
        """Menghitung ringkasan statistik koleksi."""
        stats = {
            "total_koleksi": 0,
            "total_manga": 0,
            "total_anime": 0,
            "sedang_diikuti": 0,
            "sudah_selesai": 0,
        }
        try:
            cursor = self.connection.cursor()

            cursor.execute("SELECT COUNT(*) FROM koleksi")
            stats["total_koleksi"] = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM koleksi WHERE tipe = 'Manga'"
            )
            stats["total_manga"] = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM koleksi WHERE tipe = 'Anime'"
            )
            stats["total_anime"] = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM koleksi WHERE status = 'Sedang Ditonton/Dibaca'"
            )
            stats["sedang_diikuti"] = cursor.fetchone()[0]

            cursor.execute(
                "SELECT COUNT(*) FROM koleksi WHERE status = 'Selesai'"
            )
            stats["sudah_selesai"] = cursor.fetchone()[0]

        except sqlite3.Error as e:
            print(f"[ERROR] Gagal mengambil statistik: {e}")

        return stats

    def close(self):
        """Menutup koneksi database."""
        if self.connection:
            self.connection.close()
            print("[INFO] Database ditutup.")
