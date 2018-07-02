import gpxpy
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3 import (
    NavigationToolbar2GTK3 as NavigationToolbar)
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)


class SnaptoCursor(object):
    """
    Like Cursor but the crosshair snaps to the nearest x,y point
    For simplicity, I'm assuming x is sorted
    """

    def __init__(self, ax, x, y):
        self.ax = ax
        self.lx = ax.axhline(color='k', lw=1)  # the horiz line
        self.ly = ax.axvline(color='k', lw=1)  # the vert line
        self.x = x
        self.y = y

    def mouseMove(self, event):
        if not event.inaxes:
            return
        x, y = event.xdata, event.ydata
        indx = min(np.searchsorted(self.x, [x])[0], len(self.x) - 1)
        x = self.x[indx]
        y = self.y[indx]
        # update the line positions
        self.lx.set_ydata(y)
        self.ly.set_xdata(x)


# виджет-график
class PlotCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(5, 4), dpi=100)
        FigureCanvas.__init__(self, self.fig)
        self.gpxData = []   # данные с GPX файла
        self.cursor = None
        self.plot = None
        self.markers = []

    def loadGpx(self, path):
        gpxFile = open(path)
        gpx = gpxpy.parse(gpxFile)
        self.gpxData.append(gpx)    # добавляем данные с gpx
        self._buildGpxData()

    def mousePress(self, event):
        if not event.inaxes:
            return
        self.plot.scatter(self.cursor.ly.get_xdata(), self.cursor.lx.get_ydata(), s=45)

    def _buildGpxData(self):
        self.plot = self.fig.add_subplot(1, 1, 1)
        q = []
        lat = []
        lon = []
        mag = []
        for gpx in self.gpxData:
            for route in gpx.routes:
                for point in route.points:
                    q.append(point.vertical_dilution)
                    lat.append(point.latitude)
                    lon.append(point.longitude)
                    mag.append(point.horizontal_dilution)
        self.plot.plot(q, mag)
        self.cursor = SnaptoCursor(self.plot, q, mag)
        self.fig.canvas.mpl_connect("motion_notify_event", self.cursor.mouseMove)
        self.fig.canvas.mpl_connect("button_press_event", self.mousePress)






