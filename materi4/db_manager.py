import sqlite3

class DatabaseManager:
    """Class untuk mengelola semua operasi database"""
    
    def __init__(self, db_name='data_mhs.db'):
        self.db_name = db_name
        self.create_table()
    
    def get_connection(self):
        """Buat koneksi baru ke database"""
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row  # Agar hasil bisa diakses pakai nama kolom
        return conn
    
    def create_table(self):
        """Buat tabel mahasiswa jika belum ada"""
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS mahasiswa (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nim TEXT NOT NULL UNIQUE,
                    nama TEXT NOT NULL
                )
            ''')
    
    def tambah(self, nim, nama):
        """Tambah mahasiswa baru"""
        with self.get_connection() as conn:
            conn.execute(
                'INSERT INTO mahasiswa (nim, nama) VALUES (?, ?)',
                (nim, nama)
            )
    
    def ambil_semua(self):
        """Ambil semua data mahasiswa"""
        with self.get_connection() as conn:
            return conn.execute('SELECT * FROM mahasiswa ORDER BY nama').fetchall()
    
    def ambil_by_id(self, id):
        """Ambil satu mahasiswa berdasarkan ID"""
        with self.get_connection() as conn:
            return conn.execute('SELECT * FROM mahasiswa WHERE id = ?', (id,)).fetchone()
    
    def cari(self, keyword):
        """Cari mahasiswa berdasarkan nama atau NIM"""
        with self.get_connection() as conn:
            return conn.execute(
                'SELECT * FROM mahasiswa WHERE nama LIKE ? OR nim LIKE ?',
                (f'%{keyword}%', f'%{keyword}%')
            ).fetchall()
    
    def update(self, id, nim, nama):
        """Update data mahasiswa"""
        with self.get_connection() as conn:
            conn.execute(
                'UPDATE mahasiswa SET nim = ?, nama = ? WHERE id = ?',
                (nim, nama, id)
            )
    
    def hapus(self, id):
        """Hapus mahasiswa berdasarkan ID"""
        with self.get_connection() as conn:
            conn.execute('DELETE FROM mahasiswa WHERE id = ?', (id,))