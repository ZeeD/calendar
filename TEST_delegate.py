#!/usr/bin/env python

from PyQt4.QtGui import QStandardItemModel, QItemDelegate, QSpinBox
from PyQt4.QtCore import QVariant, Qt

class CustomModel(QStandardItemModel):
    def __init__(self, w=3, h=4):
        QStandardItemModel.__init__(self, w, h)
        for r in range(w):
            for c in range(h):
                QStandardItemModel.setData(self, self.index(r, c),
                        QVariant((r+1)*(c+1)))

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
