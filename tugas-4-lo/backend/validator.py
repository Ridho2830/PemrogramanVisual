class Validator:
    """Validasi input data mahasiswa.
    File ini TIDAK boleh import PySide6 atau sqlite3."""
    
    @staticmethod
    def validasi_judul_film(judul_film):
        """Return (True/False, pesan_error)"""
        if not judul_film:
            return False, "Judul film tidak boleh kosong"
        if len(judul_film) < 3:
            return False, "Judul film minimal 3 karakter"
        return True, ""
    
    @staticmethod
    def validasi_sutradara(sutradara):
        """Return (True/False, pesan_error)"""
        if not sutradara:
            return False, "Sutradara tidak boleh kosong"
        if len(sutradara) < 3:
            return False, "Sutradara minimal 3 karakter"
        return True, ""
    
    @staticmethod
    def validasi_tahun(tahun_rilis):
        """Return (True/False, pesan_error)"""
        if not tahun_rilis:
            return False, "Tahun rilis tidak boleh kosong"
        if not isinstance(tahun_rilis, int):
            return False, "Tahun rilis harus berupa angka"
        if tahun_rilis < 1945 or tahun_rilis > 2023:
            return False, "Tahun rilis tidak valid"
        return True, ""
    
    @staticmethod
    def validasi_durasi(durasi):
        """Return (True/False, pesan_error)"""
        if not durasi:
            return False, "Durasi tidak boleh kosong"
        try:
            durasi_int = int(durasi)
            if durasi_int <= 0:
                return False, "Durasi harus berupa angka positif"
        except ValueError:
            return False, "Durasi harus berupa angka"
        return True, ""
    
    @staticmethod
    def validasi_rating(rating):
        """Return (True/False, pesan_error)"""
        if rating is None:
            return False, "Rating tidak boleh kosong"
        if not isinstance(rating, (int, float)):
            return False, "Rating harus berupa angka"
        if rating < 0 or rating > 10:
            return False, "Rating harus berupa angka antara 0 dan 10"
        return True, ""

    @staticmethod
    def validasi_genre(genre):
        """Return (True/False, pesan_error)"""
        if not genre:
            return False, "Genre tidak boleh kosong"
        return True, ""
    
    @staticmethod
    def validasi_semua(judul_film, sutradara, tahun_rilis, durasi, rating, genre):
        """Validasi semua field sekaligus.
        Return (True/False, list_pesan_error)"""
        errors = []
        
        v1, m1 = Validator.validasi_judul_film(judul_film)
        if not v1: errors.append(m1)
        
        v2, m2 = Validator.validasi_sutradara(sutradara)
        if not v2: errors.append(m2)
        
        v3, m3 = Validator.validasi_tahun(tahun_rilis)
        if not v3: errors.append(m3)
        
        v4, m4 = Validator.validasi_durasi(durasi)
        if not v4: errors.append(m4)
        
        v5, m5 = Validator.validasi_rating(rating)
        if not v5: errors.append(m5)
        
        v6, m6 = Validator.validasi_genre(genre)
        if not v6: errors.append(m6)
        
        return len(errors) == 0, errors