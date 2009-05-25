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
from PyQt4.QtGui import QItemDelegate, QCheckBox
from datetime import date, datetime

if False:
    QSQ = QSqlQuery
    class QSqlQuery(QSQ):
        def exec_(self):
            ret = QSQ.exec_(self)
            if ret:
                r = unicode(self.executedQuery())
                for k, v in self.boundValues().items():
                    r = r.replace(unicode(k), '%r' % unicode(v.toPyObject()))
                print '[OK|%s]' % (r, )
            else:
                print '[ER|%s|%s]' % (self.lastQuery(), self.lastError().text())
            return ret

class Client(object):
    def __init__(self, query):
        record = query.record()
        self.client = query.value(record.indexOf('client')).toString()
        self.machine = query.value(record.indexOf('machine')).toString()
        self.selldate = query.value(record.indexOf('selldate')).toDate()
        self.deltamonth = query.value(record.indexOf('deltamonth')).toInt()[0]
        self.anticiped = query.value(record.indexOf('anticiped')).toBool()

class Payment(object):
    def __init__(self, query):
        record = query.record()
        self.client = query.value(record.indexOf('clients_client')).toString()
        self.machine = query.value(record.indexOf('clients_machine')).toString()
        self.selldate = query.value(record.indexOf('clients_selldate')).toDate()
        self.datepayd = query.value(record.indexOf('datepayd')).toDate()
        self.payed = query.value(record.indexOf('payed')).toBool()

