#!/usr/bin/env python

"""
Spreadsheet-like scrollable program I made for my dad
"""

from main_ui import Ui_MainWindow
from PyQt4.QtGui import QApplication, QMainWindow

if __name__ == "__main__":
    from sys import argv
    APP = QApplication(argv)
    MAIN = QMainWindow()
    UI = Ui_MainWindow()
    UI.setupUi(MAIN)
    MAIN.show()
    exit(APP.exec_())
