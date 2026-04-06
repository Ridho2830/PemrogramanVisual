import sys
from PySide6.QtWidgets import (QApplication, QPushButton, QLabel, QVBoxLayout, QWidget, QLineEdit)

class SignalSlotDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Signal & Slot Demo")
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # label untuk menampilkan hasil
        self.label = QLabel("Ketik Sesuatu di bawah....")
        layout.addWidget(self.label)
        
        # input field
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Ketik disini...")
        layout.addWidget(self.input_field)
        
        # button
        self.button = QPushButton("Reset")
        layout.addWidget(self.button)
        
        # menhubungkan sinyal textChanged dari QLineEdit ke slot
        
        # cara 1 signal ke fungsi biasa
        self.button.clicked.connect(self.reset_text)
        
        # cara 2 signal ke lambda function
        self.input_field.textChanged.connect(lambda text: self.label.setText(f"Kamu mengetik: {text}"))
        
        # cara 3 satu signal ke beberapa slot
        self.button.clicked.connect(lambda: self.label.setText("Input telah direset!"))
        
    def reset_text(self):
        self.input_field.clear()
        self.label.setText("text telah direset!")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = SignalSlotDemo()
    demo.show()
    sys.exit(app.exec())