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
        self._db = QSqlDatabase.addDatabase('QSQLITE')
        self._db.setDatabaseName(self.dbname)
        #self.db.open()

    #def __del__(self):
        #self.db.close()

    def rowCount(self, model_index=None):
        """Tell the view how many months (rows) the model have"""
        return 12 # I'll always show from -3 to +9 months

    def columnCount(self, model_index=None):
        """Tell the view how many machines (columns) the model have"""
        try:
            self._db.open()
        except:
            raise
        else:
            query = QSqlQuery('SELECT COUNT(*) from CLIENTS')
            if not query.first():
                raise StandardError("Are you sure there's a `CLIENTS' table?")
            column_count = query.value(0).toInt()[0]
        finally:
            self._db.close()
        return column_count

    def data(self, model_index, role=None):
        """STUB: use model_index to tell the view what the hell it's inside"""
        return QVariant(QVariant.Invalid)
