from datetime import datetime
import pickle
from gui.trial_detail_widget import EchoTrialDetailsWidget
from lib.racer_driver import execute_trial
from lib.trial_jobs import TrialJob, EchoTrialJob

__author__ = 'daniel'
from gui.experiment_combo_box import ExperimentComboBox
from gui.new_trial_dialog import NewTrialDialog
from gui.sqlalchemy_table_model import SQLAlchemyTableModel
from models.trial import Trial
from models.experiment import Experiment

from rq import Connection, Queue
from redis import Redis




from PyQt4 import QtGui, QtCore
from gui.data_source_model import DataSourceModel
from gui.plot_style_edit_dialog import PlotStyleEditDialog
from gui.plotter_widget import PlotterWidget



from lib.timing_data import TimingData
from lib.plot import Plot
from lib.box_test import BoxTest

class FeasibilityTab(QtGui.QWidget):

    longer_plot = None
    shorter_plot = None

    def __init__(self, session = None, parent = None):
        super(FeasibilityTab, self).__init__(parent)
        self.session = session

        self.current_trial = None

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)


        ####################
        ## ANALYSIS
        ####################
        self.analysis_box = QtGui.QGroupBox(self, title="Analysis")
        self.layout.addWidget(self.analysis_box,1,0, 1, 1)
        self.analysis_box_layout = QtGui.QGridLayout(self.analysis_box)

        self.analysis_box.setLayout(self.analysis_box_layout)

        ###  shorter trial box
        self.analysis_data_source_shorter = QtGui.QGroupBox("Shorter Trial")
        self.analysis_data_source_shorter_layout = QtGui.QGridLayout()
        self.analysis_data_source_shorter.setLayout(self.analysis_data_source_shorter_layout)

        self.shorter_trial_label = QtGui.QLabel("<b>Trial:</b>")
        self.shorter_trial = QtGui.QLabel("[select on experiment tab]")
        self.analysis_data_source_shorter_layout.addWidget(self.shorter_trial_label, 0, 0)
        self.analysis_data_source_shorter_layout.addWidget(self.shorter_trial, 0, 1)

        self.shorter_trial_color_label = QtGui.QLabel("<b>Color:</b>")
        self.shorter_trial_color = QtGui.QLabel()
        self.analysis_data_source_shorter_layout.addWidget(self.shorter_trial_color_label, 1, 0)
        self.analysis_data_source_shorter_layout.addWidget(self.shorter_trial_color, 1, 1)


        self.shorter_trial_bins_label = QtGui.QLabel("<b>Bins:</b>")
        self.shorter_trial_bins = QtGui.QLabel()
        self.analysis_data_source_shorter_layout.addWidget(self.shorter_trial_bins_label, 2, 0)
        self.analysis_data_source_shorter_layout.addWidget(self.shorter_trial_bins, 2, 1)


        self.shorter_trial_edit = QtGui.QPushButton("Edit")
        self.shorter_trial_edit.setEnabled(False)
        self.shorter_trial_edit.released.connect(self.edit_shorter_trial)
        self.analysis_data_source_shorter_layout.addWidget(self.shorter_trial_edit, 3, 0, 1, 2)

        self.analysis_box_layout.addWidget(self.analysis_data_source_shorter, 0, 0)



        ###  longer trial box
        self.analysis_data_source_longer = QtGui.QGroupBox("Longer Trial")
        self.analysis_data_source_longer_layout = QtGui.QGridLayout()
        self.analysis_data_source_longer.setLayout(self.analysis_data_source_longer_layout)

        self.longer_trial_label = QtGui.QLabel("<b>Trial:</b>")
        self.longer_trial = QtGui.QLabel("[select on experiment tab]")
        self.analysis_data_source_longer_layout.addWidget(self.longer_trial_label, 0, 0)
        self.analysis_data_source_longer_layout.addWidget(self.longer_trial, 0, 1)

        self.longer_trial_color_label = QtGui.QLabel("<b>Color:</b>")
        self.longer_trial_color = QtGui.QLabel()
        self.analysis_data_source_longer_layout.addWidget(self.longer_trial_color_label, 1, 0)
        self.analysis_data_source_longer_layout.addWidget(self.longer_trial_color, 1, 1)


        self.longer_trial_bins_label = QtGui.QLabel("<b>Bins:</b>")
        self.longer_trial_bins = QtGui.QLabel()
        self.analysis_data_source_longer_layout.addWidget(self.longer_trial_bins_label, 2, 0)
        self.analysis_data_source_longer_layout.addWidget(self.longer_trial_bins, 2, 1)


        self.longer_trial_edit = QtGui.QPushButton("Edit")
        self.longer_trial_edit.setEnabled(False)
        self.longer_trial_edit.released.connect(self.edit_longer_trial)
        self.analysis_data_source_longer_layout.addWidget(self.longer_trial_edit, 3, 0, 1, 2)



        self.analysis_box_layout.addWidget(self.analysis_data_source_longer, 0, 1)



        #### configuration
        self.analysis_config = QtGui.QGroupBox("Analysis Configuration")
        self.analysis_config_layout = QtGui.QGridLayout()

        self.analysis_config.setLayout(self.analysis_config_layout)

        self.analysis_type_label = QtGui.QLabel("Analysis Method")
        self.analysis_type = QtGui.QComboBox()
        self.analysis_type.addItem("Box Test")
        self.analysis_config_layout.addWidget(self.analysis_type_label, 0, 0)
        self.analysis_config_layout.addWidget(self.analysis_type, 0, 1)


        self.analysis_lower_quantile_label = QtGui.QLabel("Lower Quantile")
        self.analysis_lower_quantile = QtGui.QLineEdit(text="6")
        self.analysis_config_layout.addWidget(self.analysis_lower_quantile_label, 1, 0)
        self.analysis_config_layout.addWidget(self.analysis_lower_quantile, 1, 1)

        self.analysis_upper_quantile_label = QtGui.QLabel("Upper Quantile")
        self.analysis_upper_quantile = QtGui.QLineEdit(text="6.5")
        self.analysis_config_layout.addWidget(self.analysis_upper_quantile_label, 2, 0)
        self.analysis_config_layout.addWidget(self.analysis_upper_quantile, 2, 1)



        self.analysis_perfom_button = QtGui.QPushButton("Perform Analysis")
        self.analysis_perfom_button.released.connect(self.perform_analysis)
        self.analysis_config_layout.addWidget(self.analysis_perfom_button, 3, 0, 1, 2)

        self.analysis_box_layout.addWidget(self.analysis_config, 0,2)

        # Reset
        self.reset_plot_button = QtGui.QPushButton("Reset Plot")
        self.reset_plot_button.released.connect(self.reset_plot)
        self.analysis_box_layout.addWidget(self.reset_plot_button, 1, 0,1, 2)

        ## Result
        self.analysis_result_box = QtGui.QGroupBox("Result")
        self.analysis_result_box_layout = QtGui.QGridLayout()
        self.analysis_result_box.setLayout(self.analysis_result_box_layout)

        self.analysis_result = QtGui.QLabel()
        self.analysis_result_box_layout.addWidget(self.analysis_result, 0, 0)

        self.analysis_box_layout.addWidget(self.analysis_result_box, 1,2, 1, 1)


        ### PLotter
        self.plotter = PlotterWidget(self)
