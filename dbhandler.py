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
from PyQt4.QtGui import QItemDelegate, QDateEdit#, QCheckBox

QSQ = QSqlQuery
class QSqlQuery(QSQ):
    def exec_(self, DEBUG=False):
        ret = QSQ.exec_(self)
        if not DEBUG:
            return ret
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
        self.machine = query.value(
                record.indexOf('clients_machine')).toString()
        self.selldate = query.value(
                record.indexOf('clients_selldate')).toDate()
        self.expected_datepayd = query.value(
                record.indexOf('expected_datepayd')).toDate()
        self.effective_datepayd = query.value(
                record.indexOf('effective_datepayd')).toDate()
        self.payed = not query.isNull(record.indexOf('effective_datepayd'))

class EditableCheckboxDate(QItemDelegate):
    format = 'dd MMMM yyyy'
    def createEditor(self, parent, option, index):
        """Create the Date edit widget to set the payment date"""
        qde = QDateEdit(parent)
        qde.setDisplayFormat(self.format)
        qde.setCalendarPopup(True)
        return qde

    def setEditorData(self, editor, index):
        """Set the "default" editor data (from the index)"""
        editor.setDate(QDate.fromString(index.data().toString(), self.format))

    def setModelData(self, editor, model, index):
        """Tell the model to set the new data taken from the editor"""
        model.setData(index, editor.date().toString(self.format), Qt.EditRole)
        #model.setData(index, Qt.Checked, Qt.CheckStateRole) # do I need this?

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
        self.update_db_content()

    def __del__(self):
        self._db.close()

    def rowCount(self, index=None):
        """Tell the view how many months (rows) the model have"""
        # pylint: disable-msg=C0103
        assert not index.isValid()
        return self.months_before + self.months_afther

    def columnCount(self, index=None):
        """Tell the view how many machines (columns) the model have"""
        # pylint: disable-msg=C0103
        assert not index.isValid()
        query = QSqlQuery('SELECT COUNT(*) FROM clients', self._db)
        if not query.exec_():
            raise StandardError('SYNTAX ERROR')
        if not query.first():
            raise StandardError('No table found (or no elements)')
        return query.value(0).toInt()[0]

    def data(self, index, role=None):
        """return a QVariant saying if exists a payment at index.(row|column)"""
        if not index.isValid() or role not in (Qt.DisplayRole,
                Qt.CheckStateRole):
            return QVariant()
        #self.update_db_content()
        # find the month from the row number
        month_year = QDate().fromString(self.headerData(index.row(),
                Qt.Vertical, role).toString(), 'MMMM yyyy')
        month = month_year.month()
        year = month_year.year()
        # find the client from the column number
        header_infos = self.headerData(index.column(), Qt.Horizontal,
                role).toString().split('\n')
        client = header_infos[0]
        machine = header_infos[1]
        selldate = QDate.fromString(header_infos[2], 'd MMMM yyyy')
        deltamonth = int(header_infos[3][5:-5]) # [len('Ogni '):-len(' mesi')]
        anticiped = header_infos[4][10:-6] == 'anti' # 'Pagamento ':-'cipato'
        query = QSqlQuery('SELECT expected_datepayd, effective_datepayd FROM '
                'payments WHERE clients_client = :client AND clients_machine = '
                ':machine AND clients_selldate = :selldate AND '
                'expected_datepayd BETWEEN :datebefore AND :dateafter',
                self._db)
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
        if not query.first():
            return QVariant()
        expected_datepayd = query.value(0).toDate()
        payed = not query.isNull(1)
        effective_datepayd = query.value(1).toDate()
        if role == Qt.CheckStateRole:
            return QVariant(Qt.Checked if payed else Qt.Unchecked)
        else: # DisplayRole
            date = effective_datepayd if payed else expected_datepayd
            return QVariant(date.toString('d MMMM yyyy'))

    def headerData(self, section, orientation, role=None):
        """Generate the months on the rows and the clients on the columns"""
        # pylint: disable-msg=C0103
        if role not in (Qt.DisplayRole, Qt.CheckStateRole):
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
            return QVariant(QDate.currentDate().addMonths(
                    section - self.months_before).toString('MMMM yyyy'))

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

    def setData(self, index, value, role=None):
        if not index.isValid() or role not in (Qt.EditRole, Qt.CheckStateRole):
            return False
        print 'TODO setData(%s, %s, %s)' % (index, value, role)
        self.emit(SIGNAL("dataChanged()"), index, index)
        return True

    def flags(self, index):
        """A valid index is selectable, enabled and maybe editable"""
        if not index.isValid():
            return Qt.NoItemFlags
        default_flags = QAbstractTableModel.flags(self, index)
        if not self.data(index, Qt.DisplayRole).isValid():
            return default_flags
        return default_flags | Qt.ItemIsEditable | Qt.ItemIsUserCheckable

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
            while payments_date < datebefore: # ignora date non visibili
                payments_date = payments_date.addMonths(client.deltamonth)
            while payments_date < dateafter:
                query2 = QSqlQuery('SELECT effective_datepayd FROM payments '
                        'WHERE clients_client = :client AND clients_machine = '
                        ':machine AND clients_selldate = :selldate AND '
                        'expected_datepayd = :expected_datepayd', self._db)
                query2.bindValue(':client', QVariant(client.client))
                query2.bindValue(':machine', QVariant(client.machine))
                query2.bindValue(':selldate', QVariant(client.selldate))
                query2.bindValue(':expected_datepayd', QVariant(payments_date))
                if not query2.exec_():
                    raise StandardError('SYNTAX ERROR')
                if not query2.first():
                    query3 = QSqlQuery('INSERT INTO payments (clients_client, '
                            'clients_machine, clients_selldate, '
                            'expected_datepayd) VALUES (:client, :machine, '
                            ':selldate, :expected_datepayd)', self._db)
                    query3.bindValue(':client', QVariant(client.client))
                    query3.bindValue(':machine', QVariant(client.machine))
                    query3.bindValue(':selldate', QVariant(client.selldate))
                    query3.bindValue(':expected_datepayd',
                            QVariant(payments_date))
                    if not query3.exec_():
                        raise StandardError('SYNTAX ERROR')
                payments_date = payments_date.addMonths(client.deltamonth)
        self.emit(SIGNAL("layoutChanged()"))
