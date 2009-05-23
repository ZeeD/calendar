#!/usr/bin/env python

"""
Simple dialog to add a new row into the database
"""

from PyQt4.QtGui import QDialog, QPalette, QColor
from new_machine_ui import Ui_NewMachine

class NewMachine(QDialog):
    """
    This dialog should ask the few info I need to know to create the "tabellone"
    """
    def __init__(self, dbhandler):
        QDialog.__init__(self)
        self.dbhandler = dbhandler
        self.ui_new_machine = Ui_NewMachine()
        self.ui_new_machine.setupUi(self)

    def exec_(self):
        if QDialog.exec_(self) == QDialog.Rejected:
            return False

        self.client = self.ui_new_machine.Cliente.text()
        self.machine = self.ui_new_machine.Macchina.text()
        self.selldate = self.ui_new_machine.DataInizio.selectedDate()
        self.deltamonth = self.ui_new_machine.DeltaMesi.value()
        self.anticiped = self.ui_new_machine.isAnticipato.isChecked()

        self.dbhandler.add_new_machine(self.client, self.machine,
                self.selldate, self.deltamonth, self.anticiped)
        return True

    def set_color(self, widget, boolean):
        color = QColor(255, 255, 255) if boolean else QColor(255, 0, 0)
        palette = widget.palette()
        palette.setColor(QPalette.Base, color)
        widget.setPalette(palette)

    def on_Cliente_textChanged(self, string):
        self.check_all()
        self.set_color(self.ui_new_machine.Cliente, string)

    def on_Macchina_textChanged(self, string):
        self.check_all()
        self.set_color(self.ui_new_machine.Macchina, string)

    def on_DeltaMesi_valueChanged(self, integer):
        self.check_all()
        self.set_color(self.ui_new_machine.DeltaMesi, integer)

    def check_all(self):
        self.ui_new_machine.buttonBox.setEnabled(all([
                self.ui_new_machine.Cliente.text(),
                self.ui_new_machine.Macchina.text(),
                self.ui_new_machine.DeltaMesi.value()]))

    def __str__(self):
        try:
            return '|' + ', '.join("%r" % el for el in (self.client,
                    self.machine, self.selldate, self.deltamonth,
                    self.anticiped)) + '|'
        except:
            raise StandardError('You should exec_() the object first')
