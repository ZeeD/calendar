#!/usr/bin/env python

"""
Spreadsheet-like scrollable program I made for my dad
"""

from main_ui import Ui_Calendar
from PyQt4.QtGui import QMainWindow
from new_machine import NewMachine

class Calendar(QMainWindow):
    """
    Main window, should show a matrix month\client;
    the items should be mostly empty: when necessary a "DA PAGARE"
            or a date whith the payment
    """
    def __init__(self, header_table):
        QMainWindow.__init__(self)
        self.header_table = header_table
        self.ui_calendar = Ui_Calendar()
        self.ui_calendar.setupUi(self)
        self.ui_calendar.Table.setModel(self.header_table)
        self.ui_calendar.Table.resizeColumnsToContents()

    def on_NewMachine_triggered(self, checked=None):
        """Insert a new client into the database"""
        if checked is None:
            return # fix a stupid double triggered (IMHO) bug
        new_machine = NewMachine(self.header_table)
        new_machine.exec_()
        self.ui_calendar.Table.resizeColumnsToContents()

if __name__ == "__main__":
    from dbhandler import HeaderTable
    from sys import argv
    from PyQt4.QtGui import QApplication
    APP = QApplication(argv)
    CALENDAR = Calendar(HeaderTable())
    CALENDAR.show()
    exit(APP.exec_())
