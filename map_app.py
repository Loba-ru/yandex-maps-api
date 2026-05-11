import sys
import requests
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

API_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"


class MapWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Карта")
        self.setFixedSize(650, 450)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # Координаты г. Воронеж:
        self.latitude = 51.66078  # с.ш.
        self.longitude = 39.2003  # в.д.

        self.min_latitude = -70  # -90
        self.max_latitude = 70  # 90

        self.min_longitude = -180
        self.max_longitude = 180

        self.step = 0.2  # 20% сдвиг

        self.min_zoom = 2
        self.max_zoom = 20
        self.zoom = 12

        self.load_map()

    def load_map(self):
        # Статическая карта Yandex Maps
        width, height = self.width(), self.height()
        url = (
            f"https://static-maps.yandex.ru/v1?"
            f"ll={self.longitude},{self.latitude}&z={self.zoom}"
            f"&size={width},{height}&apikey={API_KEY}"
        )
        try:
            response = requests.get(url)
            if response.status_code == 200:
                pixmap = QPixmap()
                pixmap.loadFromData(response.content)
                self.label.setPixmap(pixmap)
            else:
                self.label.setText("Ошибка загрузки карты")
        except:
            self.label.setText("Ошибка соединения")

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key.Key_PageUp:
            if self.zoom < self.max_zoom:
                self.zoom += 1
                self.load_map()
        elif key == Qt.Key.Key_PageDown:
            if self.zoom > self.min_zoom:
                self.zoom -= 1
                self.load_map()
        elif key == Qt.Key.Key_Left:
            delta_lon = (360 / (2**self.zoom)) * self.step
            self.longitude -= delta_lon
            if self.longitude < -180:
                self.longitude += 360
            self.load_map()
        elif key == Qt.Key.Key_Right:
            delta_lon = (360 / (2**self.zoom)) * self.step
            self.longitude += delta_lon
            if self.longitude > 180:
                self.longitude -= 360
            self.load_map()
        elif key == Qt.Key.Key_Up:
            delta = (180 / (2**self.zoom)) * self.step
            new_latitude = self.latitude + delta
            if new_latitude <= self.max_latitude:
                self.latitude = new_latitude
                self.load_map()
        elif key == Qt.Key.Key_Down:
            delta = (180 / (2**self.zoom)) * self.step
            new_latitude = self.latitude - delta
            if new_latitude >= self.min_latitude:
                self.latitude = new_latitude
                self.load_map()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec())
