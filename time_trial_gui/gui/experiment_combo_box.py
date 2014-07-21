from PyQt4 import QtGui
from models.experiment import Experiment

__author__ = 'daniel'

class ExperimentComboBox(QtGui.QComboBox):

    def __init__(self, session = None, parent = None):
        super(ExperimentComboBox, self).__init__(parent)
        self.session = session
        self.refresh_experiments()

    def refresh_experiments(self):
        self.clear()
        self.experiments = self.session.query(Experiment).all()
        for e in self.experiments:
            self.addItem(e.name)

    def currentItem(self):
        try:
            val = self.experiments[self.currentIndex()]
        except Exception as e:
            print(e)
            return None

        return val

