#!/usr/bin/env python

"""
Simple dialog to add a new row into the database
"""

from PyQt4.QtGui import QDialog, QPalette, QColor
from new_machine_ui import Ui_NewMachine

def set_color(widget, boolean):
    color = QColor(255, 255, 255) if boolean else QColor(255, 0, 0)
    palette = widget.palette()
    palette.setColor(QPalette.Base, color)
    widget.setPalette(palette)

class NewMachine(QDialog):
    """
    This dialog should ask the few info I need to know to create the "tabellone"
    """
    def __init__(self, dbhandler):
        QDialog.__init__(self)
        self.dbhandler = dbhandler
        self.ui_new_machine = Ui_NewMachine()
        self.ui_new_machine.setupUi(self)

    @property
    def client(self):
        """Cliente lineedit wrapper"""
        return self.ui_new_machine.Cliente.text()

    @property
    def machine(self):
        """Macchina lineedit wrapper"""
        return self.ui_new_machine.Macchina.text()

    @property
    def selldate(self):
        """DataInizio calendar wrapper"""
        return self.ui_new_machine.DataInizio.selectedDate()

    @property
    def deltamonth(self):
        """DeltaMesi spinbox wrapper"""
        return self.ui_new_machine.DeltaMesi.value()

    @property
    def anticiped(self):
        """isAnticipato checkbox wrapper"""
        return self.ui_new_machine.isAnticipato.isChecked()

    def exec_(self):
        """Add the defined new machine into the database"""
        if QDialog.exec_(self) == QDialog.Rejected:
            return False
        self.dbhandler.add_new_machine(self.client, self.machine,
                self.selldate, self.deltamonth, self.anticiped)
        return True

    def on_Cliente_textChanged(self, string):
        """Slot invoked when I type a char into the Cliente lineedit"""
        # pylint: disable-msg=C0103
        self.check_all()
        set_color(self.ui_new_machine.Cliente, string)

    def on_Macchina_textChanged(self, string):
        """Slot invoked when I type a char into the Macchina lineedit"""
        # pylint: disable-msg=C0103
        self.check_all()
        set_color(self.ui_new_machine.Macchina, string)

    def on_DeltaMesi_valueChanged(self, integer):
        """Slot invoked when I select a int into the DeltaMesi spinbox"""
        # pylint: disable-msg=C0103
        self.check_all()
        set_color(self.ui_new_machine.DeltaMesi, integer)

    def check_all(self):
        """Just check if *all* needed info are setted"""
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
