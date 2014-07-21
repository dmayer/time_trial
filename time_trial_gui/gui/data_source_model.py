from PyQt4 import QtGui, QtCore, Qt

class DataSourceModel(QtCore.QAbstractTableModel):

    def __init__(self, parent = None, *args):
        QtCore.QAbstractTableModel.__init__(self, parent, *args)
        self.data_store = []
        self.header_vals =  ["File Name", "Label", "Color", "Bins", "Style"]
        self.default_colors = ["red", "blue", "green", "black"]

    def rowCount(self, parent):
        return len(self.data_store)

    def columnCount(self, parent):
        return 5

    def headerData(self, p_int, Qt_Orientation, int_role=None):
        if int_role == QtCore.Qt.DisplayRole and Qt_Orientation == QtCore.Qt.Horizontal:
            return self.header_vals[p_int]
        return QtCore.QAbstractTableModel.headerData(self, p_int, Qt_Orientation, int_role)


    def data(self, index, role):
        if not index.isValid():
            return None
        if role == QtCore.Qt.EditRole:
            item = self.data_store[index.row()]
            return item
        elif role != QtCore.Qt.DisplayRole:
            return None
        else:
            item = self.data_store[index.row()]
            if index.column() == 0:
                return item.timing_data.file_name
            elif index.column() == 1:
                return item.label
            elif index.column() == 2:
                return item.color
            elif index.column() == 3:
                return item.bins
            elif index.column() == 4:
                return item.style_name()

    def add_data(self, item):
#        index = self.createIndex(len(self.data_store), 0)
        self.beginInsertRows(QtCore.QModelIndex(), len(self.data_store), len(self.data_store))
        self.data_store.append(item)
        item.color = self.default_colors[len(self.data_store)-1]
#        self.dataChanged.emit(index, index)
        self.endInsertRows()
