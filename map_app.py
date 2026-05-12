import sys
import requests
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QVBoxLayout,
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

from classes import ThemeButton, SearchWidget

STATIC_MAPS_API_KEY = "f3a0fe3a-b07e-4840-a1da-06f18b2ddf13"
GEOCODE_MAPS_API_KEY = "8013b162-6b42-4997-9691-77b7074026e0"


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

        self.search_widget = SearchWidget(self.label)
        self.search_widget.move(10, 10)
        self.search_widget.button.clicked.connect(self.search_object)
        self.search_widget.line_edit.returnPressed.connect(self.search_object)

        self.theme_btn = ThemeButton(self.label)
        self.theme_btn.move(580, 10)  # 650 - 70
        self.theme_btn.clicked.connect(self.change_theme)

        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.setFocus()

        self.mark_latitude = None
        self.mark_longitude = None

        self.dark_theme = False

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

        params = "&theme=dark" if self.dark_theme else ""

        is_object_marked = not (
            self.mark_longitude is None or self.mark_latitude is None
        )
        if is_object_marked:
            params += f"&pt={self.mark_longitude},{self.mark_latitude},pm2rdl"

        url = (
            f"https://static-maps.yandex.ru/v1?"
            f"ll={self.longitude},{self.latitude}&z={self.zoom}"
            f"&size={width},{height}&apikey={STATIC_MAPS_API_KEY}{params}"
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

    def change_theme(self):
        self.dark_theme = self.theme_btn.toggle()
        self.load_map()

    def search_object(self):
        query = self.search_widget.line_edit.text().strip()
        if not query:
            return

        geocoder_url = (
            f"https://geocode-maps.yandex.ru/1.x/?"
            f"apikey={GEOCODE_MAPS_API_KEY}&geocode={query}&format=json"
        )

        try:
            response = requests.get(geocoder_url)
            if response.status_code == 200:
                data = response.json()
                geo_collection = data["response"]["GeoObjectCollection"]
                toponym = geo_collection["featureMember"][0]["GeoObject"]
                coords = toponym["Point"]["pos"]
                longitude, latitude = map(float, coords.split())
                self.longitude = longitude
                self.latitude = latitude
                self.mark_longitude = longitude
                self.mark_latitude = latitude
                self.load_map()
        except:
            pass

        self.setFocus()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapWindow()
    window.show()
    sys.exit(app.exec())
