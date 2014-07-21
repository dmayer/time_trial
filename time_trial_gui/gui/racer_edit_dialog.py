__author__ = 'daniel'

from PyQt4 import QtGui, QtCore

class RacerEditDialog(QtGui.QDialog):

    def __init__(self, racer, parent = None, flags = QtCore.Qt.Dialog):
        QtGui.QDialog.__init__(self, parent, flags)

        self.racer = racer

        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

        form_layout = QtGui.QFormLayout()
        self.layout.addLayout(form_layout)

        self.name = QtGui.QLineEdit(text=racer.name)
        form_layout.addRow("Name", self.name)
        self.hostname = QtGui.QLineEdit(text=racer.hostname)
        form_layout.addRow("Hostname",self.hostname)
        self.location = QtGui.QLineEdit(text=racer.location)
        form_layout.addRow("Location",self.location)

        button_layout = QtGui.QHBoxLayout()
        save = QtGui.QPushButton(text="Save")
        save.released.connect(self.save)
        button_layout.addWidget(save)
        cancel = QtGui.QPushButton(text="Cancel")
        cancel.released.connect(self.reject)
        button_layout.addWidget(cancel)

        self.layout.addLayout(button_layout)

    def save(self):
        self.racer.name = self.name.text()
        self.racer.hostname = self.hostname.text()
        self.racer.location = self.location.text()
        self.accept()

