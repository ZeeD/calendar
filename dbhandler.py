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
from PyQt4.QtCore import QAbstractTableModel, QModelIndex, QVariant, Qt
from datetime import date

class HeaderTable(QAbstractTableModel):
    """
    Strange Table model that reverse the real table
    """
    def __init__(self, dbname='calendar.db'):
        QAbstractTableModel.__init__(self)
        self.dbname = dbname
        self._db = QSqlDatabase.addDatabase('QSQLITE')
        self._db.setDatabaseName(self.dbname)

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
            query = QSqlQuery('SELECT COUNT(*) FROM clients', self._db)
            if not query.first():
                raise StandardError("No table found (or no elements)")
            column_count = query.value(0).toInt()[0]
        finally:
            self._db.close()
        return column_count

    def data(self, model_index, role=None):
        """STUB: use model_index to tell the view what the hell it's inside"""
        return QVariant(QVariant.Invalid)

    def headerData(self, section, orientation, role=None):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            try:
                self._db.open()
            except:
                raise
            else:
                query = QSqlQuery('''SELECT
                        client, machine, selldate, deltamonth, anticiped
                        FROM clients
                        ORDER BY client, machine, selldate''', self._db)
                if not query.first():
                    raise StandardError("Non c'e' manco un risultato?")
                if not query.seek(section):
                    raise StandardError('Not enough elements into the table')
                string = '%s\n%s\n%s\nOgni %s mesi\nPagamento %scipato' % (
                        query.value(0).toString(),
                        query.value(1).toString(),
                        query.value(2).toDate().toPyDate().strftime('%d %B %Y'), # data
                        query.value(3).toInt()[0], # intero
                        'anti' if query.value(4).toBool() else 'posti')
                return QVariant(string)
            finally:
                self._db.close()
        else:
            today = date.today()
            year = today.year
            # inizio da -3 e finisco a + 9
            month = today.month - 3 + section
            if month > 12:
                year = today.year + 1
                month = ((month - 1) % 12 ) + 1
            return QVariant(date(year, month, 1).strftime('%B %Y'))

    def add_new_machine(self, client, machine, selldate, deltamonth, anticiped):
        """Insert a single row into the CLIENTS table"""
        try:
            self._db.open()
        except:
            raise
        else:
            query = QSqlQuery(self._db)
            query.prepare('''INSERT INTO clients
                    (client, machine, selldate, deltamonth, anticiped)
                    VALUES
                    (:client, :machine, :selldate, :deltamonth, :anticiped)''')
            query.bindValue(':client', QVariant(client))
            query.bindValue(':machine', QVariant(machine))
            query.bindValue(':selldate', QVariant(selldate))
            query.bindValue(':deltamonth', QVariant(deltamonth))
            query.bindValue(':anticiped', QVariant(anticiped))
            query.exec_()
        finally:
            self._db.close()
