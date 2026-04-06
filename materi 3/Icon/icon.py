import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QTextEdit, QStyle
)
from PySide6.QtGui import QAction, QKeySequence, QIcon

class IconDemo(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Icon Action Demo")
        self.setGeometry(100, 100, 700, 500)
        
        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)
        
        self.create_actions()
        self.create_menus()
        self.create_toolbars()
        
        self.statusBar().showMessage("Ready")
    
    def create_actions(self):
        # Mendapatkan style untuk standard icons
        style = self.style()
        
        # === MENGGUNAKAN STANDARD ICONS ===
        
        # New Action dengan standard icon
        self.new_action = QAction("&New", self)
        self.new_action.setIcon(style.standardIcon(QStyle.SP_FileIcon))
        self.new_action.setShortcut(QKeySequence.New)
        self.new_action.setStatusTip("Create new document")
        self.new_action.triggered.connect(self.new_file)
        
        # Open Action
        self.open_action = QAction("&Open", self)
        self.open_action.setIcon(style.standardIcon(QStyle.SP_DialogOpenButton))
        self.open_action.setShortcut(QKeySequence.Open)
        self.open_action.setStatusTip("Open existing document")
        self.open_action.triggered.connect(self.open_file)
        
        # Save Action
        self.save_action = QAction("&Save", self)
        self.save_action.setIcon(style.standardIcon(QStyle.SP_DialogSaveButton))
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.setStatusTip("Save document")
        self.save_action.triggered.connect(self.save_file)
        
        # Delete Action
        self.delete_action = QAction("&Delete", self)
        self.delete_action.setIcon(style.standardIcon(QStyle.SP_TrashIcon))
        self.delete_action.setShortcut(QKeySequence.Delete)
        self.delete_action.setStatusTip("Delete content")
        self.delete_action.triggered.connect(self.delete_content)
        
        # Info Action
        self.info_action = QAction("&About", self)
        self.info_action.setIcon(style.standardIcon(QStyle.SP_MessageBoxInformation))
        self.info_action.setStatusTip("About this application")
        self.info_action.triggered.connect(self.show_about)
        
        # === MENGGUNAKAN FILE ICON ===
        # Uncomment jika punya file icon
        # self.custom_action = QAction("Custom", self)
        # self.custom_action.setIcon(QIcon("icons/custom.png"))
        
        # === MENGGUNAKAN ICON DARI THEME (Linux) ===
        # self.edit_action = QAction("Edit", self)
        # self.edit_action.setIcon(QIcon.fromTheme("document-edit"))
    
    def create_menus(self):
        menu_bar = self.menuBar()
        
        # File Menu
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.delete_action)
        
        # Help Menu
        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction(self.info_action)
    
    def create_toolbars(self):
        # Main Toolbar
        toolbar = self.addToolBar("Main")
        toolbar.addAction(self.new_action)
        toolbar.addAction(self.open_action)
        toolbar.addAction(self.save_action)
        toolbar.addSeparator()
        toolbar.addAction(self.delete_action)
        toolbar.addSeparator()
        toolbar.addAction(self.info_action)
    
    # Slot methods
    def new_file(self):
        self.text_edit.clear()
        self.statusBar().showMessage("New file created", 3000)
    
    def open_file(self):
        self.statusBar().showMessage("Open file...", 3000)
    
    def save_file(self):
        self.statusBar().showMessage("File saved", 3000)
    
    def delete_content(self):
        self.text_edit.clear()
        self.statusBar().showMessage("Content deleted", 3000)
    
    def show_about(self):
        self.statusBar().showMessage("About dialog", 3000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IconDemo()
    window.show()
    sys.exit(app.exec())