import gpxpy
import matplotlib.pyplot as plt
import numpy as np
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3 import (
    NavigationToolbar2GTK3 as NavigationToolbar)
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
import DataWorker


class SnaptoCursor(object):
    """
    Две линии, бегающие за курсором

    """
    def __init__(self, ax, x, y):   # ax - plot, x - набор данных по x, y - набор данных по y
        self.ax = ax
        self.lx = ax.axhline(color='k', lw=1)  # the horiz line
        self.ly = ax.axvline(color='k', lw=1)  # the vert line
        self.x = x
        self.y = y

    def mouseMove(self, event):
        if not event.inaxes:    # за пределами осей
            return
        x, y = event.xdata, event.ydata     # получение данных о положении курсора
        indx = min(np.searchsorted(self.x, [x])[0], len(self.x) - 1)    # минимальное расстояние до линии
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
        self.data = None    # данные графика
        self.cursor = None  # курсор
        self.plot = None    # график
        self.markersData = None   # маркеры

    def loadData(self, data):    # загрузка графика
        self.data = data
        self.plot = self.fig.add_subplot(1, 1, 1)
        self.plot.plot(self.data.measurementNumber, self.data.magnitudeX)     # сделать, чтоб было 3 графика
        self.cursor = SnaptoCursor(self.plot, self.data.measurementNumber, self.data.magnitudeX)
        self.fig.canvas.mpl_connect("motion_notify_event", self.cursor.mouseMove)   # привязываем события к обработчикам
        self.fig.canvas.mpl_connect("button_press_event", self.mousePress)

    def mousePress(self, event):    # обработчик события, нажатия кнопки мыши
        if not event.inaxes:
            return
        x, y = self.cursor.ly.get_xdata(), self.cursor.lx.get_ydata()   # получение текущих значений вертикальной и
        # горизонтальной линий
        self.plot.scatter(x, y, s=50)   # ставим маркер на график, толщина 50 попугаев
        self.setMarker(self, self.cursor, x, y)   # вызываем ф-ию обработчик того, что мы поставили маркер

    def setMarker(self, cursor, x, y):    # ф-ия для перегрузки, вызывается, когда ставится маркер
        pass


class PlotWindow(Gtk.Window):   # отдельное окно с графиком
    def __init__(self, title="Figure"):
        Gtk.Window.__init__(self, title=title)
        self.set_property("width_request", 300)
        self.set_property("height_request", 300)
        self.plotCanvas = PlotCanvas()
        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.add(self.box)
        self.box.pack_start(self.plotCanvas, True, True, 0)
        self.toolbar = NavigationToolbar(self.plotCanvas, self)
        self.box.pack_start(self.toolbar, False, False, 1)










