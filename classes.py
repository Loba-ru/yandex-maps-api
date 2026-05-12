from PyQt6.QtWidgets import QPushButton


class ThemeButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(40, 40)
        self.setStyleSheet("""
            QPushButton {
                border-radius: 20px;
                background-color: rgba(0, 0, 0, 150);
                color: white;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: rgba(0, 0, 0, 200);
            }
        """)
        self.set_dark(False)

    def set_dark(self, dark):
        self.dark = dark
        self.setText("🌙" if dark else "☀️")

    def toggle(self):
        self.set_dark(not self.dark)
        return self.dark
