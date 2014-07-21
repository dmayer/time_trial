import logging

from gui.mpl_canvas import *
from pylab import Rectangle
from matplotlib.patches import Rectangle
import matplotlib.ticker as ticker

import numpy

from PyQt4 import QtGui, QtCore



class Histogram(MplCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100, settings=None):
        MplCanvas.__init__(self, parent, width, height, dpi)

        self.settings = settings
        self.logger = logging.getLogger('time_trial')

    def add_plot_raw(self, data, bins, type, range, label, color, final = False):
        self.axes.hist(data, bins, histtype=type, range=range, color=color, label=label, alpha=0.5)
        self.axes.relim()
        if self.settings.legend:
            self.axes.legend()


    def compute_initial_figure(self):
        pass

    def draw_rectangle(self, x, y, width, height, fg_color="CornflowerBlue", edge_color="gray"):
        self.axes.add_patch(Rectangle((x, y), width, height, ec=edge_color, fc=fg_color, alpha=0.5, zorder=10))
        self.update_figure()


    def add_plot(self, plot):
        ticks = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x*self.settings.x_scaling))
        self.axes.xaxis.set_major_formatter(ticks)

        if plot.minimum is None and plot.maximum is None:
            range = [min(plot.timing_data.data), max(plot.timing_data.data)]
        elif plot.range_type == "absolute":
            range = [plot.minimum, plot.maximum]
            print(range)
            if len(numpy.intersect1d(range, plot.timing_data.data)) == 0:
                msg = QtGui.QMessageBox()
                msg.setIcon(QtGui.QMessageBox.Warning)
                msg.setText("The specified range is invalid for data set as they do not overlap. Falling back to plotting the full range instead:\n [min(data), max(data)].")
                msg.exec()
                logging.warning("Specified range is invalid for data. Falling back to [min(data), max(data)].")
                plot.minimum = min(plot.timing_data.data)
                plot.maximum = max(plot.timing_data.data)
                range = [plot.minimum, plot.maximum]

        else:
            range = [plot.timing_data.quantile(plot.minimum), plot.timing_data.quantile(plot.maximum)]

        self.add_plot_raw(plot.timing_data.data, plot.bins, plot.style, range, plot.label, plot.color)

    def clear(self):
        self.axes.cla()
        self.axes.set_xlabel(self.settings.x_axis_label)
        self.axes.set_ylabel(self.settings.y_axis_label)
        self.fig.tight_layout()



