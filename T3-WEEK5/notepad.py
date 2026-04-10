import sys
from PySide6.QtWidgets import *

# =========================
# FIND DIALOG
# =========================
class FindDialog(QDialog):
    def __init__(self, editor):
        super().__init__()
        self.editor = editor
        self.setWindowTitle("Find")
        self.setFixedWidth(300)

        layout = QVBoxLayout(self)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Cari teks...")

        btn = QPushButton("Find Next")
        btn.clicked.connect(self.find)

        layout.addWidget(self.input)
        layout.addWidget(btn)

    def find(self):
        text = self.editor.toPlainText()
        keyword = self.input.text()

        if keyword == "":
            return

        cursor = self.editor.textCursor()
        pos = cursor.position()

        idx = text.find(keyword, pos)
        if idx == -1:
            idx = text.find(keyword, 0)

        if idx != -1:
            cursor.setPosition(idx)
            cursor.setPosition(idx + len(keyword), cursor.KeepAnchor)
            self.editor.setTextCursor(cursor)


# =========================
# MAIN WINDOW
# =========================
class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()

        self.file = None

        # Editor
        self.editor = QTextEdit()
        self.setCentralWidget(self.editor)

        # Status
        self.status = self.statusBar()
        self.label = QLabel("Ready")
        self.status.addWidget(self.label)

        # Build UI
        self.menu()
        self.toolbar()

        # Event
        self.editor.cursorPositionChanged.connect(self.update_status)

        self.setWindowTitle("Simple Notepad")
        self.resize(800, 600)

    # =========================
    # MENU
    # =========================
    def menu(self):
        bar = self.menuBar()

        file_menu = bar.addMenu("File")
        file_menu.addAction("New", self.new)
        file_menu.addAction("Open", self.open)
        file_menu.addAction("Save", self.save)

        edit_menu = bar.addMenu("Edit")
        edit_menu.addAction("Find", self.show_find)
        edit_menu.addAction("Clear", self.editor.clear)

    # =========================
    # TOOLBAR
    # =========================
    def toolbar(self):
        tb = self.addToolBar("Tools")

        tb.addAction("New", self.new)
        tb.addAction("Open", self.open)
        tb.addAction("Save", self.save)
        tb.addSeparator()
        tb.addAction("Find", self.show_find)

    # =========================
    # FILE
    # =========================
    def new(self):
        self.editor.clear()
        self.file = None
        self.setWindowTitle("Untitled")

    def open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open File")

        if path:
            f = open(path, "r", encoding="utf-8")
            self.editor.setPlainText(f.read())
            f.close()

            self.file = path
            self.setWindowTitle(path)

    def save(self):
        if not self.file:
            path, _ = QFileDialog.getSaveFileName(self, "Save File")
            if not path:
                return
            self.file = path

        f = open(self.file, "w", encoding="utf-8")
        f.write(self.editor.toPlainText())
        f.close()

        self.status.showMessage("Saved!", 2000)

    # =========================
    # FIND
    # =========================
    def show_find(self):
        self.dialog = FindDialog(self.editor)
        self.dialog.show()

    # =========================
    # STATUS
    # =========================
    def update_status(self):
        cursor = self.editor.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1

        self.label.setText(f"Line: {line}, Col: {col}")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Notepad()
    win.show()
    sys.exit(app.exec())