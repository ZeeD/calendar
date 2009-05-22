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
    def __init__(self, dbhandler):
        QMainWindow.__init__(self)
        self.dbhandler = dbhandler
        self.ui_calendar = Ui_Calendar()
        self.ui_calendar.setupUi(self)

    def on_NewMachine_triggered(self, checked=None):
        if checked is None: return # fix a stupid double triggered
        new_machine = NewMachine(self.dbhandler)
        new_machine.exec_()
        print new_machine

if __name__ == "__main__":
    from dbhandler import HeaderTable
    from sys import argv
    from PyQt4.QtGui import QApplication
    APP = QApplication(argv)
    CALENDAR = Calendar(HeaderTable)
    CALENDAR.show()
    exit(APP.exec_())
