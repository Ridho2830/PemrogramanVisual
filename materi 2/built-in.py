import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QSlider,
    QSpinBox, QCheckBox, QComboBox
)
from PySide6.QtCore import Qt

class BuiltInWidgetsDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Built-in Widgets Demo")
        self.setMinimumWidth(400)
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Clicked signal
        self.click_label = QLabel("Jumlah klik: 0")
        self.click_count = 0
        self.click_button = QPushButton("Klik Saya")
        self.click_button.clicked.connect(self.on_button_clicked)
        layout.addWidget(self.click_label)
        layout.addWidget(self.click_button)
        
        # Text Changed signal
        self.text_label = QLabel("TEXT: -")
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Ketik sesuatu...")
        self.text_input.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.text_label)
        layout.addWidget(self.text_input)
        
        # Value Changed signal (slider + spinbox)
        slider_layout = QHBoxLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 100)
        self.spinbox = QSpinBox()
        self.spinbox.setRange(0, 100)
        
        # sinkronsasi slider dan spinbox
        self.slider.valueChanged.connect(self.spinbox.setValue)
        self.spinbox.valueChanged.connect(self.slider.setValue)
        
        slider_layout.addWidget(QLabel("Nilai:"))
        slider_layout.addWidget(self.slider)
        slider_layout.addWidget(self.spinbox)
        layout.addLayout(slider_layout)
        
        # stateChanged signal (checkbox)
        
        self.checkbox = QCheckBox("Aktifkan Fitur")
        self.feature_label = QLabel("Fitur: Nonaktif")
        self.checkbox.stateChanged.connect(self.on_checkbox_state_changed)
        layout.addWidget(self.checkbox)
        layout.addWidget(self.feature_label)
        
        # currentIndexChanged signal (combobox)
        self.combobox = QComboBox()
        self.combobox.addItems(["Merah", "Hijau", "Biru"])
        self.color_label = QLabel("Warna: -")
        self.combobox.currentIndexChanged.connect(self.on_combobox_index_changed)
        layout.addWidget(self.combobox)
        layout.addWidget(self.color_label)
        
    # slot methods
    def on_button_clicked(self):
        self.click_count += 1
        self.click_label.setText(f"Jumlah klik: {self.click_count}")
    
    def on_text_changed(self, text):
        self.text_label.setText(f"TEXT: {text}")
    
    def on_checkbox_state_changed(self, state):
        if self.checkbox.isChecked():
            status = "Aktif"
        else:
            status = "Nonaktif"
        self.feature_label.setText(f"Fitur: {status}")
        
    def on_combobox_index_changed(self, index):
        color = self.combobox.itemText(index)
        self.color_label.setText(f"Warna: {color}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    demo = BuiltInWidgetsDemo()
    demo.show()
    sys.exit(app.exec())