class EditableCheckboxDate(QItemDelegate):
    # const QStyleOptionViewItem & option, const QModelIndex &index
    def createEditor(self, parent, option, index):
        return QCheckBox(parent)

    #QWidget *editor, const QModelIndex &index
    def setEditorData(self, editor, index):
        # piglia i dati dal model di index e modifica editor
        editor.setText('data')
        editor.setChecked(True)

    # QWidget *editor, QAbstractItemModel *model, const QModelIndex &index
    def setModelData(self, editor, model, index):
        pass # scrivi nel model

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

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
        if not query.exec_():
            raise StandardError('SYNTAX ERROR')
        if not query.first():
            raise StandardError('No table found (or no elements)')
        return query.value(0).toInt()[0]

    def data(self, model_index, role=None):
        """TODO: use model_index to tell the view what the hell it's inside"""
        if role != Qt.DisplayRole:
            return QVariant()
        # find the month from the row number
        month_year = QDate().fromString(self.headerData(model_index.row(),
                Qt.Vertical, role).toString(), 'MMMM yyyy')
        month = month_year.month()
        year = month_year.year()
        # find the client from the column number
        client_machine = unicode(self.headerData(model_index.column(),
                Qt.Horizontal, role).toString()).split('\n')
        client = client_machine[0]
        machine = client_machine[1]
        selldate = QDate.fromString(client_machine[2], 'd MMMM yyyy')
        deltamonth = int(client_machine[3][5:-5]) # [len('Ogni '):-len(' mesi')]
        anticiped = client_machine[4][10:-6] == 'anti' # 'Pagamento ':-'cipato'
        query = QSqlQuery('SELECT datepayd, payed FROM payments WHERE '
                'clients_client = :client AND clients_machine = :machine AND '
                'clients_selldate = :selldate AND datepayd BETWEEN :datebefore '
                'AND :dateafter', self._db)
        query.bindValue(':client', QVariant(client))
        query.bindValue(':machine', QVariant(machine))
        query.bindValue(':selldate', QVariant(selldate))
        # primo giorno del mese
        d = QDate(year, month, 1)
        query.bindValue(':datebefore', QVariant(d))
        # ultimo giorno del mese
        query.bindValue(':dateafter', QVariant(d.addMonths(1).addDays(-1)))
        if not query.exec_():
            raise StandardError('SYNTAX ERROR')
        while query.next():
            datepayd = query.value(0).toDate()
            payed = query.value(1).toBool()
            return QVariant('%s%s' % (datepayd.toString('d MMMM yyyy'),
                    'Pagato' if payed else 'Da pagare'))
        return QVariant()

    def headerData(self, section, orientation, role=None):
        """Generate the months on the rows and the clients on the columns"""
        # pylint: disable-msg=C0103
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            query = QSqlQuery('SELECT client, machine, selldate, deltamonth, '
                    'anticiped FROM clients ORDER BY client, machine, '
                    'selldate', self._db)
            if not query.exec_():
                raise StandardError('SYNTAX ERROR')
            if not query.first():
                raise StandardError("Non c'e' manco un risultato?")
            if not query.seek(section):
                raise StandardError('Not enough elements into the table')
            client = Client(query)
            return QVariant('%s\n%s\n%s\nOgni %s mesi\nPagamento %scipato' % (
                    client.client, client.machine,
                    client.selldate.toString('d MMMM yyyy'),
                    client.deltamonth, 'anti' if client.anticiped else 'posti'))
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
        query = QSqlQuery('INSERT INTO clients (client, machine, selldate, '
                'deltamonth, anticiped) VALUES (:client, :machine, :selldate, '
                ':deltamonth, :anticiped)''', self._db)
        query.bindValue(':client', QVariant(client))
        query.bindValue(':machine', QVariant(machine))
        query.bindValue(':selldate', QVariant(selldate))
        query.bindValue(':deltamonth', QVariant(deltamonth))
        query.bindValue(':anticiped', QVariant(anticiped))
        if not query.exec_():
            raise StandardError('SYNTAX ERROR')
        self.update_db_content()

    def update_db_content(self):
        """Populate the payment table ensuring all "visible" data"""
        today = QDate.currentDate()
        first_month_day = QDate(today.year(), today.month(), 1)
        datebefore = first_month_day.addMonths(-self.months_before)
        dateafter = first_month_day.addMonths(self.months_afther)
        query = QSqlQuery('SELECT client, machine, selldate, deltamonth, '
                'anticiped FROM clients', self._db)
        if not query.exec_():
            raise StandardError('SYNTAX ERROR')
        while query.next():
            client = Client(query)
            payments_date = client.selldate.addMonths(0 if client.anticiped
                    else client.deltamonth)
            while payments_date < datebefore:
                # ignora date non visibili
                payments_date = payments_date.addMonths(client.deltamonth)
            while payments_date < dateafter:
                query2 = QSqlQuery('SELECT payed FROM payments WHERE '
                        'clients_client = :clients_client AND clients_machine '
                        '= :clients_machine AND clients_selldate = '
                        ':clients_selldate AND datepayd = :datepayd', self._db)
                query2.bindValue(':clients_client', QVariant(client.client))
                query2.bindValue(':clients_machine', QVariant(client.machine))
                query2.bindValue(':clients_selldate', QVariant(client.selldate))
                query2.bindValue(':datepayd', QVariant(payments_date))
                if not query2.exec_():
                    raise StandardError('SYNTAX ERROR')
                if not query2.first():
                    query3 = QSqlQuery('INSERT INTO payments (clients_client, '
                            'clients_machine, clients_selldate, datepayd, '
                            'payed) VALUES (:clients_client, :clients_machine, '
                            ':clients_selldate, :datepayd, :payed)', self._db)
                    query3.bindValue(':clients_client', QVariant(client.client))
                    query3.bindValue(':clients_machine',
                            QVariant(client.machine))
                    query3.bindValue(':clients_selldate',
                            QVariant(client.selldate))
                    query3.bindValue(':datepayd', QVariant(payments_date))
                    query3.bindValue(':payed', QVariant(False))
                    if not query3.exec_():
                        raise StandardError('SYNTAX ERROR')
                payments_date = payments_date.addMonths(client.deltamonth)
        self.emit(SIGNAL("layoutChanged()"))
