#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4.QtGui import QApplication, QMainWindow, QWidget, QTableWidget, \
        QTableWidgetItem, QGridLayout
from PyQt4.QtCore import QMetaObject

def setupUi(MainWindow):
    centralwidget = QWidget(MainWindow)
    MainWindow.setCentralWidget(centralwidget)
    gridLayout = QGridLayout(centralwidget)

    calendarView = QTableWidget(centralwidget)
    calendarView.setColumnCount(4)
    calendarView.setRowCount(2)
    calendarView.setVerticalHeaderItem(0, QTableWidgetItem("Gennaio"))
    calendarView.setVerticalHeaderItem(1, QTableWidgetItem("Febbraio"))
    calendarView.setHorizontalHeaderItem(0,
            QTableWidgetItem("Cliente1\nKyocera\nogni 6 mesi (anticipato)"))
    calendarView.setHorizontalHeaderItem(1,
            QTableWidgetItem("Cliente2\nFoo\nogni 6 mesi (anticipato)"))
    calendarView.setHorizontalHeaderItem(2,
            QTableWidgetItem("Cliente3\nbar\nogni 6 mesi (anticipato)"))
    calendarView.setHorizontalHeaderItem(3,
            QTableWidgetItem("Cliente4\nFoobar\nogni 6 mesi (anticipato)"))

    gridLayout.addWidget(calendarView, 0, 0, 1, 1)
    QMetaObject.connectSlotsByName(MainWindow)

if __name__ == "__main__":
    APP = QApplication(['dummy'])
    MAIN = QMainWindow()
    setupUi(MAIN)
    MAIN.show()
    raise SystemExit(APP.exec_())
