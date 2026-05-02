import sqlite3

# Cek versi sqlite3 (selalu tersedia di Python)
print(f"sqlite3 version (binding): {getattr(sqlite3, 'version', 'n/a')}")
print(f"SQLite version (library)  : {sqlite3.sqlite_version}")

# Cek PySide6
try:
    import PySide6
    print(f"PySide6 version: {PySide6.__version__}")
except ModuleNotFoundError:
    print("PySide6: belum terpasang (pip install PySide6)")

print("Selesai.")