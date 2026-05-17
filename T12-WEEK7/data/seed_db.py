# ==========================================
# Nama  : Rafly Ridho' Sukardi
# NIM   : F1D02310134
# Kelas : D
# ==========================================

"""
seed_db.py
Membuat dan mengisi database SQLite dengan data booking ruangan kelas kampus.
"""

import sqlite3
import random
from datetime import date, timedelta
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "bookings.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # Tabel ruangan
    cur.execute("""
        CREATE TABLE IF NOT EXISTS rooms (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            kode_ruang  TEXT NOT NULL UNIQUE,
            gedung      TEXT NOT NULL,
            kapasitas   INTEGER NOT NULL,
            fasilitas   TEXT
        )
    """)

    # Tabel booking
    cur.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id     INTEGER NOT NULL,
            peminjam    TEXT NOT NULL,
            prodi       TEXT NOT NULL,
            tanggal     TEXT NOT NULL,
            sesi        TEXT NOT NULL,
            keperluan   TEXT NOT NULL,
            status      TEXT NOT NULL DEFAULT 'Pending',
            FOREIGN KEY (room_id) REFERENCES rooms(id)
        )
    """)

    conn.commit()

    # Seed rooms jika kosong
    cur.execute("SELECT COUNT(*) FROM rooms")
    if cur.fetchone()[0] == 0:
        rooms = [
            ("A101", "Gedung A", 40, "Proyektor, AC, Whiteboard"),
            ("A102", "Gedung A", 35, "Proyektor, AC"),
            ("A201", "Gedung A", 50, "Proyektor, AC, Lab Komputer"),
            ("B101", "Gedung B", 30, "Proyektor, Kipas"),
            ("B102", "Gedung B", 45, "Proyektor, AC, Whiteboard"),
            ("B201", "Gedung B", 60, "Proyektor, AC, Podium"),
            ("C101", "Gedung C", 40, "Proyektor, AC"),
            ("C102", "Gedung C", 35, "AC, Whiteboard"),
            ("LAB01", "Lab Terpadu", 25, "Komputer, AC, Proyektor"),
            ("AULA", "Aula Utama", 200, "Sound System, AC, Proyektor"),
        ]
        cur.executemany(
            "INSERT INTO rooms (kode_ruang, gedung, kapasitas, fasilitas) VALUES (?,?,?,?)",
            rooms,
        )
        conn.commit()

    # Seed bookings jika kosong
    cur.execute("SELECT COUNT(*) FROM bookings")
    if cur.fetchone()[0] == 0:
        peminjam_list = [
            "Budi Santoso", "Siti Rahayu", "Ahmad Fauzi", "Dewi Lestari",
            "Rizky Pratama", "Nurul Hidayah", "Andi Wijaya", "Rina Kusuma",
            "Fajar Nugroho", "Mega Putri", "Hendra Gunawan", "Yuni Astuti",
            "Doni Setiawan", "Lina Marlina", "Bagas Eko", "Fitri Handayani",
            "Gilang Ramadan", "Nisa Aulia", "Taufik Hidayat", "Reza Mahendra",
        ]
        prodi_list = [
            "Teknik Informatika", "Sistem Informasi", "Manajemen",
            "Akuntansi", "Teknik Elektro", "Desain Komunikasi Visual",
            "Psikologi", "Hukum",
        ]
        sesi_list = ["07:00-09:00", "09:00-11:00", "11:00-13:00",
                     "13:00-15:00", "15:00-17:00", "17:00-19:00"]
        keperluan_list = [
            "Kuliah Reguler", "Ujian Tengah Semester", "Ujian Akhir Semester",
            "Seminar Tugas Akhir", "Rapat Organisasi", "Workshop", "Praktikum",
        ]
        status_list = ["Disetujui", "Disetujui", "Disetujui", "Pending", "Ditolak"]

        # Get room IDs
        cur.execute("SELECT id FROM rooms")
        room_ids = [r[0] for r in cur.fetchall()]

        start_date = date(2024, 1, 1)
        bookings = []
        random.seed(42)
        for i in range(80):
            rand_date = start_date + timedelta(days=random.randint(0, 364))
            bookings.append((
                random.choice(room_ids),
                random.choice(peminjam_list),
                random.choice(prodi_list),
                rand_date.strftime("%Y-%m-%d"),
                random.choice(sesi_list),
                random.choice(keperluan_list),
                random.choice(status_list),
            ))

        cur.executemany(
            """INSERT INTO bookings
               (room_id, peminjam, prodi, tanggal, sesi, keperluan, status)
               VALUES (?,?,?,?,?,?,?)""",
            bookings,
        )
        conn.commit()

    conn.close()
    print(f"[DB] Database siap di: {DB_PATH}")


if __name__ == "__main__":
    init_db()
