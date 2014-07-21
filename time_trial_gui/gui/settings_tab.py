from PyQt4 import QtGui
from PyQt4 import QtCore
from gui.racer_edit_dialog import RacerEditDialog
from gui.sqlalchemy_table_model import SQLAlchemyTableModel
from models.racer import Racer
__author__ = 'daniel'


class SettingsTab(QtGui.QWidget):

    def __init__(self,  parent = None, session = None):
        super(SettingsTab, self).__init__(parent)
        self.session = session
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        racers_box = QtGui.QGroupBox("Racer Configuration")
        racers_box_layout = QtGui.QGridLayout()
        racers_box.setLayout(racers_box_layout)
        self.layout.addWidget(racers_box,0,0)

        self.racers_table = QtGui.QTableView(self)
        self.racers_table.doubleClicked.connect(self.edit_racer)
        self.racers_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.racers_table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.racers_table_model = SQLAlchemyTableModel(session, Racer, [
            ('name', Racer.name, 'name'),
            ('hostname', Racer.hostname, 'hostname'),
            ('location', Racer.location, 'location')])


        self.racers_table_selection_model  = QtGui.QItemSelectionModel(self.racers_table_model)
        self.racers_table.setModel(self.racers_table_selection_model.model())
        self.racers_table.setSelectionModel(self.racers_table_selection_model)


        racers_box_layout.addWidget(self.racers_table,0,0, 1, 3)

        racers_add_button = QtGui.QPushButton("Add")
        racers_add_button.released.connect(self.add_racer)
        racers_box_layout.addWidget(racers_add_button, 1, 0)

        racers_edit_button = QtGui.QPushButton("Edit")
        racers_edit_button.released.connect(self.edit_racer)
        racers_box_layout.addWidget(racers_edit_button, 1, 1)


        racers_delete_button = QtGui.QPushButton("Delete")
        racers_delete_button.released.connect(self.delete_racer)
        racers_box_layout.addWidget(racers_delete_button, 1, 2)

    def edit_racer(self):
        racer = self.racers_table_selection_model.currentIndex().data(QtCore.Qt.EditRole)
        dialog = RacerEditDialog(racer)
        dialog.exec()
        self.session.add(racer)
        self.session.commit()
        self.racers_table_model.refresh()


    def add_racer(self):
        racer = Racer()
        dialog = RacerEditDialog(racer)
        dialog.exec()
        self.session.add(racer)
        self.session.commit()
        self.racers_table_model.refresh()

    def delete_racer(self):
        self.session.delete(self.racers_table_selection_model.currentIndex().data(QtCore.Qt.EditRole))
        self.session.commit()
        self.racers_table_model.refresh()





