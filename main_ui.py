# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Sun May 24 09:33:41 2009
#      by: PyQt4 UI code generator 4.5-snapshot-20090507
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Calendar(object):
    def setupUi(self, Calendar):
        Calendar.setObjectName("Calendar")
        Calendar.resize(423, 341)
        self.centralwidget = QtGui.QWidget(Calendar)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.Table = QtGui.QTableView(self.centralwidget)
        self.Table.setAlternatingRowColors(True)
        self.Table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.Table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.Table.setObjectName("Table")
        self.gridLayout.addWidget(self.Table, 0, 0, 1, 1)
        Calendar.setCentralWidget(self.centralwidget)
        self.toolBar = QtGui.QToolBar(Calendar)
        self.toolBar.setObjectName("toolBar")
        Calendar.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.NewMachine = QtGui.QAction(Calendar)
        self.NewMachine.setObjectName("NewMachine")
        self.action_Esci = QtGui.QAction(Calendar)
        self.action_Esci.setObjectName("action_Esci")
        self.toolBar.addAction(self.NewMachine)
        self.toolBar.addAction(self.action_Esci)

        self.retranslateUi(Calendar)
        QtCore.QObject.connect(self.action_Esci, QtCore.SIGNAL("activated()"), Calendar.close)
        QtCore.QMetaObject.connectSlotsByName(Calendar)

    def retranslateUi(self, Calendar):
        Calendar.setWindowTitle(QtGui.QApplication.translate("Calendar", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("Calendar", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.NewMachine.setText(QtGui.QApplication.translate("Calendar", "Inserisci &nuova macchina", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Esci.setText(QtGui.QApplication.translate("Calendar", "&Esci", None, QtGui.QApplication.UnicodeUTF8))

