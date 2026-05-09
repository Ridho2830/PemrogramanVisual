# Tugas Pemrograman Visual - Week 6

Aplikasi Desktop CRUD (Create, Read, Update, Delete) untuk manajemen post menggunakan **PySide6** dan REST API.

## Deskripsi Tugas
Aplikasi ini dibuat untuk memenuhi tugas Pemrograman Visual Minggu ke-6. Aplikasi ini berfungsi untuk mengelola data "Post" melalui API eksternal. Fitur-fitur yang tersedia antara lain:
- **Refresh**: Mengambil ulang daftar post dari API.
- **Add Post**: Menambahkan post baru.
- **Edit Post**: Mengubah data post yang sudah ada.
- **Delete Post**: Menghapus post.
- **View Detail**: Menampilkan detail post beserta komentar yang terkait jika ada.

Aplikasi ini menggunakan `QThread` untuk operasi jaringan agar UI tetap responsif (tidak freeze) saat mengambil data dari API.

## Hasil Screenshot

Berikut adalah beberapa tampilan dari aplikasi:

### 1. Tampilan Utama (Daftar Post)
![Tampilan Utama](ss/Screenshot%202026-05-09%20210815.png)

### 2. Tampilan Detail Post
![Detail Post](ss/Screenshot%202026-05-09%20210802.png)

### 3. Form Tambah/Edit Post
![Form Post](ss/Screenshot%202026-05-09%20210751.png)

### 4. Notifikasi / Dialog
![Notifikasi](ss/Screenshot%202026-05-09%20210808.png)

*(Catatan: Screenshot lainnya dapat dilihat di folder `ss/`)*
