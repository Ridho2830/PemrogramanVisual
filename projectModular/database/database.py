import sqlite3


class DatabaseManager:
    """Mengelola semua operasi database (SQL).
    File ini TIDAK boleh import PySide6."""
    
    def __init__(self, db_name='data_mhs.db', lokasi='projectModular/database/'):
        self.db_name = lokasi + db_name
        self.create_table()
    
    def get_connection(self):
        conn = sqlite3.connect(self.db_name)
        conn.row_factory = sqlite3.Row
        return conn
    
    def create_table(self):
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS mahasiswa (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nim TEXT NOT NULL UNIQUE,
                    nama TEXT NOT NULL
                )
            ''')
    
    def tambah(self, nim, nama):
        with self.get_connection() as conn:
            conn.execute(
                'INSERT INTO mahasiswa (nim, nama) VALUES (?, ?)',
                (nim, nama)
            )
    
    def ambil_semua(self):
        with self.get_connection() as conn:
            return conn.execute(
                'SELECT * FROM mahasiswa ORDER BY nama'
            ).fetchall()
    
    def cari(self, keyword):
        with self.get_connection() as conn:
            return conn.execute(
                'SELECT * FROM mahasiswa WHERE nama LIKE ? OR nim LIKE ?',
                (f'%{keyword}%', f'%{keyword}%')
            ).fetchall()
    
    def update(self, id, nim, nama):
        with self.get_connection() as conn:
            conn.execute(
                'UPDATE mahasiswa SET nim=?, nama=? WHERE id=?',
                (nim, nama, id)
            )
    
    def hapus(self, id):
        with self.get_connection() as conn:
            conn.execute(
                'DELETE FROM mahasiswa WHERE id = ?', (id,)
            )