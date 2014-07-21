__author__ = 'daniel'
from PyQt4 import QtGui, QtCore

class PlotSettingsDialog(QtGui.QDialog):

    def __init__(self, plot_settings=None, parent=None):
        super(PlotSettingsDialog, self).__init__(parent)

        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)
        self.plot_settings = plot_settings


        form_layout =  QtGui.QFormLayout()

        # plot settings
        plot_settings_box = QtGui.QGroupBox(title="Plot Settings")
        plot_settings_box_layout = QtGui.QVBoxLayout()
        plot_settings_box.setLayout(plot_settings_box_layout)
        plot_settings_box_form_layout =  QtGui.QFormLayout()
        plot_settings_box_layout.addLayout(plot_settings_box_form_layout)

        self.plot_settings_box_x_axis_label = QtGui.QLineEdit(text = self.plot_settings.x_axis_label)
        form_layout.addRow("X-Axis Label", self.plot_settings_box_x_axis_label)

        self.plot_settings_box_y_axis_label = QtGui.QLineEdit(text = self.plot_settings.y_axis_label)
        form_layout.addRow("Y-Axis Label", self.plot_settings_box_y_axis_label)

        self.plot_settings_box_legend = QtGui.QCheckBox()
        if self.plot_settings.legend:
            self.plot_settings_box_legend.setChecked(True)
        else:
            self.plot_settings_box_legend.setChecked(False)


        self.x_minimum = QtGui.QLineEdit(text = self.plot_settings.x_minimum)
        form_layout.addRow("X-Axis Minimum", self.x_minimum)

        self.x_maximum = QtGui.QLineEdit(text = self.plot_settings.x_maximum)
        form_layout.addRow("X-Axis Maximum", self.x_maximum)


        self.x_scaling = QtGui.QLineEdit(text = str(self.plot_settings.x_scaling))
        form_layout.addRow("X-Axis Scaling Factor", self.x_scaling)


        self.y_minimum = QtGui.QLineEdit(text = self.plot_settings.y_minimum)
        form_layout.addRow("Y-Axis Minimum", self.y_minimum)

        self.y_maximum = QtGui.QLineEdit(text = self.plot_settings.y_maximum)
        form_layout.addRow("Y-Axis Maximum", self.y_maximum)


        form_layout.addRow("Legend", self.plot_settings_box_legend)



        self.layout.addLayout(form_layout)
        button_box = QtGui.QDialogButtonBox()
        button_box.addButton("OK", QtGui.QDialogButtonBox.AcceptRole)
        button_box.addButton("Cancel", QtGui.QDialogButtonBox.RejectRole)
        button_box.rejected.connect(self.cancel)
        button_box.accepted.connect(self.apply)

        self.layout.addWidget(button_box)

    def apply(self):
        self.plot_settings.x_axis_label = self.plot_settings_box_x_axis_label.text()
        self.plot_settings.y_axis_label = self.plot_settings_box_y_axis_label.text()
        self.plot_settings.x_minimum = float(self.x_minimum.text()) if self.x_minimum.text()!= "" else None
        self.plot_settings.x_maximum = float(self.x_maximum.text()) if self.x_maximum.text()!= "" else None
        self.plot_settings.y_minimum = float(self.y_minimum.text()) if self.y_minimum.text()!= "" else None
        self.plot_settings.y_maximum = float(self.y_maximum.text()) if self.y_maximum.text()!= "" else None
        self.plot_settings.x_scaling = float(self.x_scaling.text()) if self.x_scaling.text()!= "" else None
        self.plot_settings.legend = self.plot_settings_box_legend.isChecked()
        self.accept()

    def cancel(self):
        self.reject()
