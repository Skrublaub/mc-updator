from PyQt6.QtWidgets import  QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import
from PyQt6.QtWidgets import QCheckBox, QBoxLayout

from typing import Any

from backend.github.parse_tools import get_versions

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        icon = QIcon("gui/icons/mc.png")

        self.setWindowIcon(icon)

        assets: list[Any] = get_versions(1)[2]

    def get_check_boxes(self, assets: list[Any]) -> QCheckBox:
