#!/usr/bin/env python

"""
Spreadsheet-like scrollable program I made for my dad
"""

from main_ui import Ui_Calendar
from PyQt4.QtGui import QMainWindow, QPrinter, QPrintDialog, QDialog, QPainter
from new_machine import NewMachine
from dbhandler import EditableCheckboxDate

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
        self.delegate = EditableCheckboxDate()
        self.ui_calendar.Table.setItemDelegate(self.delegate)
        self.ui_calendar.Table.resizeColumnsToContents()

    def on_NewMachine_triggered(self, checked=None):
        """Insert a new client into the database"""
        # pylint: disable-msg=C0103
        if checked is None:
            return # fix a stupid double triggered (IMHO) bug
        new_machine = NewMachine(self.header_table)
        new_machine.exec_()
        self.ui_calendar.Table.resizeColumnsToContents()

    def on_stampa_triggered(self, checked=None):
        """Slot launched when the user click on the "stampa" button"""
        if checked is None:
            return
        printer = QPrinter()
        print_dialog = QPrintDialog(printer, self)
        if print_dialog.exec_() == QDialog.Accepted:
            printer.setOrientation(QPrinter.Landscape)
            painter = QPainter()
            painter.begin(printer)
            geometry = self.ui_calendar.Table.geometry()
            self.ui_calendar.Table.setGeometry(printer.pageRect())
            self.ui_calendar.Table.render(painter)
            self.ui_calendar.Table.setGeometry(geometry)
            painter.end()

    def on_MonthsBeforeSlider_valueChanged(self, value):
        """add/remove the model to calculate the values for value months"""
        model = self.ui_calendar.Table.model()
        model.months_before = value
        model.update_db_content()

    def on_MonthsAfterSlider_valueChanged(self, value):
        """add/remove the model to calculate the values for value months"""
        model = self.ui_calendar.Table.model()
        model.months_after = value
        model.update_db_content()

if __name__ == "__main__":
    from dbhandler import HeaderTable
    from sys import argv
    from PyQt4.QtGui import QApplication
    APP = QApplication(argv)
    CALENDAR = Calendar(HeaderTable())
    CALENDAR.show()
    exit(APP.exec_())
