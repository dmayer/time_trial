from gui.plot_settings_dialog import PlotSettingsDialog

__author__ = 'daniel'

from gui.histogram import Histogram
from PyQt4 import QtGui, QtCore

from lib.plot_settings import PlotSettings


class PlotterWidget(QtGui.QWidget):

    plots = []

    def __init__(self, parent=None):
        super(PlotterWidget, self).__init__(parent)

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)


        self.plot_settings = PlotSettings()

        #plot_canvas = MyStaticMplCanvas(self.main_widget, width=5, height=4, dpi=100)
        self.plot_canvas = Histogram(self, width=9, height=3, dpi=100, settings=self.plot_settings)
        self.plot_canvas.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.plot_canvas.customContextMenuRequested.connect(self.display_context_menu)



        self.layout.addWidget(self.plot_canvas,0,0)

#        self.plot_settings_button = QtGui.QPushButton("Plot Settings")
        self.plot_settings_dialog = PlotSettingsDialog(plot_settings=self.plot_settings)
        self.plot_settings_dialog.accepted.connect(self.apply_plot_settings)
#        self.plot_settings_button.released.connect(self.plot_settings_dialog.exec)
#        self.layout.addWidget(self.plot_settings_button)
        self.setToolTip("Right click for options.")

    def display_context_menu(self, pos):
        self. menu = QtGui.QMenu()

        self.edit_action = self.menu.addAction("Edit Plot Settings")
        self.edit_action.triggered.connect(self.plot_settings_dialog.exec)

        self.pdf_action = self.menu.addAction("Save as PDF")
        self.pdf_action.triggered.connect(self.save_as_pdf)

        self.menu.popup(self.mapToGlobal(pos))

    def save_as_pdf(self):
        dialog = QtGui.QFileDialog(self)
        dialog.setDefaultSuffix("pdf")
        dialog.setWindowTitle("Save Figure as PDF...")
        dialog.setAcceptMode(QtGui.QFileDialog.AcceptSave)
        dialog.setFileMode(QtGui.QFileDialog.AnyFile)
        dialog.fileSelected.connect(self.save_as_pdf_to_file)
        dialog.exec()


    def save_as_pdf_to_file(self, filename):
        self.plot_canvas.fig.set_size_inches(9,3)
        pdf = self.plot_canvas.fig.savefig(filename=filename, format="pdf")

    def apply_plot_settings(self):
        self.plot_canvas.axes.set_xlim(self.plot_settings.x_minimum, self.plot_settings.x_maximum)
        self.plot_canvas.axes.set_ylim(self.plot_settings.y_minimum, self.plot_settings.y_maximum)
        self.update_plot()

    def set_data_source_model(self, model):
        self.data_source_model = model

    def add_plot(self, plot):
        self.plots.append(plot)
        self.update_plot()

    def reset(self):
        self.plots.clear()
        self.update_plot()


    def update_plot(self):
        self.plot_canvas.clear()
        for d in self.plots:
            self.plot_canvas.add_plot(d)

        self.plot_canvas.axes.set_xlim(self.plot_settings.x_minimum, self.plot_settings.x_maximum)
        self.plot_canvas.axes.set_ylim(self.plot_settings.y_minimum, self.plot_settings.y_maximum)
        self.plot_canvas.update_figure()




