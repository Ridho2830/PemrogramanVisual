import sys
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QListWidget)
from PySide6.QtCore import Qt

class TodoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Aplikasi To-Do List")
        self.resize(400, 300)
        
        main_layout = QVBoxLayout()
        
        # Judul
        judul = QLabel("TO-DO LIST")
        judul.setAlignment(Qt.AlignmentFlag.AlignCenter)
        judul.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px; background-color: #34495e; color: white; border-radius: 5px;")
        
        # input dan tombol tambah
        input_layout = QHBoxLayout()
        self.input_tugas = QLineEdit()
        self.input_tugas.setPlaceholderText("Masukkan tugas baru")
        self.input_tugas.setStyleSheet("""
            padding: 10px 20px;
            border: 2px solid #2980b9;
            border-radius: 5px;
        """)
        self.btn_tambah = QPushButton("Tambah")
        self.btn_tambah.setStyleSheet("""
            padding: 10px 20px;
            font-size: 16px;
            background-color: #2980b9;
            border: 2px solid blue;
            border-radius: 5px;
        """)
        self.btn_tambah.clicked.connect(self.tambah_tugas)
        
        input_layout.addWidget(self.input_tugas)
        
        input_layout.addWidget(self.btn_tambah)
        
        # List Widget
        self.list_tugas = QListWidget()
        self.list_tugas.setStyleSheet("""
            padding: 10px;
            border: 2px solid #2980b9;
            border-radius: 5px;
        """)
        
        # Tombol aksi
        btn_layout = QHBoxLayout()
        self.btn_hapus = QPushButton("Hapus")
        self.btn_hapus.setStyleSheet("""
            padding: 10px 20px;
            font-size: 16px;
            background-color: #e74c3c;
            border: 2px solid #c0392b;
            border-radius: 5px;
        """)
        self.btn_hapus.clicked.connect(self.hapus_tugas)
        
        self.btn_clear = QPushButton("Clear")
        self.btn_clear.setStyleSheet("""
            padding: 10px 20px;
            font-size: 16px;
            background-color: #f39c12;
            border: 2px solid #d35400;
            border-radius: 5px;
        """)
        self.btn_clear.clicked.connect(self.clear_tugas)
        
        btn_layout.addWidget(self.btn_hapus)
        btn_layout.addWidget(self.btn_clear)
        
        # Label Statistik
        self.label_statistik = QLabel("Total Tugas: 0")
        self.label_statistik.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_statistik.setStyleSheet("font-size: 14px; padding: 10px; color: #2c3e50;")
        
        # Assemble Layout
        main_layout.addWidget(judul)
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.list_tugas)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.label_statistik)
        main_layout.addStretch()
        self.setLayout(main_layout)
    
    def tambah_tugas(self):
        tugas = self.input_tugas.text().strip()
        if tugas:
            self.list_tugas.addItem(tugas)
            self.input_tugas.clear()
            self.update_statistik()
        else:
            QMessageBox.warning(self, "Peringatan", "Tugas tidak boleh kosong!")
            
    
    def hapus_tugas(self):
        selected_items = self.list_tugas.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Peringatan", "Pilih tugas yang ingin dihapus!")
            return
        for item in selected_items:
            self.list_tugas.takeItem(self.list_tugas.row(item))
        self.update_statistik()

    def clear_tugas(self):
        self.list_tugas.clear()
        self.update_statistik()

    def update_statistik(self):
        total_tugas = self.list_tugas.count()
        self.label_statistik.setText(f"Total Tugas: {total_tugas}")
        
app = QApplication(sys.argv)
window = TodoApp()
window.show()
sys.exit(app.exec())