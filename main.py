#!/usr/bin/env python

"""
Spreadsheet-like scrollable program I made for my dad
"""

from main_ui import Ui_Calendar
from PyQt4.QtGui import QMainWindow
from new_machine import NewMachine

DEBUG = True

def PRINT(*args, **kwargs):
    if DEBUG:
        print "DBG args=%r, kwargs=%r" % (args, kwargs)

class Calendar(QMainWindow):
    def __init__(self, header_table):
        QMainWindow.__init__(self)
        self.header_table = header_table
        self.ui_calendar = Ui_Calendar()
        self.ui_calendar.setupUi(self)
        self.ui_calendar.Table.setModel(self.header_table)

    def on_NewMachine_triggered(self, checked=None):
        if checked is None: return # fix a stupid double triggered (IMHO) bug
        new_machine = NewMachine(self.header_table)
        new_machine.exec_()
        print new_machine

if __name__ == "__main__":
    from dbhandler import HeaderTable
    from sys import argv
    from PyQt4.QtGui import QApplication
    APP = QApplication(argv)
    CALENDAR = Calendar(HeaderTable())
    CALENDAR.show()
    exit(APP.exec_())
