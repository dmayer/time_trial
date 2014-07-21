__author__ = 'daniel'

import logging

from PyQt4 import QtGui
from gui.data_source_model import DataSourceModel
from gui.plotter_widget import PlotterWidget



from lib.timing_data import TimingData
from lib.plot import Plot

class PlotterTab(QtGui.QWidget):

    def __init__(self, parent = None):
        super(PlotterTab, self).__init__(parent)
        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        # data sources
        self.data_box = QtGui.QGroupBox(self, title="Data Sources")
        self.layout.addWidget(self.data_box,0,0)

        data_box_layout = QtGui.QGridLayout(self.data_box)
        self.data_box.setLayout(data_box_layout)

        self.data_source_model = DataSourceModel()
        self.data_source_table = QtGui.QTableView()
        self.data_source_table.setModel(self.data_source_model)
        self.data_source_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.data_source_table.activated.connect(self.event_open_data_source_edit)

        data_box_layout.addWidget(self.data_source_table, 0, 0)


        self.plotter = PlotterWidget(self)
        self.plotter.set_data_source_model(self.data_source_model)
        self.layout.addWidget(self.plotter, 1,0,1,2)

        self.data_source_model.rowsInserted.connect(self.plotter.update_plot)


        # main buttons
        add_file_button = QtGui.QPushButton(self.data_box)
        add_file_button.setText("Add File")

        add_file_button.released.connect(self.event_show_select_file_dialog)
        self.layout.addWidget(add_file_button,0,1)

    def event_open_data_source_edit(self, index):
        dialog = EditDataSourceDialog(index.data(QtCore.Qt.EditRole), self.main_widget)
        dialog.accepted.connect(self.event_data_source_edited)
        dialog.exec()

    def event_data_source_edited(self):
        self.data_source_table.resizeColumnsToContents()
        self.update_plot()

    def event_show_select_file_dialog(self):
        file_dialog = QtGui.QFileDialog()
        file_dialog.setAcceptMode(QtGui.QFileDialog.AcceptOpen)
        filters = [ "PEM Files (*.pem)", "Any files (*)" ]
        #        file_dialog.fileSelected.connect(self.event_file_selected)
        file_dialog.filesSelected.connect(self.event_files_selected)
        file_dialog.setFileMode(QtGui.QFileDialog.ExistingFiles)
        file_dialog.exec()

    def event_files_selected(self, file_names):
        print(file_names)
        for f in file_names:
            self.event_file_selected(f)

    def event_file_selected(self,file_name):
        new_data = TimingData()
        new_data.load_from_csv(file_name)
        new_plot = Plot(new_data)
        self.data_source_model.add_data(new_plot)
        self.data_source_table.resizeColumnsToContents()

        #data = parse_csv(file_name)
        #self.plot_canvas.add_plot(data, 200, [min(data), 26*1000*1000], "100 micros", 'red')
        #self.plot_canvas.update_figure()

    def add_data_row(self, data):
        pass

