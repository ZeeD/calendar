#!/usr/bin/env python

"""

"""

from PyQt4.QtGui import QDialog
from new_machine_ui import Ui_NewMachine

class NewMachine(QDialog):
    """

    """
    def __init__(self, header_table):
        QDialog.__init__(self)
        self.dbhandler = header_table
        self.ui_new_machine = Ui_NewMachine()
        self.ui_new_machine.setupUi(self)
