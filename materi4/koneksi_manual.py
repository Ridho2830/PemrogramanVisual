import sqlite3

# Membuat koneksi (file akan dibuat otomatis jika belum ada)
conn = sqlite3.connect('data_mhs.db')

# Membuat cursor
cursor = conn.cursor()

# Membuat tabel sederhana: id, nim, nama
cursor.execute('''
    CREATE TABLE IF NOT EXISTS mahasiswa (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nim TEXT NOT NULL UNIQUE,
        nama TEXT NOT NULL
    )
''')

# Simpan perubahan
conn.commit()

# Tutup koneksi
conn.close()

print("Database dan tabel berhasil dibuat!")