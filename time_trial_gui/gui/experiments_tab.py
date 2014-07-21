from PyQt4 import QtGui,QtCore
from datetime import datetime
from rq.job import Job
from redis import Redis
from rq import Queue
from gui.experiment_combo_box import ExperimentComboBox
from gui.new_trial_dialog import NewTrialDialog
from gui.sqlalchemy_table_model import SQLAlchemyTableModel
from gui.trial_detail_widget import EchoTrialDetailsWidget, HttpTrialDetailsWidget, RacerDetailsWidget, \
    TrialStatusWidget
from lib.racer_driver import execute_trial
from lib.trial_jobs import EchoTrialJob, HTTPTrialJob

from models.experiment import Experiment
from models.trial import Trial

__author__ = 'daniel'

class ExperimentsTab(QtGui.QWidget):




    def __init__(self, session = None, parent = None):
        super(ExperimentsTab, self).__init__(parent)
        self.session = session
        self.redis_conn = Redis()


        self.current_experiment = None


        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        # experiments
        self.experiment_box = QtGui.QGroupBox(self, title="Experiments")
        self.experiment_box.setSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)
        self.layout.addWidget(self.experiment_box,0,0)
        self.experiment_box_layout = QtGui.QGridLayout(self.experiment_box)
        self.experiment_box.setLayout(self.experiment_box_layout)


        self.experiment_list = ExperimentComboBox(session = session)
        self.experiment_list.currentIndexChanged.connect(self.update_current_experiment)
        self.experiment_box_layout.addWidget(self.experiment_list, 0, 0)

        self.new_experiment_button = QtGui.QPushButton("New Experiment")
        self.new_experiment_button.released.connect(self.new_experiment)
        self.experiment_box_layout.addWidget(self.new_experiment_button, 0, 1)


        # data sources
        self.data_box = QtGui.QGroupBox(self, title="Trials for this Experiment")
        self.data_box.setSizePolicy(QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Expanding )
        self.layout.addWidget(self.data_box,1,0, 1, 1)

        self.data_box_layout = QtGui.QGridLayout(self.data_box)
        self.data_box.setLayout(self.data_box_layout)





        self.trial_table = QtGui.QTableView(self)
        #        self.trial_table.doubleClicked.connect(self.edit_racer)
        #        self.trial_table.activated.connect(self.update_current_trial)
        self.trial_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.trial_table_model = SQLAlchemyTableModel(session, Trial, [
            ('Type', Trial.discriminator, 'discriminator'),
            ('Name', Trial.name, 'name'),
            ('Reps', Trial.reps, 'reps'),
            ('Start', Trial.start_date, 'start_date'),
            ('End', Trial.end_date, 'end_date')
        ])

        self.trial_table.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.trial_table.customContextMenuRequested.connect(self.display_context_menu)
        self.trial_table.doubleClicked.connect(self.edit_trial)
        self.trial_table.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)


        self.trial_table_selection_model  = QtGui.QItemSelectionModel(self.trial_table_model)
        self.trial_table.setModel(self.trial_table_selection_model.model())
        self.trial_table.setSelectionModel(self.trial_table_selection_model)
        self.trial_table_selection_model.selectionChanged.connect(self.update_current_trial)


        self.data_box_layout.addWidget(self.trial_table, 0, 0, 2, 1)

        self.add_trial_button = QtGui.QPushButton("New Trial")
        self.data_box_layout.addWidget(self.add_trial_button, 0, 1)
        self.add_trial_button.released.connect(self.new_trial)


        self.trial_details_box = QtGui.QGroupBox("Trial Details")
        self.trial_details_box.setSizePolicy(QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Minimum)
        self.data_box_layout.addWidget(self.trial_details_box, 2, 0, 1, 1)
        self.trial_details_box_layout = QtGui.QGridLayout(self.trial_details_box)

        self.echo_trial_details = EchoTrialDetailsWidget()
        self.trial_details_box_layout.addWidget(self.echo_trial_details, 0, 0, 1, 1)
        self.echo_trial_details.hide()

        self.http_trial_details = HttpTrialDetailsWidget()
        self.trial_details_box_layout.addWidget(self.http_trial_details, 0, 0, 1, 1)

        self.racer_settings_widget = RacerDetailsWidget()
        self.trial_details_box_layout.addWidget(self.racer_settings_widget, 1, 0, 1, 1)

        self.trial_status = TrialStatusWidget()
