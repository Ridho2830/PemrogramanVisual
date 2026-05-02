class Validator:
    """Validasi input data mahasiswa.
    File ini TIDAK boleh import PySide6 atau sqlite3."""
    
    @staticmethod
    def validasi_nim(nim):
        """Return (True/False, pesan_error)"""
        if not nim:
            return False, "NIM tidak boleh kosong"
        if not nim.isdigit():
            return False, "NIM harus berupa angka"
        if len(nim) != 8:
            return False, "NIM harus 8 digit"
        return True, ""
    
    @staticmethod
    def validasi_nama(nama):
        """Return (True/False, pesan_error)"""
        if not nama:
            return False, "Nama tidak boleh kosong"
        if len(nama) < 3:
            return False, "Nama minimal 3 karakter"
        return True, ""
    
    @staticmethod
    def validasi_semua(nim, nama):
        """Validasi semua field sekaligus.
        Return (True/False, list_pesan_error)"""
        errors = []
        
        valid, msg = Validator.validasi_nim(nim)
        if not valid:
            errors.append(msg)
        
        valid, msg = Validator.validasi_nama(nama)
        if not valid:
            errors.append(msg)
        
        return len(errors) == 0, errors