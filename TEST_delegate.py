#!/usr/bin/env python

from PyQt4.QtGui import QItemDelegate, QSpinBox
from PyQt4.QtCore import QVariant, Qt, QAbstractTableModel

class CustomModel(QAbstractTableModel):
    def __init__(self, w=3, h=4):
        QAbstractTableModel.__init__(self)
        self._data = [ [ (r+1)*(c+1) for c in range(h) ] for r in range(w) ]
        self._w = w
        self._h = h

    def rowCount(self, parent=None):
        return self._w

    def columnCount(self, parent=None):
        return self._h

    def data(self, index, role=None):
        if not index.isValid() or role not in (Qt.DisplayRole, Qt.EditRole):
            return QVariant()
        return QVariant(self._data[index.row()][index.column()])

    def setData(self, index, value, role=None):
        self._data[index.row()][index.column()] = value
        return True

    def flags(self, index):
        if index.isValid():
            return Qt.ItemIsEditable | Qt.ItemIsSelectable | Qt.ItemIsEnabled
        else:
            return Qt.NoItemFlags

class CustomDelegate(QItemDelegate):
    def createEditor(self, parent, option, index):
        return QSpinBox(parent)

    def setEditorData(self, editor, index):
        editor.setValue(index.model().data(index, Qt.EditRole).toInt()[0])

    def setModelData(self, editor, model, index):
        editor.interpretText()
        model.setData(index, QVariant(editor.value()), Qt.EditRole)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

if __name__ == '__main__':
    from PyQt4.QtGui import QApplication, QTableView
    app = QApplication(['dummy'])
    view = QTableView()
    model = CustomModel(5, 5)
    view.setModel(model)
    delegate = CustomDelegate()
    view.setItemDelegate(delegate)
    view.show()
    exit(app.exec_())
