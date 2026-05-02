import sqlite3


class DatabaseManager:
    """Mengelola semua operasi database (SQL).
    File ini TIDAK boleh import PySide6."""
    
    def __init__(self, db_name='data_film.db'):
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_name = os.path.join(base_dir, db_name)
        self.create_table()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def create_table(self):
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS film (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    judul_film TEXT NOT NULL UNIQUE,
                    sutradara TEXT NOT NULL,
                    tahun_rilis INTEGER NOT NULL,
                    durasi INTEGER NOT NULL,
                    rating INTEGER NOT NULL,
                    genre TEXT NOT NULL
                )
            ''')
    
    def tambah(self, judul_film, sutradara, tahun_rilis, durasi, rating, genre):
        with self.get_connection() as conn:
            conn.execute(
                'INSERT INTO film (judul_film, sutradara, tahun_rilis, durasi, rating, genre) VALUES (?, ?, ?, ?, ?, ?)',
                (judul_film, sutradara, tahun_rilis, durasi, rating, genre)
            )
    
    def ambil_semua(self):
        with self.get_connection() as conn:
            return conn.execute(
                'SELECT * FROM film ORDER BY judul_film'
            ).fetchall()
    
    def cari(self, keyword):
        with self.get_connection() as conn:
            return conn.execute(
                'SELECT * FROM film WHERE judul_film LIKE ? OR sutradara LIKE ?',
                (f'%{keyword}%', f'%{keyword}%')
            ).fetchall()
    
    def update(self, id, judul_film, sutradara, tahun_rilis, durasi, rating, genre):
        with self.get_connection() as conn:
            conn.execute(
                'UPDATE film SET judul_film=?, sutradara=?, tahun_rilis=?, durasi=?, rating=?, genre=? WHERE id=?',
                (judul_film, sutradara, tahun_rilis, durasi, rating, genre, id)
            )
    
    def hapus(self, id):
        with self.get_connection() as conn:
            conn.execute(
                'DELETE FROM film WHERE id = ?', (id,)
            )