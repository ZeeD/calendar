# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_machine.ui'
#
# Created: Fri May 22 09:01:51 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(283, 323)
        self.formLayout = QtGui.QFormLayout(Dialog)
        self.formLayout.setObjectName("formLayout")
        self.DataInizio = QtGui.QCalendarWidget(Dialog)
        self.DataInizio.setObjectName("DataInizio")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.DataInizio)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName("label")
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.Cliente = QtGui.QLineEdit(Dialog)
        self.Cliente.setObjectName("Cliente")
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.Cliente)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_2)
        self.Macchina = QtGui.QLineEdit(Dialog)
        self.Macchina.setObjectName("Macchina")
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.Macchina)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_3)
        self.DeltaMesi = QtGui.QSpinBox(Dialog)
        self.DeltaMesi.setObjectName("DeltaMesi")
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.DeltaMesi)
        self.isAnticipato = QtGui.QCheckBox(Dialog)
        self.isAnticipato.setObjectName("isAnticipato")
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.isAnticipato)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.buttonBox)
        self.label.setBuddy(self.Cliente)
        self.label_2.setBuddy(self.Macchina)
        self.label_3.setBuddy(self.DeltaMesi)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Cliente", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dialog", "Macchina", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dialog", "Durata contrato", None, QtGui.QApplication.UnicodeUTF8))
        self.DeltaMesi.setSuffix(QtGui.QApplication.translate("Dialog", " mesi", None, QtGui.QApplication.UnicodeUTF8))
        self.DeltaMesi.setPrefix(QtGui.QApplication.translate("Dialog", "ogni ", None, QtGui.QApplication.UnicodeUTF8))
        self.isAnticipato.setText(QtGui.QApplication.translate("Dialog", "Pagamento anticipato", None, QtGui.QApplication.UnicodeUTF8))

