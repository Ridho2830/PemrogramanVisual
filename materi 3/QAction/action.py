import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit
from PySide6.QtGui import QAction, QKeySequence

class TextEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("QAction Demo")
        self.setGeometry(100, 100, 700, 500)

        self.text_edit = QTextEdit()
        self.setCentralWidget(self.text_edit)

        self.create_actions()
        self.create_menus()
        self.create_toolbars()
        self.statusBar().showMessage("Ready")

    def create_actions(self):
        # New Action
        self.new_action = QAction("&New", self)
        self.new_action.setShortcut(QKeySequence.New)
        self.new_action.setStatusTip("Buat dokumen baru")
        self.new_action.triggered.connect(self.new_document)

        # Save Action
        self.save_action = QAction("&Save", self)
        self.save_action.setShortcut(QKeySequence.Save)
        self.save_action.setStatusTip("Simpan dokumen")
        self.save_action.triggered.connect(self.save_document)

        # Exit Action
        self.exit_action = QAction("E&xit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.setStatusTip("Keluar dari aplikasi")
        self.exit_action.triggered.connect(self.close)

        # Word Wrap — contoh checkable action (bisa di-toggle on/off)
        self.wordwrap_action = QAction("&Word Wrap", self)
        self.wordwrap_action.setCheckable(True)
        self.wordwrap_action.setChecked(True)
        self.wordwrap_action.setStatusTip("Toggle word wrap")
        self.wordwrap_action.triggered.connect(self.toggle_word_wrap)
        
        # Menubar Profile
        self.profile_action = QAction("&Tentang", self)
        self.profile_action.setStatusTip("Tentang pembuat aplikasi")
        self.profile_action.triggered.connect(self.show_about)
        

    def create_menus(self):
        # File Menu — action yang sama dipasang di sini...
        file_menu = self.menuBar().addMenu("&File")
        file_menu.addAction(self.new_action)
        file_menu.addAction(self.save_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        # View Menu — contoh checkable action di menu
        view_menu = self.menuBar().addMenu("&View")
        view_menu.addAction(self.wordwrap_action)
        
        # Profile Menu
        profile_menu = self.menuBar().addMenu("&Profile")
        profile_menu.addAction(self.profile_action)


    def create_toolbars(self):
        # ...dan action yang SAMA juga dipasang di toolbar — tidak perlu definisi ulang
        toolbar = self.addToolBar("File")
        toolbar.addAction(self.new_action)
        toolbar.addAction(self.save_action)
        
        
    # === SLOT METHODS ===

    def new_document(self):
        self.text_edit.clear()
        self.statusBar().showMessage("Dokumen baru dibuat", 3000)

    def save_document(self):
        self.statusBar().showMessage("Dokumen disimpan", 3000)

    def toggle_word_wrap(self, checked):
        if checked:
            self.text_edit.setLineWrapMode(QTextEdit.WidgetWidth)
            self.statusBar().showMessage("Word wrap ON", 2000)
        else:
            self.text_edit.setLineWrapMode(QTextEdit.NoWrap)
            self.statusBar().showMessage("Word wrap OFF", 2000)
    
    def show_about(self):
        self.statusBar().showMessage("QAction Demo v1.0 - Created by Ridho", 5000)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextEditor()
    window.show()
    sys.exit(app.exec())