# ==========================================
# Nama  : Rafly Ridho' Sukardi
# NIM   : F1D02310134
# Kelas : D
# ==========================================

import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "bookings.db")


def _conn():
    return sqlite3.connect(DB_PATH)


# ── READ ──────────────────────────────────────────────────────────────────────

def get_all_bookings() -> pd.DataFrame:
    """Ambil semua booking beserta info ruangan (JOIN)."""
    sql = """
        SELECT
            b.id,
            r.kode_ruang,
            r.gedung,
            r.kapasitas,
            b.peminjam,
            b.prodi,
            b.tanggal,
            b.sesi,
            b.keperluan,
            b.status
        FROM bookings b
        JOIN rooms r ON b.room_id = r.id
        ORDER BY b.tanggal DESC
    """
    with _conn() as conn:
        return pd.read_sql_query(sql, conn)


def get_rooms() -> pd.DataFrame:
    with _conn() as conn:
        return pd.read_sql_query("SELECT * FROM rooms", conn)


def get_booking_by_id(booking_id: int) -> dict | None:
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM bookings WHERE id=?", (booking_id,))
        row = cur.fetchone()
        if row:
            cols = [d[0] for d in cur.description]
            return dict(zip(cols, row))
    return None


# ── CREATE ────────────────────────────────────────────────────────────────────

def add_booking(room_id: int, peminjam: str, prodi: str,
                tanggal: str, sesi: str, keperluan: str, status: str = "Pending") -> int:
    sql = """
        INSERT INTO bookings (room_id, peminjam, prodi, tanggal, sesi, keperluan, status)
        VALUES (?,?,?,?,?,?,?)
    """
    with _conn() as conn:
        cur = conn.cursor()
        cur.execute(sql, (room_id, peminjam, prodi, tanggal, sesi, keperluan, status))
        conn.commit()
        return cur.lastrowid


# ── UPDATE ────────────────────────────────────────────────────────────────────

def update_booking(booking_id: int, room_id: int, peminjam: str, prodi: str, tanggal: str, sesi: str, keperluan: str, status: str):
    sql = """
        UPDATE bookings 
        SET room_id=?, peminjam=?, prodi=?, tanggal=?, sesi=?, keperluan=?, status=?
        WHERE id=?
    """
    with _conn() as conn:
        conn.execute(sql, (room_id, peminjam, prodi, tanggal, sesi, keperluan, status, booking_id))
        conn.commit()

def update_booking_status(booking_id: int, status: str):
    with _conn() as conn:
        conn.execute(
            "UPDATE bookings SET status=? WHERE id=?", (status, booking_id)
        )
        conn.commit()


# ── DELETE ────────────────────────────────────────────────────────────────────

def delete_booking(booking_id: int):
    with _conn() as conn:
        conn.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
        conn.commit()


# ── AGREGASI untuk Chart ──────────────────────────────────────────────────────

def bookings_by_status() -> pd.DataFrame:
    sql = "SELECT status, COUNT(*) as jumlah FROM bookings GROUP BY status"
    with _conn() as conn:
        return pd.read_sql_query(sql, conn)


def bookings_by_prodi() -> pd.DataFrame:
    sql = "SELECT prodi, COUNT(*) as jumlah FROM bookings GROUP BY prodi ORDER BY jumlah DESC"
    with _conn() as conn:
        return pd.read_sql_query(sql, conn)


def bookings_by_room() -> pd.DataFrame:
    sql = """
        SELECT r.kode_ruang, COUNT(*) as jumlah
        FROM bookings b JOIN rooms r ON b.room_id = r.id
        GROUP BY r.kode_ruang ORDER BY jumlah DESC
    """
    with _conn() as conn:
        return pd.read_sql_query(sql, conn)


def bookings_by_month() -> pd.DataFrame:
    sql = """
        SELECT strftime('%Y-%m', tanggal) as bulan, COUNT(*) as jumlah
        FROM bookings GROUP BY bulan ORDER BY bulan
    """
    with _conn() as conn:
        return pd.read_sql_query(sql, conn)


def bookings_by_sesi() -> pd.DataFrame:
    sql = "SELECT sesi, COUNT(*) as jumlah FROM bookings GROUP BY sesi ORDER BY sesi"
    with _conn() as conn:
        return pd.read_sql_query(sql, conn)


def summary_stats() -> dict:
    df = get_all_bookings()
    return {
        "total": len(df),
        "disetujui": len(df[df["status"] == "Disetujui"]),
        "pending": len(df[df["status"] == "Pending"]),
        "ditolak": len(df[df["status"] == "Ditolak"]),
        "total_ruangan": len(get_rooms()),
    }
