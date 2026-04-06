import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTextEdit, QLabel, QDockWidget, QListWidget
)
from PySide6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Struktur QMainWindow")
        self.setGeometry(100, 100, 800, 600)
        
        self.setup_central_widget()
        self.setup_menu_bar()
        self.setup_toolbars()
        self.setup_status_bar()
        self.setup_dock_widgets()
    
    def setup_central_widget(self):
        """Membuat central widget - area konten utama"""
        self.text_edit = QTextEdit()
        self.text_edit.setPlaceholderText("Ketik teks di sini...")
        self.setCentralWidget(self.text_edit)
    
    def setup_menu_bar(self):
        """Membuat menu bar"""
        menu_bar = self.menuBar()
        
        # Menu File
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction("New")
        file_menu.addAction("Open")
        file_menu.addAction("Save")
        file_menu.addSeparator()
        file_menu.addAction("Exit")
        
        # Menu Edit
        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction("Undo")
        edit_menu.addAction("Redo")
        edit_menu.addSeparator()
        edit_menu.addAction("Cut")
        edit_menu.addAction("Copy")
        edit_menu.addAction("Paste")
        
        # Menu View
        view_menu = menu_bar.addMenu("&View")
        view_menu.addAction("Zoom In")
        view_menu.addAction("Zoom Out")
        
        # Menu Help
        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction("About")
    
    def setup_toolbars(self):
        """Membuat toolbar"""
        # Toolbar File
        file_toolbar = self.addToolBar("File")
        file_toolbar.addAction("New")
        file_toolbar.addAction("Open")
        file_toolbar.addAction("Save")
        
        # Toolbar Edit
        edit_toolbar = self.addToolBar("Edit")
        edit_toolbar.addAction("Cut")
        edit_toolbar.addAction("Copy")
        edit_toolbar.addAction("Paste")
    
    def setup_status_bar(self):
        """Membuat status bar"""
        self.statusBar().showMessage("Ready")
        
        # Menambahkan widget permanen ke status bar
        self.status_label = QLabel("Ln 1, Col 1")
        self.statusBar().addPermanentWidget(self.status_label)
    
    def setup_dock_widgets(self):
        """Membuat dock widgets"""
        # Dock kiri - File Explorer
        file_dock = QDockWidget("File Explorer", self)
        file_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        file_list = QListWidget()
        file_list.addItems(["document.txt", "image.png", "data.csv"])
        file_dock.setWidget(file_list)
        
        self.addDockWidget(Qt.LeftDockWidgetArea, file_dock)
        
        # Dock kanan - Properties
        prop_dock = QDockWidget("Properties", self)
        prop_dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        
        prop_widget = QWidget()
        prop_layout = QVBoxLayout(prop_widget)
        prop_layout.addWidget(QLabel("File: document.txt"))
        prop_layout.addWidget(QLabel("Size: 1.2 KB"))
        prop_layout.addWidget(QLabel("Modified: 2024-01-15"))
        prop_layout.addStretch()
        prop_dock.setWidget(prop_widget)
        6
        self.addDockWidget(Qt.RightDockWidgetArea, prop_dock)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())