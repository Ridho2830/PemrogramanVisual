import sqlite3
import os
from utils.constants import DB_NAME


class DatabaseManager:
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

        # Tentukan path database di direktori yang sama dengan main.py
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.db_path = os.path.join(base_dir, DB_NAME)
        self.connection = None
        self._connect()
        self._create_tables()

    def _connect(self):
        try:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row
            self.connection.execute("PRAGMA foreign_keys = ON")
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal koneksi database: {e}")

    def _create_tables(self):
        query = """
        CREATE TABLE IF NOT EXISTS inventaris (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_barang TEXT NOT NULL,
            kategori TEXT NOT NULL,
            jumlah INTEGER NOT NULL DEFAULT 0,
            harga REAL NOT NULL DEFAULT 0.0,
            lokasi TEXT NOT NULL,
            kondisi TEXT NOT NULL DEFAULT 'Baru',
            status TEXT NOT NULL DEFAULT 'Tersedia',
            deskripsi TEXT,
            tanggal_masuk TEXT NOT NULL,
            tanggal_update TEXT NOT NULL
        )
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            self.connection.commit()
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal membuat tabel: {e}")

    # ================================================================
    # OPERASI CREATE
    # ================================================================
    def tambah_barang(self, data: dict) -> bool:
        query = """
        INSERT INTO inventaris 
            (nama_barang, kategori, jumlah, harga, lokasi, kondisi, status, deskripsi, tanggal_masuk, tanggal_update)
        VALUES 
            (:nama_barang, :kategori, :jumlah, :harga, :lokasi, :kondisi, :status, :deskripsi, :tanggal_masuk, :tanggal_update)
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, data)
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal menambah barang: {e}")
            return False

    # ================================================================
    # OPERASI READ
    # ================================================================
    def ambil_semua_barang(self) -> list:
        query = "SELECT * FROM inventaris ORDER BY id ASC"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal mengambil data: {e}")
            return []

    def ambil_barang_by_id(self, item_id: int):
        query = "SELECT * FROM inventaris WHERE id = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (item_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal mengambil barang ID {item_id}: {e}")
            return None

    def cari_barang(self, keyword: str) -> list:
        query = """
        SELECT * FROM inventaris 
        WHERE nama_barang LIKE ? OR kategori LIKE ? OR lokasi LIKE ?
        ORDER BY id ASC
        """
        wildcard = f"%{keyword}%"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (wildcard, wildcard, wildcard))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal mencari barang: {e}")
            return []

    def filter_by_kategori(self, kategori: str) -> list:
        if kategori == "Semua Kategori":
            return self.ambil_semua_barang()
        query = "SELECT * FROM inventaris WHERE kategori = ? ORDER BY id ASC"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (kategori,))
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal filter kategori: {e}")
            return []

    # ================================================================
    # OPERASI UPDATE
    # ================================================================
    def update_barang(self, item_id: int, data: dict) -> bool:
        query = """
        UPDATE inventaris SET
            nama_barang = :nama_barang,
            kategori = :kategori,
            jumlah = :jumlah,
            harga = :harga,
            lokasi = :lokasi,
            kondisi = :kondisi,
            status = :status,
            deskripsi = :deskripsi,
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
            print(f"[ERROR] Gagal update barang ID {item_id}: {e}")
            return False

    # ================================================================
    # OPERASI DELETE
    # ================================================================
    def hapus_barang(self, item_id: int) -> bool:
        query = "DELETE FROM inventaris WHERE id = ?"
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, (item_id,))
            self.connection.commit()
            return True
        except sqlite3.Error as e:
            print(f"[ERROR] Gagal hapus barang ID {item_id}: {e}")
            return False

    # ================================================================
    # STATISTIK
    # ================================================================
    def get_statistik(self) -> dict:
        stats = {
            "total_barang": 0,
            "total_stok": 0,
            "total_nilai": 0.0,
            "stok_menipis": 0,
            "habis": 0,
        }
        try:
            cursor = self.connection.cursor()

            # Total jenis barang
            cursor.execute("SELECT COUNT(*) FROM inventaris")
            stats["total_barang"] = cursor.fetchone()[0]

            # Total stok keseluruhan
            cursor.execute("SELECT COALESCE(SUM(jumlah), 0) FROM inventaris")
            stats["total_stok"] = cursor.fetchone()[0]

            # Total nilai inventaris
            cursor.execute(
                "SELECT COALESCE(SUM(jumlah * harga), 0) FROM inventaris"
            )
            stats["total_nilai"] = cursor.fetchone()[0]

            # Jumlah barang stok menipis
            cursor.execute(
                "SELECT COUNT(*) FROM inventaris WHERE status = 'Stok Menipis'"
            )
            stats["stok_menipis"] = cursor.fetchone()[0]

            # Jumlah barang habis
            cursor.execute(
                "SELECT COUNT(*) FROM inventaris WHERE status = 'Habis'"
            )
            stats["habis"] = cursor.fetchone()[0]

        except sqlite3.Error as e:
            print(f"[ERROR] Gagal mengambil statistik: {e}")

        return stats

    def close(self):
        if self.connection:
            self.connection.close()
