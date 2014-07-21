from gui.http_request_text_edit import HttpRequestTextEdit
from models.racer import Racer
from models.trial import Trial, EchoTrial, HTTPTrial


__author__ = 'daniel'



from PyQt4 import QtGui, QtCore

class NewTrialDialog(QtGui.QDialog):
    init_done = False

    def __init__(self, session, experiment = None, trial = None, parent = None, flags = QtCore.Qt.Dialog):
        QtGui.QDialog.__init__(self, parent, flags)

        self.session = session
        self.experiment = experiment
        self.trial = trial

        self.layout = QtGui.QGridLayout()
        self.setLayout(self.layout)

        top_layout =  QtGui.QFormLayout()
        self.type = QtGui.QComboBox()
        self.type.currentIndexChanged.connect(self.trial_type_changed)
        self.type.addItem("HTTP Trial", "HTTP Trial")
        self.type.addItem("Echo Trial", "Echo Trial")
        top_layout.addRow("Trial Type", self.type)


        self.layout.addLayout(top_layout,0,0,1,2)

        ## GENERAL

        general_group = QtGui.QGroupBox("General Settings")
        general_group_layout = QtGui.QFormLayout()
        general_group.setLayout(general_group_layout)



        self.name = QtGui.QLineEdit()
        if self.trial is not None: self.name.setText(trial.name)
        general_group_layout.addRow("Name", self.name)

        self.reps = QtGui.QLineEdit()
        if self.trial is not None:  self.reps.setText(str(trial.reps))
        general_group_layout.addRow("Repetitions", self.reps)

        self.description = QtGui.QPlainTextEdit()
        self.description.setMinimumWidth(100)
        self.description.setTabChangesFocus(True)
        if self.trial is not None: self.description.setPlainText(trial.description)

        general_group_layout.addRow("Description", self.description)


        self.layout.addWidget(general_group,1,0)

        racer_group = QtGui.QGroupBox("Racer Settings")
        racer_group_layout = QtGui.QFormLayout()
        racer_group.setLayout(racer_group_layout)

        self.racer = QtGui.QComboBox()
        for r in self.session.query(Racer).all():
            self.racer.addItem(r.hostname, r.id)

        if self.trial is not None: self.racer.setCurrentIndex(self.racer.findData(self.trial.racer.id))

        racer_group_layout.addRow("Racer", self.racer)

        self.core_id = QtGui.QLineEdit()
        if self.trial is not None: self.core_id.setText(str(self.trial.core_id))

        self.core_id.setToolTip("Assigns the racer to the specified CPU core.")
        racer_group_layout.addRow("CPU Core", self.core_id)

        self.real_time = QtGui.QComboBox()
        self.real_time.setToolTip("Executes the trial with real-time priority.")
        self.real_time.addItem("True", userData=True)
        self.real_time.addItem("False", userData=False)
        if self.trial is not None: self.real_time.setCurrentIndex(self.real_time.findData(bool(self.trial.real_time)))
        racer_group_layout.addRow("Real-Time Scheduling", self.real_time)

        self.layout.addWidget(racer_group, 2,0)


        ## ECHO
        self.echo_group = QtGui.QGroupBox("Echo-Specific Settings")
        echo_group_layout = QtGui.QFormLayout()
        self.echo_group.setLayout(echo_group_layout)

        self.host = QtGui.QLineEdit()
        echo_group_layout.addRow("Host", self.host)

        self.port = QtGui.QLineEdit()
        echo_group_layout.addRow("Port", self.port)

        self.delay = QtGui.QLineEdit()
        echo_group_layout.addRow("Delay (ns)", self.delay)

        if self.trial is not None and self.trial.discriminator == "Echo Trial":
            self.type.setCurrentIndex(self.type.findData("Echo Trial"))
            self.type.setEnabled(False) # we don't allow chanigng the type when editing
            self.host.setText(self.trial.host)
            self.port.setText(str(self.trial.port))
            self.delay.setText(str(self.trial.delay))


        self.layout.addWidget(self.echo_group,1,1,2,1)
        self.echo_group.hide()


        ## HTTP
        self.http_group = QtGui.QGroupBox("HTTP-Specific Settings")
        http_group_layout = QtGui.QFormLayout()
        self.http_group.setLayout(http_group_layout)


        if self.trial is not None and self.trial.discriminator == "Echo Trial":
            self.echo_group.show()
            self.http_group.hide()
        else:
            self.echo_group.hide()
            self.http_group.show()


        self.request_url = QtGui.QLineEdit()
        self.request_url.setMinimumWidth(400)
        http_group_layout.addRow("Request URL", self.request_url)
        http_group_layout.addRow("",QtGui.QLabel(text="<i>(e.g., https://www.example.com:43562)</i>"))

        self.http_request = HttpRequestTextEdit(self)
        http_group_layout.addRow("HTTP request",self.http_request)

        self.layout.addWidget(self.http_group, 1,1, 2,1)

        if self.trial is not None and self.trial.discriminator == "HTTP Trial":
            self.type.setCurrentIndex(self.type.findData("HTTP Trial"))
            self.type.setEnabled(False) # we don't allow chanigng the type when editing
            self.request_url.setText(self.trial.request_url)
            self.http_request.setPlainText(self.trial.request)
            self.http_request.highlight()


        button_box = QtGui.QDialogButtonBox()
        if self.trial is None:
            button_box.addButton("Create", QtGui.QDialogButtonBox.AcceptRole)
        else:
            button_box.addButton("Save", QtGui.QDialogButtonBox.AcceptRole)

        button_box.addButton("Cancel", QtGui.QDialogButtonBox.RejectRole)
        button_box.rejected.connect(self.cancel)
        button_box.accepted.connect(self.store)

        self.layout.addWidget(button_box,3,0, 1, 2)
        self.init_done = True

    def trial_type_changed(self, index):
        if self.init_done:

            if self.type.currentText() == "HTTP Trial":
                self.echo_group.hide()
                self.http_group.show()
            else:
                self.echo_group.show()
                self.http_group.hide()




    def store(self):

        ## init for editing
        trial = self.trial

        # only init a new Trial object when not editing
        if trial is None:
            if self.type.currentText() == "HTTP Trial":
                trial = HTTPTrial()
            else:
                trial = EchoTrial()


        #store type-specific data
        if self.type.currentText() == "HTTP Trial":
            trial.request_url = self.request_url.text()
            trial.request = self.http_request.toPlainText()
        else:
            trial.delay = self.delay.text()
            trial.host = self.host.text()
            trial.port = self.port.text()

        trial.name = self.name.text()
        trial.description = self.description.toPlainText()
        trial.reps = self.reps.text()

        trial.core_id = int(self.core_id.text())
        trial.real_time = self.real_time.itemData(self.real_time.currentIndex(), QtCore.Qt.UserRole)
        racer = self.session.query(Racer).filter_by(hostname = self.racer.currentText()).first()

        trial.racer = racer
        trial.experiment = self.experiment
        self.session.add(trial)
        self.session.commit()
        self.accept()

    def cancel(self):
        self.reject()




