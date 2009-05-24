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
from PyQt4.QtCore import QAbstractTableModel, QVariant, Qt, SIGNAL, QDate
from datetime import date, datetime

class HeaderTable(QAbstractTableModel):
    """
    Strange Table model that reverse the real table
    """
    def __init__(self, dbname='calendar.db'):
        QAbstractTableModel.__init__(self)
        self.dbname = dbname
        self._db = QSqlDatabase.addDatabase('QSQLITE')
        self._db.setDatabaseName(self.dbname)
        self._db.open()
        self.months_before = 3
        self.months_afther = 9

    def __del__(self):
        self._db.close()

    def rowCount(self, model_index=None):
        """Tell the view how many months (rows) the model have"""
        # pylint: disable-msg=C0103
        assert not model_index.isValid()
        return self.months_before + self.months_afther

    def columnCount(self, model_index=None):
        """Tell the view how many machines (columns) the model have"""
        # pylint: disable-msg=C0103
        assert not model_index.isValid()
        query = QSqlQuery('SELECT COUNT(*) FROM clients', self._db)
        if not query.first():
            raise StandardError("No table found (or no elements)")
        return query.value(0).toInt()[0]

    def data(self, model_index, role=None):
        """TODO: use model_index to tell the view what the hell it's inside"""
        if role != Qt.DisplayRole:
            return QVariant()
        # find the month from the row number
        month_year = datetime.strptime(unicode(self.headerData(model_index.row(),
                Qt.Vertical, role).toString()), '%B %Y')
        month = month_year.month
        year = month_year.year
        # find the client from the column number
        client_machine = unicode(self.headerData(model_index.column(),
                Qt.Horizontal, role).toString()).split('\n')
        client = client_machine[0]
        machine = client_machine[1]
        selldate = datetime.strptime(client_machine[2], '%d %B %Y').date()
        deltamonth = int(client_machine[3][5:-5]) # [len('Ogni '):-len(' mesi')]
        anticiped = client_machine[4][10:-6] == 'anti' # 'Pagamento ':-'cipato'

        print 'searching if (%s|%s|%s|%s|%s) has something into (%s|%s)' % (
                client, machine, selldate, deltamonth, anticiped,
                month, year)

        query = QSqlQuery("""SELECT datepayd, payed FROM payments WHERE
                clients_client = :client AND clients_machine = :machine AND
                clients_selldate = :selldate AND
                datepayd BETWEEN :datebefore AND :dateafter""", self._db)
        query.bindValue(':client', QVariant(client))
        query.bindValue(':machine', QVariant(machine))
        query.bindValue(':selldate', QVariant(selldate))
        # primo giorno del mese
        d = QDate(year, month, 1)
        query.bindValue(':datebefore', QVariant(d))
        # ultimo giorno del mese
        query.bindValue(':dateafter', QVariant(d.addMonths(1).addDays(-1)))
        while query.next():
            datepayd = query.value(0).toDate()
            payed = query.value(1).toBool()
            print '-f> found (%s|%s)' % (datepayd, payed)
        return QVariant()

    def headerData(self, section, orientation, role=None):
        """Generate the months on the rows and the clients on the columns"""
        # pylint: disable-msg=C0103
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            query = QSqlQuery('''SELECT
                    client, machine, selldate, deltamonth, anticiped
                    FROM clients
                    ORDER BY client, machine, selldate''', self._db)
            if not query.first():
                raise StandardError("Non c'e' manco un risultato?")
            if not query.seek(section):
                raise StandardError('Not enough elements into the table')

            return QVariant('%s\n%s\n%s\nOgni %s mesi\nPagamento %scipato' % (
                    query.value(0).toString(), query.value(1).toString(),
                    query.value(2).toDate().toPyDate().strftime('%d %B %Y'),
                    query.value(3).toInt()[0],
                    'anti' if query.value(4).toBool() else 'posti'))
        else:
            today = date.today()
            year = today.year
            month = today.month - self.months_before + section
            if month > 12:
                year = today.year + 1
                month = ((month - 1) % 12 ) + 1
            return QVariant(date(year, month, 1).strftime('%B %Y'))

    def add_new_machine(self, client, machine, selldate, deltamonth, anticiped):
        """Insert a single row into the CLIENTS table"""
        query = QSqlQuery('''INSERT INTO clients
                (client, machine, selldate, deltamonth, anticiped)
                VALUES
                (:client, :machine, :selldate, :deltamonth, :anticiped)''',
                self._db)
        query.bindValue(':client', QVariant(client))
        query.bindValue(':machine', QVariant(machine))
        query.bindValue(':selldate', QVariant(selldate))
        query.bindValue(':deltamonth', QVariant(deltamonth))
        query.bindValue(':anticiped', QVariant(anticiped))
        query.exec_()
        self.update_db_content()

    def update_db_content(self):
        """Populate the payment table ensuring all "visible" data"""
        clients = [] # TODO: clients should be filled by a QSqlQuery
        for client in clients:
            for month in range(self.months_before, self.months_afther):
                pass
                # TODO: I need to check if there is a payment for client in the
                # date range date(year, month, 1) .. datetime(year, month+1, 1)
                # where year it's this (+/-1) year
                should_pay = not_in_database = lambda a,b: None # fake functions
                if should_pay(client, month) and not_in_database(client, month):
                    pass # do an insert
        self.emit(SIGNAL("layoutChanged()"))