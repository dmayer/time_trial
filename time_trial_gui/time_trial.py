import sys

from PyQt4 import QtGui, QtCore
import sip
from sqlalchemy.orm import sessionmaker
from gui.experiments_tab import ExperimentsTab

from gui.feasibility_tab import FeasibilityTab
from gui.plotter_tab import PlotterTab

import logging
from sqlalchemy import create_engine
from gui.settings_tab import SettingsTab
from lib.rq_result_processor import RqResultsProcessor
from models.racer import Racer
from models.trial import Trial
from models.experiment import Experiment
from lib.base import Base




progname = "Time Trial"
progversion = "0.1"


class ApplicationWindow(QtGui.QMainWindow):
    def __init__(self):
        ################
        #  Data Init
        ################
        logger = logging.getLogger('time_trial')
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        logger.info("Time Trial starting up...")

        #####################
        #  Connect Database
        #####################
        self.engine = create_engine('sqlite:///data.sqlite',  connect_args={'check_same_thread':False},  echo=False)
        Base.metadata.create_all(self.engine, checkfirst=True)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        ################################
        #  Launching Background Threads
        ################################

        # thread to check for results
        self.processor = RqResultsProcessor()
        ThreadSession = sessionmaker(bind=self.engine)
        self.processor.session = ThreadSession()
        self.processor.start()




        ################
        #  G U I
        ################
        QtGui.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("Time Trial")
        self.setWindowIcon(QtGui.QIcon('images/clock.png'))


        ################
        #  M E N U
        ################


        self.file_menu = QtGui.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtGui.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        ################
        #  Main Window
        ################
        self.main_widget = QtGui.QWidget(self)
        self.main_layout = QtGui.QGridLayout(self.main_widget)



        self.tab_widget = QtGui.QTabWidget(self.main_widget)
        self.main_layout.addWidget(self.tab_widget,0,0)

        self.experiment_tab = ExperimentsTab(session = self.session, parent = self.main_widget)

        QtCore.QObject.connect(self.experiment_tab,
                       QtCore.SIGNAL("shorter_trial_set(PyQt_PyObject)") ,
                       self.shorter_trial_set)


        QtCore.QObject.connect(self.experiment_tab,
                               QtCore.SIGNAL("longer_trial_set(PyQt_PyObject)") ,
                               self.longer_trial_set)

        self.tab_widget.addTab(self.experiment_tab, "Experiments")

        self.feasibility_tab = FeasibilityTab(session = self.session, parent = self.main_widget)
        self.tab_widget.addTab(self.feasibility_tab, "Feasibility Analysis")
#
#        self.plotter_tab = PlotterTab(self.main_widget)
#        self.tab_widget.addTab(self.plotter_tab, "Plotter")
#
        self.settings_tab = SettingsTab(self.main_widget, session = self.session)
        self.tab_widget.addTab(self.settings_tab, "Settings")

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

    def shorter_trial_set(self, trial):
        self.feasibility_tab.set_shorter(trial)

    def longer_trial_set(self, trial):
        self.feasibility_tab.set_longer(trial)


    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.session.close()
        self.processor.stop()
        self.processor.join()
        self.fileQuit()

    def about(self):
        QtGui.QMessageBox.about(self, "About", """TKTK""" )






# The following call prevents C++ destructors from being called.
# The order of calling would be arbitrary and causes a crash when
# closing the PyQt app.
# http://pyqt.sourceforge.net/Docs/sip4/python_api.html
# https://stackoverflow.com/questions/23565702/pyqt4-crashed-on-exit
sip.setdestroyonexit(False)

qApp = QtGui.QApplication(sys.argv)
qApp.setWindowIcon(QtGui.QIcon('images/clock.png'))
qApp.setApplicationName("Time Trial")

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)

desktop = QtGui.QDesktopWidget()
screen_size = desktop.availableGeometry()
width = min(screen_size.width() * 0.9, 1024)
height = min(screen_size.height() * 0.95, 900)

aw.setFixedSize(QtCore.QSize(width, height))
aw.show()
aw.raise_()


sys.exit(qApp.exec_())
#qApp.exec_()

