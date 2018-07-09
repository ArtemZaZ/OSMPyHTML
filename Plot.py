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
import threading


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
        self.gpxData = []   # данные с GPX файла
        self.cursor = None  # курсор
        self.plot = None    # график
        self.markers = []   # маркеры
        self.tastyData = [] # распарсенные данные, хранятся как кеш, чтоб при поиске параметров маркера не парсить
        # второй раз gpx файл

    def loadGpx(self, path):    # загрузка графика
        gpxFile = open(path)
        gpx = gpxpy.parse(gpxFile)
        self.gpxData.clear()    # очистка предыдущих данных
        self.gpxData.append(gpx)    # добавляем данные с gpx
        self._buildGpxData()    # сборка новых данных

    def mousePress(self, event):    # обработчик события, нажатия кнопки мыши
        if not event.inaxes:
            return
        x, y = self.cursor.ly.get_xdata(), self.cursor.lx.get_ydata()   # получение текущих значений вертикальной и
        # горизонтальной линий
        self.plot.scatter(x, y, s=50)   # ставим маркер на график, толкина 50 попугаев
        self.markers.append([x, y])     # добавляем его в список маркеров
        self.setMarker(self, self.cursor)   # вызываем ф-ию обработчик того, что мы поставили маркер

    def _buildGpxData(self):    # сборка данных графика
        self.plot = self.fig.add_subplot(1, 1, 1)
        q = []      # Данные с gpx
        lat = []    #
        lon = []    #
        mag = []    #
        for gpx in self.gpxData:    # проходим по каждому маршруту и добавляем значения из точек
            for route in gpx.routes:
                for point in route.points:
                    q.append(point.vertical_dilution)
                    lat.append(point.latitude)
                    lon.append(point.longitude)
                    mag.append(point.horizontal_dilution)
        self.plot.plot(q, mag)
        self.tastyData = [q, lat, lon, mag]     # сохраняем данные
        self.cursor = SnaptoCursor(self.plot, q, mag)   # создаем курсор
        self.fig.canvas.mpl_connect("motion_notify_event", self.cursor.mouseMove)   # привязываем события к обработчикам
        self.fig.canvas.mpl_connect("button_press_event", self.mousePress)

    def setMarker(self, cursor):    # ф-ия для перегрузки, вызывается, когда ставится маркер
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










