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

from PyQt4.QtSql import QSqlDatabase
from PyQt4.QtCore import QAbstractTableModel

class HeaderTable(QAbstractTableModel):
    """
    Strange Table model that reverse the real table
    """
    def __init__(self, dbname='calendar.db'):
        self.dbname = dbname
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        self.db.setDatabaseName(self.dbname)
        #self.db.open()

    def __del__(self):
        pass # self.db.close()
