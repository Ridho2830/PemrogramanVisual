import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QDialog, QDialogButtonBox, QPushButton, QLabel,
    QLineEdit, QComboBox, QSpinBox, QFormLayout, QTextEdit
)
from PySide6.QtCore import Qt


# ============================================
# CUSTOM DIALOG: Form Input Mahasiswa
# ============================================

class StudentDialog(QDialog):
    """Custom dialog untuk input data mahasiswa"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Input Data Mahasiswa")
        self.setMinimumWidth(350)
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Form layout untuk input
        form_layout = QFormLayout()
        
        # NIM
        self.nim_input = QLineEdit()
        self.nim_input.setPlaceholderText("Contoh: 12345678")
        form_layout.addRow("NIM:", self.nim_input)
        
        # Nama
        self.nama_input = QLineEdit()
        self.nama_input.setPlaceholderText("Nama lengkap")
        form_layout.addRow("Nama:", self.nama_input)
        
        # Jurusan
        self.jurusan_combo = QComboBox()
        self.jurusan_combo.addItems([
            "Teknik Informatika",
            "Sistem Informasi",
            "Teknik Komputer",
            "Manajemen Informatika"
        ])
        form_layout.addRow("Jurusan:", self.jurusan_combo)
        
        # Semester
        self.semester_spin = QSpinBox()
        self.semester_spin.setRange(1, 14)
        self.semester_spin.setValue(1)
        form_layout.addRow("Semester:", self.semester_spin)
        
        layout.addLayout(form_layout)
        
        # Standard button box (OK dan Cancel)
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self.validate_and_accept)
        button_box.rejected.connect(self.reject)
        
        layout.addWidget(button_box)
    
    def validate_and_accept(self):
        """Validasi input sebelum accept"""
        if not self.nim_input.text().strip():
            self.nim_input.setFocus()
            self.nim_input.setStyleSheet("border: 2px solid red;")
            return
        
        if not self.nama_input.text().strip():
            self.nama_input.setFocus()
            self.nama_input.setStyleSheet("border: 2px solid red;")
            return
        
        self.accept()
    
    def get_data(self):
        """Mengembalikan data yang diinput"""
        return {
            'nim': self.nim_input.text().strip(),
            'nama': self.nama_input.text().strip(),
            'jurusan': self.jurusan_combo.currentText(),
            'semester': self.semester_spin.value()
        }


# ============================================
# CUSTOM DIALOG: Settings
# ============================================

class SettingsDialog(QDialog):
    """Custom dialog untuk pengaturan aplikasi"""
    
    def __init__(self, current_settings=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pengaturan")
        self.setMinimumWidth(300)
        self.current_settings = current_settings or {}
        self.setup_ui()
        self.load_settings()
    
    def setup_ui(self):
        layout = QVBoxLayout(self)
        form = QFormLayout()
        
        # Theme
        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark", "System"])
        form.addRow("Theme:", self.theme_combo)
        
        # Font Size
        self.fontsize_spin = QSpinBox()
        self.fontsize_spin.setRange(8, 24)
        self.fontsize_spin.setValue(12)
        form.addRow("Font Size:", self.fontsize_spin)
        
        # Auto Save
        self.autosave_combo = QComboBox()
        self.autosave_combo.addItems(["Off", "1 menit", "5 menit", "10 menit"])
        form.addRow("Auto Save:", self.autosave_combo)
        
        layout.addLayout(form)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        reset_btn = QPushButton("Reset Default")
        reset_btn.clicked.connect(self.reset_defaults)
        button_layout.addWidget(reset_btn)
        
        button_layout.addStretch()
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Save")
        save_btn.setDefault(True)
        save_btn.clicked.connect(self.accept)
        button_layout.addWidget(save_btn)
        
        layout.addLayout(button_layout)
    
    def load_settings(self):
        """Load current settings ke form"""
        if 'theme' in self.current_settings:
            index = self.theme_combo.findText(self.current_settings['theme'])
            if index >= 0:
                self.theme_combo.setCurrentIndex(index)
        
        if 'font_size' in self.current_settings:
            self.fontsize_spin.setValue(self.current_settings['font_size'])
    
    def reset_defaults(self):
        """Reset ke nilai default"""
        self.theme_combo.setCurrentIndex(0)
        self.fontsize_spin.setValue(12)
        self.autosave_combo.setCurrentIndex(0)
    
    def get_settings(self):
        """Mengembalikan settings yang dipilih"""
        return {
            'theme': self.theme_combo.currentText(),
            'font_size': self.fontsize_spin.value(),
            'autosave': self.autosave_combo.currentText()
        }


# ============================================
# MAIN WINDOW
# ============================================

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Custom Dialog Demo")
        self.setGeometry(100, 100, 500, 400)
        
        self.settings = {}
        self.students = []
        
        self.setup_ui()
    
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Buttons
        add_student_btn = QPushButton("Tambah Mahasiswa")
        add_student_btn.clicked.connect(self.show_student_dialog)
        layout.addWidget(add_student_btn)
        
        settings_btn = QPushButton("Pengaturan")
        settings_btn.clicked.connect(self.show_settings_dialog)
        layout.addWidget(settings_btn)
        
        # Display area
        self.display = QTextEdit()
        self.display.setReadOnly(True)
        layout.addWidget(self.display)
        
        self.statusBar().showMessage("Ready")
    
    def show_student_dialog(self):
        dialog = StudentDialog(self)
        
        if dialog.exec() == QDialog.Accepted:
            data = dialog.get_data()
            self.students.append(data)
            self.update_display()
            self.statusBar().showMessage(f"Mahasiswa {data['nama']} ditambahkan", 3000)
    
    def show_settings_dialog(self):
        dialog = SettingsDialog(self.settings, self)
        
        if dialog.exec() == QDialog.Accepted:
            self.settings = dialog.get_settings()
            self.statusBar().showMessage("Pengaturan disimpan", 3000)
            self.update_display()
    
    def update_display(self):
        text = "=== DATA MAHASISWA ===\n\n"
        
        for i, student in enumerate(self.students, 1):
            text += f"{i}. {student['nama']} ({student['nim']})\n"
            text += f"   Jurusan: {student['jurusan']}\n"
            text += f"   Semester: {student['semester']}\n\n"
        
        if self.settings:
            text += "\n=== PENGATURAN ===\n\n"
            for key, value in self.settings.items():
                text += f"{key}: {value}\n"
        
        self.display.setText(text)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())