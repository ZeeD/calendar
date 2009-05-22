#!/usr/bin/env python

"""
Database handler: I need to store something like
                                             +-------+
+------+-------+--------+----------+---------+CLIENTS|
|Client|Machine|SellDate|DeltaMonth|Anticiped+-------+
+------+-------+--------+----------+---------+
|String|String |Date    |Integer   |Boolean  |
+------+-------+--------+----------+---------+
    ^      ^
    |      +----------+                 +--------+
+---+----------+------+--------+--------+PAYMENTS|
|CLIENTS_Client|CLIENTS_Machine|DatePayd+--------+
+--------------+---------------+--------+
|String        |String         |Date    |
+--------------+---------------+--------+

The real problem I need to show this simple tables like

     |Client    |Client    |Client    |Client
     |Machine   |Machine   |Machine   |Machine
     |DeltaMonth|DeltaMonth|DeltaMonth|DeltaMonth
-----+----------+----------+----------+----------- ...
month|          | PAYD DATE|          |
month| TO CHECK |          |          |
month|          |          | TO CHECK |
month|          |          |          |
...                                                ...

"""

from PyQt4.QtSql import QSqlDatabase, QSqlQuery
from PyQt4.QtCore import QAbstractTableModel, QModelIndex, QVariant

class HeaderTable(QAbstractTableModel):
    """
    Strange Table model that reverse the real table
    """
    def __init__(self, dbname='calendar.db'):
        QAbstractTableModel.__init__(self)
        self.dbname = dbname
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(self.dbname)
        #self.db.open()

    #def __del__(self):
        #self.db.close()

    def rowCount(self, model_index=None):
        # mostro da -3 a +9 mesi
        return 12

    def columnCount(self, model_index=None):
        try:
            self.db.open()
        except:
            raise
        else:
            query = QSqlQuery('SELECT COUNT(*) from CLIENTS')
            if not query.first():
                raise "Are you sure there's a `CLIENTS' table?"
            column_count = query.value(0).toInt()[0]
        finally:
            self.db.close()
        return column_count

    def data(self, model_index, role=None):
        return QVariant(QVariant.Invalid)
