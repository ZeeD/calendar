#!/usr/bin/env python

from main_ui import Ui_MainWindow
from PyQt4.QtGui import QApplication, QMainWindow

if __name__ == "__main__":
    APP = QApplication(['dummy'])
    MAIN = QMainWindow()
    UI = Ui_MainWindow()
    UI.setupUi(MAIN)
    MAIN.show()
    raise SystemExit(APP.exec_())