#        self.trial_status.trial_edit.connect(self.show_edit_dialog)
        self.trial_status.trial_started.connect(self.start_trial)
        self.trial_status.trial_stopped.connect(self.stop_trial)
        self.trial_status.trial_refreshed.connect(self.update_trial_details)
        self.trial_status.trial_edit.connect(self.edit_trial)
        self.trial_details_box_layout.addWidget(self.trial_status, 0, 1, 2, 1)

        self.update_current_experiment(0)
        self.trial_table.resizeColumnsToContents()


    def display_context_menu(self, pos):
        index = self.trial_table.indexAt(pos)



        self. menu = QtGui.QMenu()

        self.edit_action = self.menu.addAction("Edit")
        self.edit_action.triggered.connect(self.edit_trial)

        self.duplicate_action = self.menu.addAction("Duplicate")
        self.duplicate_action.triggered.connect(self.duplicate_trial)

        self.delete_action = self.menu.addAction("Delete")
        self.delete_action.triggered.connect(self.delete_trial)

        self.feasibility_separator = self.menu.addAction("---- Feasibility Analysis ----")
        self.feasibility_separator.setEnabled(False)
        self.shorter_action = self.menu.addAction("Set Shorter Trial")
        self.shorter_action.triggered.connect(self.setAsShorterTrial)

        self.longer_action = self.menu.addAction("Set Longer Trial")
        self.longer_action.triggered.connect(self.setAsLongerTrial)


        if self.current_trial.end_date is None:
            self.shorter_action.setEnabled(False)
            self.longer_action.setEnabled(False)
        else:
            self.shorter_action.setEnabled(True)
            self.longer_action.setEnabled(True)

        table_viewport  = self.trial_table.viewport()
        self.menu.popup(table_viewport.mapToGlobal(pos))

    def setAsShorterTrial(self):
        self.emit(QtCore.SIGNAL("shorter_trial_set(PyQt_PyObject)"), self.current_trial)

    def setAsLongerTrial(self):
        self.emit(QtCore.SIGNAL("longer_trial_set(PyQt_PyObject)"), self.current_trial)


    def update_current_experiment(self, index):
        self.current_experiment = self.experiment_list.currentItem()
        #self.experiment_name.setText(self.current_experiment.name)
        self.update_trial_table()
