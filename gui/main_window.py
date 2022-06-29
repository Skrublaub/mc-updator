import requests

from backend.github.download_tools import start_requests_session
from backend.github.parse_tools import get_amt_pages, format_api_link
from PyQt6.QtWidgets import QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QCheckBox, QBoxLayout

from typing import Any


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        icon = QIcon("gui/icons/mc.png")
        self.setWindowIcon(icon)

        s: requests.Session = start_requests_session()

        # amt_pages: int = get_amt_pages(s)  # could be used later

        page_json: list[Any] = s.get(format_api_link()).json()

    def get_check_boxes(self, assets: list[Any]) -> QCheckBox:
        pass
