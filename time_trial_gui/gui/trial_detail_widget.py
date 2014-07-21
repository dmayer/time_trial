__author__ = 'daniel'

from PyQt4 import QtGui, QtCore

from PyQt4.QtCore import pyqtSignal

class TrialDetailsWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(TrialDetailsWidget, self).__init__(parent)

        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

        self.box = QtGui.QGroupBox("Trial Settings")
        self.layout.addWidget(self.box)

        self.box_layout = QtGui.QFormLayout()
        self.box_layout.setFormAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.box.setLayout(self.box_layout)


        self.type = QtGui.QLabel("")
        self.box_layout.addRow("<b>Type</b>", self.type)

        self.name = QtGui.QLabel("")
        self.box_layout.addRow("<b>Name</b>", self.name)

        self.description = QtGui.QLabel("")
        self.box_layout.addRow("<b>Description</b>", self.description)


class EchoTrialDetailsWidget(TrialDetailsWidget):

    def __init__(self, parent=None):
        super(EchoTrialDetailsWidget, self).__init__(parent)

        self.delay = QtGui.QLabel("")
        self.box_layout.addRow("<b>Delay (ns)</b>", self.delay)

class HttpTrialDetailsWidget(TrialDetailsWidget):

    def __init__(self, parent=None):
        super(HttpTrialDetailsWidget, self).__init__(parent)

        self.request_url = QtGui.QLabel("")
        self.box_layout.addRow("<b>Request URL</b>", self.request_url)


class RacerDetailsWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(RacerDetailsWidget, self).__init__(parent)

        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)


        self.box = QtGui.QGroupBox("Racer Settings")
        self.layout.addWidget(self.box)
        self.box_layout = QtGui.QFormLayout()
        self.box_layout.setFormAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.box.setLayout(self.box_layout)


        self.racer = QtGui.QLabel("")
        self.box_layout.addRow("<b>Racer</b>", self.racer)


        self.core_id = QtGui.QLabel("")
        self.box_layout.addRow("<b>Core ID</b>", self.core_id)

        self.real_time = QtGui.QLabel("")
        self.box_layout.addRow("<b>Real-Time</b>", self.real_time)




class TrialStatusWidget(QtGui.QWidget):

    trial_started = pyqtSignal()
    trial_stopped = pyqtSignal()
    trial_refreshed = pyqtSignal()
    trial_edit = pyqtSignal()

    def __init__(self, parent=None):
        super(TrialStatusWidget, self).__init__(parent)

        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

        self.box = QtGui.QGroupBox("Trial Status")
        self.super_box_layout = QtGui.QGridLayout()

        self.box_layout = QtGui.QFormLayout()
        self.box_layout.setFormAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        self.box.setLayout(self.super_box_layout)
        self.super_box_layout.addLayout(self.box_layout,0,0,1,2)


        self.layout.addWidget(self.box)

        self.start = QtGui.QLabel("")
        self.box_layout.addRow("<b>Start</b>", self.start)


        self.end = QtGui.QLabel("")
        self.box_layout.addRow("<b>End</b>", self.end)

        self.job_status = QtGui.QLabel("")
        self.box_layout.addRow("<b>Job Status</b>", self.job_status)



        self.start_trial_button = QtGui.QPushButton("Start")
        self.start_trial_button.setEnabled(False)
        self.start_trial_button.released.connect(self.trial_started.emit)
        self.super_box_layout.addWidget(self.start_trial_button,1,0)


        self.stop_trial_button = QtGui.QPushButton("Cancel and Reset")
        self.stop_trial_button.setEnabled(False)
        self.stop_trial_button.released.connect(self.trial_stopped.emit)
        self.super_box_layout.addWidget(self.stop_trial_button,1,1)

        self.refresh_trial_button = QtGui.QPushButton("Refresh")
        self.refresh_trial_button.setEnabled(False)
        self.refresh_trial_button.released.connect(self.trial_refreshed.emit)
        self.layout.addWidget(self.refresh_trial_button)


        self.edit_trial_button = QtGui.QPushButton("Edit")
        self.edit_trial_button.setEnabled(False)
        self.edit_trial_button.released.connect(self.trial_edit.emit)
        self.layout.addWidget(self.edit_trial_button)