#        self.plotter.set_data_source_model(self.data_source_model)
        self.analysis_box_layout.addWidget(self.plotter, 2,0,1,3)

#        self.data_source_model.rowsInserted.connect(self.plotter.update_plot)

    def reset_plot(self):
        self.shorter_trial.setText("[seect on experiment tab]")
        self.shorter_trial_color.setText("")
        self.shorter_trial_bins.setText("")

        self.longer_trial.setText("[select on experiment tab]")
        self.longer_trial_color.setText("")
        self.longer_trial_bins.setText("")

        self.shorter_trial_edit.setEnabled(False)
        self.longer_trial_edit.setEnabled(False)

        self.plotter.reset()

    def edit_shorter_trial(self):
        dialog = PlotStyleEditDialog(plot = self.shorter_plot)
        dialog.accepted.connect(self.update_plot_settings_view)
        dialog.exec()

    def edit_longer_trial(self):
        dialog = PlotStyleEditDialog(plot = self.longer_plot)
        dialog.accepted.connect(self.update_plot_settings_view)
        dialog.exec()

    def update_plot_settings_view(self):
        self.plotter.update_plot()

        if self.shorter_plot is not None:
            self.shorter_trial_bins.setText(str(self.shorter_plot.bins))
            self.shorter_trial_color.setText(str(self.shorter_plot.color))

        if self.longer_plot is not None:
            self.longer_trial_bins.setText(str(self.longer_plot.bins))
            self.longer_trial_color.setText(str(self.longer_plot.color))




    def set_shorter(self, trial):
        self.shorter_trial.setText(trial.name)
        self.shorter_trial_data = trial

        self.shorter = TimingData()
        self.shorter.parse_csv(self.shorter_trial_data.result)
        self.shorter_plot = Plot(self.shorter)
        self.shorter_plot.color = 'blue'
        self.shorter_plot.label = trial.name
        self.plotter.add_plot(self.shorter_plot)

        self.shorter_trial_edit.setEnabled(True)
        self.update_plot_settings_view()

    def set_longer(self, trial):
        self.longer_trial.setText(trial.name)
        self.longer_trial_data = trial

        self.longer = TimingData()
        self.longer.parse_csv(self.longer_trial_data.result)
        self.longer_plot = Plot(self.longer)
        self.longer_plot.color = 'red'
        self.longer_plot.label = trial.name

        self.plotter.add_plot(self.longer_plot)

        self.longer_trial_edit.setEnabled(True)
        self.update_plot_settings_view()


    def perform_analysis(self):
        self.plotter.update_plot()
        box_test = BoxTest(self.shorter, self.longer, float(self.analysis_lower_quantile.text()), float(self.analysis_upper_quantile.text()))
        res = box_test.perform()
        self.analysis_result.setText("Are the two distributions distinct?  " + str(res))
        x_box = box_test.x_box()
        y_box = box_test.y_box()

        self.plotter.plot_canvas.draw_rectangle(x_box[0], 0, x_box[1] - x_box[0], 1e7, fg_color=self.shorter_plot.color, edge_color="black")
        self.plotter.plot_canvas.draw_rectangle(y_box[0], 0, y_box[1] - y_box[0], 1e7, fg_color=self.longer_plot.color, edge_color="black")


#    def event_open_data_source_edit(self, index):
#        dialog = EditDataSourceDialog(index.data(QtCore.Qt.EditRole), self)
#        dialog.accepted.connect(self.event_data_source_edited)
#        dialog.exec()

    def event_data_source_edited(self):
        self.data_source_table.resizeColumnsToContents()
        self.plotter.update_plot()

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


