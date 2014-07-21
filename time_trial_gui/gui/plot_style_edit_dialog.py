from PyQt4 import QtGui, QtCore

class PlotStyleEditDialog(QtGui.QDialog):

    def __init__(self, plot, parent = None, flags = QtCore.Qt.Dialog):
        QtGui.QDialog.__init__(self, parent, flags)

        self.plot = plot

        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

        form_layout = QtGui.QFormLayout()
        self.layout.addLayout(form_layout)

        self.label = QtGui.QLineEdit(text=plot.label)
        form_layout.addRow("Label", self.label)
        self.bins = QtGui.QLineEdit(text=str(plot.bins))
        form_layout.addRow("Bins",self.bins)
        self.color = QtGui.QLineEdit(text=plot.color)
        form_layout.addRow("Color",self.color)

        self.style = QtGui.QComboBox()
        self.style.insertItem(0, "Steps - Filled", "stepfilled")
        self.style.insertItem(0, "Steps", "step")
        self.style.insertItem(0, "Bars", "bar")
        form_layout.addRow("Style",self.style)


        self.filter_box = QtGui.QGroupBox("Plot Data Range",parent=self)
        self.layout.addWidget(self.filter_box)
        filter_box_layout = QtGui.QFormLayout()
        self.filter_box.setLayout(filter_box_layout)
        filter_comment = QtGui.QLabel(text="These settings will only affect plotting.")
        filter_comment.setWordWrap(True)
        filter_box_layout.addWidget(filter_comment)


        self.filter_type = QtGui.QComboBox()
        self.filter_type.addItem("Absolute Range", "absolute")
        self.filter_type.addItem("Percentile Range", "percentile")

        self.filter_type.setCurrentIndex(self.filter_type.findData(self.plot.range_type))
        filter_box_layout.addWidget(self.filter_type)

        # for absolute
        self.minimum = QtGui.QLineEdit(text="" if plot.minimum == None else str(plot.minimum) )
        filter_box_layout.addRow("Minimum",self.minimum)

        self.maximum = QtGui.QLineEdit(text="" if plot.maximum == None else str(plot.maximum))
        filter_box_layout.addRow("Maximum",self.maximum)


        button_layout = QtGui.QHBoxLayout()
        save = QtGui.QPushButton(text="Save")
        save.released.connect(self.save)
        button_layout.addWidget(save)
        cancel = QtGui.QPushButton(text="Cancel")
        cancel.released.connect(self.reject)
        button_layout.addWidget(cancel)

        self.layout.addLayout(button_layout)

    def save(self):
        self.plot.color = self.color.text()
        self.plot.bins = int(self.bins.text())
        self.plot.label = self.label.text()
        self.plot.style = self.style.itemData(self.style.currentIndex())
        self.plot.minimum = float(self.minimum.text()) if self.minimum.text() != "" else None
        self.plot.maximum = float(self.maximum.text()) if self.maximum.text() != "" else None
        self.plot.range_type = "absolute" if self.filter_type.currentText() == "Absolute Range" else "percentile"
        self.accept()