#        self.trial_table.setSelection()


    def update_current_trial(self,x,y):
        self.current_trial = self.trial_table_selection_model.currentIndex().data(QtCore.Qt.EditRole)
        if len(x.indexes()) == 0:
            self.trial_status.start_trial_button.setEnabled(False)
            self.trial_status.edit_trial_button.setEnabled(False)
            self.trial_status.refresh_trial_button.setEnabled(False)
            self.trial_status.stop_trial_button.setEnabled(False)
        else:
            self.update_trial_details()

    def edit_trial(self):
        dialog = NewTrialDialog(self.session, experiment=self.current_experiment, parent=self, trial=self.current_trial)
        dialog.accepted.connect(self.trial_table_model.refresh)
        dialog.exec()



    def update_trial_details(self):
        self.session.refresh(self.current_trial)
        self.trial_status.edit_trial_button.setEnabled(True)
        self.trial_status.refresh_trial_button.setEnabled(True)

        if self.current_trial.start_date == None:
            self.trial_status.start_trial_button.setEnabled(True)
            self.trial_status.stop_trial_button.setEnabled(False)
        else:
            self.trial_status.start_trial_button.setEnabled(False)
            self.trial_status.stop_trial_button.setEnabled(True)

        if(self.current_trial.__class__.__name__ == "HTTPTrial"):
            self.echo_trial_details.hide()
            self.http_trial_details.show()
            self.http_trial_details.request_url.setText(self.current_trial.request_url)
            self.http_trial_details.type.setText("HTTP Trial")

        else:
            self.echo_trial_details.show()
            self.http_trial_details.hide()
            self.echo_trial_details.delay.setText(str(self.current_trial.delay))
            self.echo_trial_details.type.setText("Echo Trial")

        self.http_trial_details.name.setText(self.current_trial.name)
        self.http_trial_details.description.setText(self.current_trial.description)

        self.racer_settings_widget.racer.setText(self.current_trial.racer.hostname)
        self.racer_settings_widget.core_id.setText(str(self.current_trial.core_id))
        self.racer_settings_widget.real_time.setText(str(self.current_trial.real_time))

        self.trial_status.start.setText(str(self.current_trial.start_date))
        self.trial_status.end.setText(str(self.current_trial.end_date))

        try:
            job = Job.fetch(self.current_trial.job, connection=self.redis_conn)
            self.trial_status.job_status.setText(job.get_status())
        except:
            self.trial_status.job_status.setText("not scheduled")




    def stop_trial(self):
        self.current_trial.start_date = None
        self.current_trial.end_date = None
        self.session.add(self.current_trial)
        self.session.commit()

        job = Job.fetch(self.current_trial.job, connection=self.redis_conn)
        job.cancel()
        self.update_trial_details()
        self.trial_table.resizeColumnsToContents()


    def delete_trial(self):
        reply = QtGui.QMessageBox.question(self, "Confirm", "Really delete the selected trial?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            self.session.delete(self.current_trial)
            self.session.commit()
            self.update_trial_table()

    def duplicate_trial(self):
        new = self.current_trial.duplicate()
        self.session.add(new)
        self.session.commit()
        self.update_trial_table()

    def start_trial(self):
        q = Queue(self.current_trial.racer.hostname, connection=self.redis_conn)
        t = self.current_trial

        job = None
        if(self.current_trial.__class__.__name__ == "HTTPTrial"):
            job = HTTPTrialJob()
            job.request = t.request
            job.request_url = t.request_url
        else:
            job = EchoTrialJob()
            job.target_host = t.host
            job.target_port = t.port
            job.delay = t.delay

        job.reps = t.reps
        job.core_affinity = t.core_id
        if t.real_time:
            job.real_time = 1
        else:
            job.real_time = 0


        res = q.enqueue_call(func=execute_trial, args=(job,), result_ttl=-1, timeout=1000000)
        self.current_trial.job = res.get_id()
        self.current_trial.start_date = datetime.now()
        self.session.add(self.current_trial)
        self.session.commit()

        res.save()
        self.trial_status.start_trial_button.setEnabled(False)
        self.trial_status.stop_trial_button.setEnabled(True)
        self.update_trial_details()
        self.trial_table.resizeColumnsToContents()


    def update_trial_table(self):
        self.trial_table_model.setFilter(Trial.experiment==self.current_experiment)
        self.trial_table.resizeColumnsToContents()



    def new_trial(self):
        dialog = NewTrialDialog(self.session, experiment=self.current_experiment, parent=self)
        dialog.accepted.connect(self.trial_table_model.refresh)
        dialog.exec()


    def new_experiment(self):
        dialog = QtGui.QInputDialog(self)
        dialog.setLabelText("Please enter the name for the new Experiment.")
        dialog.textValueSelected.connect(self.store_new_experiment)
        dialog.exec()

    def store_new_experiment(self, name):
        exp = Experiment()
        exp.name = name
        self.session.add(exp)
        self.session.commit()
        self.experiment_list.refresh_experiments()

