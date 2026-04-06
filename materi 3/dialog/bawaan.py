import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QLabel, QMessageBox, QFileDialog, QInputDialog
)

class DialogDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Built-in Dialogs Demo")
        self.setGeometry(100, 100, 400, 500)
        
        self.setup_ui()
    
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Result label
        self.result_label = QLabel("Hasil akan ditampilkan di sini...")
        self.result_label.setWordWrap(True)
        self.result_label.setStyleSheet("""
            QLabel {
                background-color: #f0f0f0;
                padding: 15px;
                border-radius: 5px;
                min-height: 60px;
            }
        """)
        layout.addWidget(self.result_label)
        
        # === QMESSAGEBOX BUTTONS ===
        layout.addWidget(QLabel("<b>QMessageBox:</b>"))
        
        btn_info = QPushButton("Information Dialog")
        btn_info.clicked.connect(self.show_info)
        layout.addWidget(btn_info)
        
        btn_warning = QPushButton("Warning Dialog")
        btn_warning.clicked.connect(self.show_warning)
        layout.addWidget(btn_warning)
        
        btn_critical = QPushButton("Critical Dialog")
        btn_critical.clicked.connect(self.show_critical)
        layout.addWidget(btn_critical)
        
        btn_question = QPushButton("Question Dialog")
        btn_question.clicked.connect(self.show_question)
        layout.addWidget(btn_question)
        
        # === QFILEDIALOG BUTTONS ===
        layout.addWidget(QLabel("<b>QFileDialog:</b>"))
        
        btn_open = QPushButton("Open File Dialog")
        btn_open.clicked.connect(self.open_file_dialog)
        layout.addWidget(btn_open)
        
        btn_save = QPushButton("Save File Dialog")
        btn_save.clicked.connect(self.save_file_dialog)
        layout.addWidget(btn_save)
        
        btn_folder = QPushButton("Select Folder Dialog")
        btn_folder.clicked.connect(self.select_folder_dialog)
        layout.addWidget(btn_folder)
        
        # === QINPUTDIALOG BUTTONS ===
        layout.addWidget(QLabel("<b>QInputDialog:</b>"))
        
        btn_text = QPushButton("Input Text Dialog")
        btn_text.clicked.connect(self.input_text_dialog)
        layout.addWidget(btn_text)
        
        btn_int = QPushButton("Input Integer Dialog")
        btn_int.clicked.connect(self.input_int_dialog)
        layout.addWidget(btn_int)
        
        btn_item = QPushButton("Select Item Dialog")
        btn_item.clicked.connect(self.select_item_dialog)
        layout.addWidget(btn_item)
        
        layout.addStretch()
    
    # === QMESSAGEBOX METHODS ===
    
    def show_info(self):
        QMessageBox.information(
            self,
            "Informasi",
            "Ini adalah pesan informasi.\nOperasi berhasil dilakukan!"
        )
        self.result_label.setText("Information dialog ditampilkan")
    
    def show_warning(self):
        QMessageBox.warning(
            self,
            "Peringatan",
            "Ini adalah pesan peringatan!\nHarap perhatikan."
        )
        self.result_label.setText("Warning dialog ditampilkan")
    
    def show_critical(self):
        QMessageBox.critical(
            self,
            "Error",
            "Terjadi kesalahan kritis!\nAplikasi tidak dapat melanjutkan."
        )
        self.result_label.setText("Critical dialog ditampilkan")
    
    def show_question(self):
        reply = QMessageBox.question(
            self,
            "Konfirmasi",
            "Apakah Anda yakin ingin melanjutkan?",
            QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
            QMessageBox.No  # Default button
        )
        
        if reply == QMessageBox.Yes:
            self.result_label.setText("Anda memilih: YES")
        elif reply == QMessageBox.No:
            self.result_label.setText("Anda memilih: NO")
        else:
            self.result_label.setText("Anda memilih: CANCEL")
    
    # === QFILEDIALOG METHODS ===
    
    def open_file_dialog(self):
        file_path, selected_filter = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "",  # Start directory
            "Text Files (*.txt);;Python Files (*.py);;All Files (*)"
        )
        
        if file_path:
            self.result_label.setText(f"File dipilih:\n{file_path}")
        else:
            self.result_label.setText("Tidak ada file yang dipilih")
    
    def save_file_dialog(self):
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "untitled.txt",  # Default filename
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            self.result_label.setText(f"Save ke:\n{file_path}")
        else:
            self.result_label.setText("Save dibatalkan")
    
    def select_folder_dialog(self):
        folder_path = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
            ""
        )
        
        if folder_path:
            self.result_label.setText(f"Folder dipilih:\n{folder_path}")
        else:
            self.result_label.setText("Tidak ada folder yang dipilih")
    
    # === QINPUTDIALOG METHODS ===
    
    def input_text_dialog(self):
        text, ok = QInputDialog.getText(
            self,
            "Input Teks",
            "Masukkan nama Anda:"
        )
        
        if ok and text:
            self.result_label.setText(f"Nama: {text}")
        else:
            self.result_label.setText("Input dibatalkan")
    
    def input_int_dialog(self):
        value, ok = QInputDialog.getInt(
            self,
            "Input Angka",
            "Masukkan umur Anda:",
            value=25,      # Default value
            min=1,         # Minimum
            max=120,       # Maximum
            step=1         # Step
        )
        
        if ok:
            self.result_label.setText(f"Umur: {value} tahun")
        else:
            self.result_label.setText("Input dibatalkan")
    
    def select_item_dialog(self):
        items = ["Python", "Java", "C++", "JavaScript", "Go"]
        
        item, ok = QInputDialog.getItem(
            self,
            "Pilih Item",
            "Bahasa pemrograman favorit:",
            items,
            current=0,       # Default index
            editable=False   # Tidak bisa diedit
        )
        
        if ok and item:
            self.result_label.setText(f"Bahasa favorit: {item}")
        else:
            self.result_label.setText("Pilihan dibatalkan")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DialogDemo()
    window.show()
    sys.exit(app.exec())