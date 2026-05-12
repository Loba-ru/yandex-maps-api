from PyQt6.QtWidgets import (
    QGraphicsDropShadowEffect,
    QWidget,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)
from PyQt6.QtCore import Qt


class SearchWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        self.line_edit = QLineEdit()
        self.line_edit.setPlaceholderText("Адрес или объект")
        self.line_edit.setMinimumWidth(200)
        self.line_edit.setFixedHeight(30)
        self.line_edit.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                border: 1px solid #ccc;
                border-top-left-radius: 5px;
                border-bottom-left-radius: 5px;
                border-top-right-radius: 0;
                border-bottom-right-radius: 0;
                background-color: white;
                color: black;
            }
        """)

        self.button = QPushButton("Искать")
        self.button.setFixedWidth(60)
        self.button.setFixedHeight(30)
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #f39c12;
                color: white;
                border: 1px solid #e67e22;
                border-top-right-radius: 5px;
                border-bottom-right-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #e67e22;
                border-color: #d35400;
            }
        """)

        layout.addWidget(self.line_edit)
        layout.addWidget(self.button)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setOffset(2, 2)
        shadow.setColor(Qt.GlobalColor.gray)
        self.setGraphicsEffect(shadow)


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
