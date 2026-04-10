"""
Nama : Rafly Ridho Sukardi
NIM  : F1D02310134
Kelas: D

"""


import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit,
    QPushButton, QLabel, QComboBox, QHBoxLayout, QFrame
)


class Kalkulator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Kalkulator Modern")
        self.setMinimumWidth(400)
        self.setStyleSheet(self.global_style())

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(0)

        card = QFrame()
        card.setObjectName("card")
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Judul
        title = QLabel("Kalkulator Modern")
        title.setObjectName("title")
        layout.addWidget(title)

        layout.addSpacing(4)

        # Input 1
        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Angka pertama, contoh: 5")
        self.input1.setFixedHeight(40)
        layout.addWidget(self.input1)

        layout.addSpacing(4)

        # Operasi
        self.combo = QComboBox()
        self.combo.addItems(["Tambah (+)", "Kurang (-)", "Kali (*)", "Bagi (/)"])
        self.combo.setFixedHeight(40)
        layout.addWidget(self.combo)

        layout.addSpacing(4)

        # Input 2
        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("Angka kedua, contoh: 10")
        self.input2.setFixedHeight(40)
        layout.addWidget(self.input2)

        # Error
        self.error = QLabel("")
        self.error.setObjectName("error")
        self.error.setFixedHeight(22)
        layout.addWidget(self.error)

        # Tombol
        btn_row = QHBoxLayout()
        btn_row.setSpacing(10)
        self.btn_hitung = QPushButton("Hitung")
        self.btn_clear  = QPushButton("Clear")
        self.btn_hitung.setObjectName("primary")
        self.btn_clear.setObjectName("danger")
        self.btn_hitung.setFixedHeight(44)
        self.btn_clear.setFixedHeight(44)
        btn_row.addWidget(self.btn_hitung)
        btn_row.addWidget(self.btn_clear)
        layout.addLayout(btn_row)

        layout.addSpacing(6)

        # Hasil
        self.hasil = QLabel("Hasil: —")
        self.hasil.setObjectName("result")
        self.hasil.setFixedHeight(50)
        layout.addWidget(self.hasil)

        card.setLayout(layout)
        main_layout.addWidget(card)
        self.setLayout(main_layout)
        self.adjustSize()

        # Signal
        self.input1.textChanged.connect(self.validate)
        self.input2.textChanged.connect(self.validate)
        self.btn_hitung.clicked.connect(self.hitung)
        self.btn_clear.clicked.connect(self.clear)

        self.btn_hitung.setEnabled(False)

    def _label(self, text):
        lbl = QLabel(text)
        lbl.setObjectName("fieldLabel")
        return lbl

    # ── STYLE ─────────────────────────────────────────────
    def global_style(self):
        return """
        QWidget {
            background-color: #12121f;
            color: #e0e0f0;
            font-family: 'Segoe UI', sans-serif;
            font-size: 13px;
        }

        QLabel#title {
            font-size: 18px;
            font-weight: bold;
            color: #a89cff;
        }

        QLabel#fieldLabel {
            color: #9090b8;
            font-size: 12px;
        }

        QLabel#error {
            color: #ff6b6b;
            font-size: 12px;
        }

        QLabel#result {
            background: #12121f;
            border-radius: 12px;
            padding: 0 16px;
            font-size: 16px;
            font-weight: bold;
            color: #a89cff;
            border: 1px solid #2e2e4a;
            qproperty-alignment: AlignCenter;
        }

        QFrame#card {
            background-color: #1e1e30;
            border-radius: 16px;
            border: 1px solid #2e2e4a;
        }

        QLineEdit {
            background: #12121f;
            border: 2px solid #2e2e4a;
            border-radius: 10px;
            padding: 0 12px;
            color: #e0e0f0;
        }

        QLineEdit:focus {
            border: 2px solid #6c63ff;
            background: #16162a;
        }

        QLineEdit[valid="false"] {
            border: 2px solid #ff6b6b;
        }

        QComboBox {
            background: #12121f;
            border: 2px solid #2e2e4a;
            border-radius: 10px;
            padding: 0 12px;
            color: #e0e0f0;
        }

        QComboBox:focus {
            border: 2px solid #6c63ff;
        }

        QComboBox::drop-down {
            border: none;
            width: 24px;
        }

        QComboBox QAbstractItemView {
            background: #1e1e30;
            border: 1px solid #3a3a5a;
            selection-background-color: #6c63ff;
            color: #e0e0f0;
            padding: 4px;
        }

        QPushButton {
            border-radius: 10px;
            padding: 0 16px;
            font-weight: bold;
            font-size: 13px;
            border: none;
        }

        QPushButton#primary {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #6c63ff, stop:1 #8f7fff);
            color: #ffffff;
        }

        QPushButton#primary:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #5a52e0, stop:1 #7a6fe0);
        }

        QPushButton#primary:disabled {
            background: #2a2a40;
            color: #555575;
        }

        QPushButton#danger {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #ff5c5c, stop:1 #ff8080);
            color: #ffffff;
        }

        QPushButton#danger:hover {
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 #d94a4a, stop:1 #e06060);
        }
        """

    # ── VALIDASI ──────────────────────────────────────────
    def validate(self):
        t1 = self.input1.text().strip()
        t2 = self.input2.text().strip()

        if not t1 and not t2:
            self._reset_inputs()
            self.btn_hitung.setEnabled(False)
            return

        if t1 and not self._is_number(t1):
            self._set_error(self.input1, "Angka pertama tidak valid")
            return

        if t2 and not self._is_number(t2):
            self._set_error(self.input2, "Angka kedua tidak valid")
            return

        self._clear_error()
        self.btn_hitung.setEnabled(bool(t1 and t2))

    def _is_number(self, text):
        try:
            float(text)
            return True
        except ValueError:
            return False

    def _set_error(self, widget, msg):
        self._reset_inputs()
        widget.setProperty("valid", "false")
        widget.style().unpolish(widget)
        widget.style().polish(widget)
        self.error.setText(msg)
        self.btn_hitung.setEnabled(False)

    def _reset_inputs(self):
        for w in (self.input1, self.input2):
            w.setProperty("valid", "")
            w.style().unpolish(w)
            w.style().polish(w)

    def _clear_error(self):
        self._reset_inputs()
        self.error.setText("")

    # ── HITUNG ────────────────────────────────────────────
    def hitung(self):
        a  = float(self.input1.text())
        b  = float(self.input2.text())
        op = self.combo.currentText()

        if "Bagi" in op:
            if b == 0:
                self.error.setText("Tidak bisa membagi dengan nol!")
                self.hasil.setText("Hasil: Error")
                self.hasil.setStyleSheet("color: #ff6b6b; qproperty-alignment: AlignCenter;")
                return
            result = a / b
        elif "Tambah" in op:
            result = a + b
        elif "Kurang" in op:
            result = a - b
        else:
            result = a * b

        self.hasil.setText(f"Hasil:  {self._fmt(result)}")
        self.hasil.setStyleSheet("")

    def _fmt(self, n):
        if n == int(n) and abs(n) < 1e15:
            return f"{int(n):,}".replace(",", ".")
        return f"{n:.8f}".rstrip("0").rstrip(".")

    # ── CLEAR ─────────────────────────────────────────────
    def clear(self):
        self.input1.clear()
        self.input2.clear()
        self.hasil.setText("Hasil: —")
        self.hasil.setStyleSheet("")
        self.error.setText("")
        self._reset_inputs()
        self.btn_hitung.setEnabled(False)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Kalkulator()
    window.show()
    sys.exit(app.exec())