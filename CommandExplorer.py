#!/usr/bin/env python3

# CommandExplorer

# Created 2022 by James Bishop (james@bishopdynamics.com)

import sys

from PyQt6.QtWidgets import QApplication
from Mod_MainWindow import MainWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec())