from PyQt4.QtCore import QVariant

__author__ = 'daniel'

from PyQt4 import QtGui, QtCore, Qt

## adapted from https://gist.github.com/harvimt/4699169 by Mark Harviston

class SQLAlchemyTableModel(QtCore.QAbstractTableModel):

    def __init__(self, session, query, columns,  parent = None):
        QtCore.QAbstractTableModel.__init__(self, parent)
        self.session = session
        self.query = session.query(query)
        self.columns = columns
        self.results = None
        self.count = None
        self.sort = None
        self.filter = None
        self.refresh()

    def rowCount(self, parent):
        return self.count

    def refresh(self):
        self.layoutAboutToBeChanged.emit()

        q = self.query
        if self.sort is not None:
            order, col = self.sort
            col = self.columns[col][1]
            if order == Qt.DescendingOrder:
                col = col.desc()
        else:
            col = None

        if self.filter is not None:
            q = q.filter(self.filter)

        q = q.order_by(col)

        self.results = q.all()
        self.count = q.count()
        self.layoutChanged.emit()

    def columnCount(self, parent):
        return len(self.columns)

    def headerData(self, col, Qt_Orientation, int_role=None):
        if int_role == QtCore.Qt.DisplayRole and Qt_Orientation == QtCore.Qt.Horizontal:
            return self.columns[col][0]
        return QtCore.QAbstractTableModel.headerData(self, col, Qt_Orientation, int_role)


    def data(self, index, role):
        if not index.isValid():
            return None
        if role == QtCore.Qt.EditRole:
            return self.results[index.row()]
        elif role != QtCore.Qt.DisplayRole:
            return None
        else:
            row = self.results[index.row()]
            name = self.columns[index.column()][2]
            return str(getattr(row, name))

    def sort(self, col, order):
        self.sort = order, col
        self.refresh()

    def setFilter(self, filter):
        self.filter = filter
        self.refresh()





