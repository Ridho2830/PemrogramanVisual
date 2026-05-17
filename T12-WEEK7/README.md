# 📅 Dashboard Booking Ruangan Kelas Kampus

Dashboard manajemen peminjaman ruangan kelas berbasis **PySide6**, dengan visualisasi data menggunakan **Matplotlib** dan penyimpanan data menggunakan **SQLite**.

---

## 🗂️ Struktur Project

```
dashboard_booking/
├── main.py                  # Entry point aplikasi
├── README.md
├── requirements.txt
├── data/
│   ├── __init__.py
│   ├── seed_db.py           # Inisialisasi & seeding database SQLite
│   ├── data_loader.py       # Modul CRUD + agregasi data (Pandas + SQLite)
│   └── bookings.db          # File database SQLite (auto-dibuat saat pertama run)
└── ui/
    ├── __init__.py
    ├── main_window.py       # Window utama dashboard
    ├── chart_widget.py      # Widget Matplotlib embed di PySide6
    └── crud_dialog.py       # Dialog tambah booking (CRUD)
```

---

## 🗃️ Struktur Database SQLite

### Tabel `rooms` — Data Ruangan

| Kolom       | Tipe    | Keterangan                         |
|-------------|---------|-------------------------------------|
| `id`        | INTEGER | Primary Key, autoincrement          |
| `kode_ruang`| TEXT    | Kode unik ruangan (misal: A101)    |
| `gedung`    | TEXT    | Nama gedung                         |
| `kapasitas` | INTEGER | Kapasitas maksimum (orang)          |
| `fasilitas` | TEXT    | Daftar fasilitas yang tersedia      |

**Contoh Data:**
| kode_ruang | gedung      | kapasitas | fasilitas                     |
|------------|-------------|-----------|-------------------------------|
| A101       | Gedung A    | 40        | Proyektor, AC, Whiteboard     |
| LAB01      | Lab Terpadu | 25        | Komputer, AC, Proyektor       |
| AULA       | Aula Utama  | 200       | Sound System, AC, Proyektor   |

---

### Tabel `bookings` — Data Peminjaman

| Kolom      | Tipe    | Keterangan                                      |
|------------|---------|--------------------------------------------------|
| `id`       | INTEGER | Primary Key, autoincrement                       |
| `room_id`  | INTEGER | Foreign Key → `rooms.id`                        |
| `peminjam` | TEXT    | Nama peminjam                                    |
| `prodi`    | TEXT    | Program studi peminjam                           |
| `tanggal`  | TEXT    | Tanggal peminjaman (format: YYYY-MM-DD)         |
| `sesi`     | TEXT    | Sesi waktu (misal: 07:00-09:00)                 |
| `keperluan`| TEXT    | Tujuan peminjaman                                |
| `status`   | TEXT    | Status: `Disetujui`, `Pending`, atau `Ditolak`  |

**Relasi:** `bookings.room_id` → `rooms.id` (FOREIGN KEY)

---

## 📊 Fitur Dashboard

### 1. Tampilan Data Mentah (QTableWidget)
- Menampilkan seluruh data booking dalam tabel interaktif
- Filter berdasarkan status: Semua / Disetujui / Pending / Ditolak
- Baris bergantian warna untuk kemudahan membaca
- Status booking diberi warna berbeda (hijau/oranye/merah)

### 2. Visualisasi Chart (Matplotlib embed PySide6)
Chart tampil **langsung di aplikasi**, bukan window terpisah:

| Jenis Chart           | Deskripsi                                      |
|-----------------------|------------------------------------------------|
| Pie – Status          | Distribusi booking berdasarkan status approval |
| Bar – Program Studi   | Jumlah booking per program studi (horizontal)  |
| Bar – Ruangan         | Frekuensi pemakaian tiap ruangan               |
| Line – Tren Bulanan   | Tren jumlah booking sepanjang tahun            |
| Bar – Sesi Waktu      | Distribusi booking per sesi jam                |

### 3. Filter Interaktif
- Filter tabel berdasarkan status booking
- Filter chart berdasarkan status (untuk Pie chart)
- Pemilihan jenis chart secara dinamis

### 4. Fitur CRUD (Bonus)
- **Create**: Tambah booking baru via dialog form
- **Read**: Tampilkan semua data di tabel dan chart
- **Update**: Ubah status booking (via `data_loader.update_booking_status()`)
- **Delete**: Hapus booking dengan konfirmasi dialog

### 5. Ringkasan Statistik (Stat Cards)
- Total Booking
- Jumlah Disetujui
- Jumlah Pending
- Jumlah Ditolak
- Total Ruangan

### 6. Export Chart ke PNG
- Simpan chart aktif sebagai file `.png` via dialog file browser

---

## 🚀 Cara Menjalankan

### 1. Install dependencies
```bash
pip install PySide6 matplotlib pandas
```

### 2. Jalankan aplikasi
```bash
python main.py
```

Database `bookings.db` akan **otomatis dibuat dan diisi** dengan 80 data sampel saat pertama kali dijalankan.

---

## 🛠️ Teknologi yang Digunakan

| Library     | Versi Minimal | Kegunaan                            |
|-------------|---------------|--------------------------------------|
| PySide6     | 6.4+          | GUI framework utama                  |
| Matplotlib  | 3.6+          | Visualisasi chart (embed di Qt)     |
| Pandas      | 1.5+          | Manipulasi & agregasi data           |
| SQLite3     | Built-in      | Database lokal penyimpanan data      |

---

## 👨‍💻 Catatan Pengembangan

- Chart di-render menggunakan `FigureCanvasQTAgg` dari `matplotlib.backends.backend_qtagg`
- Semua chart menggunakan tema gelap konsisten agar cocok dengan UI dashboard
- UI responsif terhadap resize window menggunakan `QSplitter` dan `QSizePolicy`
- Database di-seed otomatis dengan 80 baris data booking dan 10 ruangan

---

## 📸 Hasil Screenshot Aplikasi

Berikut adalah beberapa tangkapan layar dari aplikasi Dashboard Booking Ruangan:

### 1. Tampilan Utama Dashboard
![Tampilan Utama](ss/Screenshot%202026-05-17%20174032.png)

### 2. Tampilan Chart dan Visualisasi Data
![Tampilan Chart](ss/Screenshot%202026-05-17%20174040.png)

### 3. Tampilan Form / Interaksi Lainnya
![Tampilan Form](ss/Screenshot%202026-05-17%20174049.png)

### 4. Tampilan CRUD / Data Tabel
![Tampilan Data](ss/Screenshot%202026-05-17%20174058.png)
