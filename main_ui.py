# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created: Fri May 22 08:52:19 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(423, 341)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.calendarView = QtGui.QTableWidget(self.centralwidget)
        self.calendarView.setFrameShape(QtGui.QFrame.NoFrame)
        self.calendarView.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked)
        self.calendarView.setTabKeyNavigation(False)
        self.calendarView.setDragDropOverwriteMode(False)
        self.calendarView.setAlternatingRowColors(True)
        self.calendarView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.calendarView.setObjectName("calendarView")
        self.calendarView.setColumnCount(0)
        self.calendarView.setRowCount(0)
        self.gridLayout.addWidget(self.calendarView, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.actionInserisci_nuova_macchina = QtGui.QAction(MainWindow)
        self.actionInserisci_nuova_macchina.setObjectName("actionInserisci_nuova_macchina")
        self.action_Esci = QtGui.QAction(MainWindow)
        self.action_Esci.setObjectName("action_Esci")
        self.toolBar.addAction(self.actionInserisci_nuova_macchina)
        self.toolBar.addAction(self.action_Esci)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.action_Esci, QtCore.SIGNAL("activated()"), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.calendarView.setSortingEnabled(True)
        self.toolBar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInserisci_nuova_macchina.setText(QtGui.QApplication.translate("MainWindow", "Inserisci &nuova macchina", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Esci.setText(QtGui.QApplication.translate("MainWindow", "&Esci", None, QtGui.QApplication.UnicodeUTF8))

