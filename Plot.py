import numpy as np
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3 import NavigationToolbar2GTK3
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)


class SnaptoCursor(object):
    """
    Две линии, бегающие за курсором

    """

    def __init__(self, ax, x, y):  # ax - plot, x - набор данных по x, y - набор данных по y
        self.__active = False  # активен ли курсор
        self.ax = ax
        self.lx = ax.axhline(color='k', lw=1)  # the horiz line
        self.ly = ax.axvline(color='k', lw=1)  # the vert line
        self.active = False     # убираем линии
        self.x = x
        self.y = y

    def mouseMove(self, event):
        if not event.inaxes:  # за пределами осей
            return
        x, y = event.xdata, event.ydata  # получение данных о положении курсора
        indx = min(np.searchsorted(self.x, [x])[0], len(self.x) - 1)  # минимальное расстояние до линии
        x = self.x[indx]
        y = self.y[indx]
        # update the line positions
        if self.__active:
            self.lx.set_ydata(y)
            self.ly.set_xdata(x)
        self.ax.figure.canvas.draw()  # обновляем данные график

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, a: bool):
        self.__active = a
        if not a:
            self.lx.set_ydata(None)    # убираем линии, чтоб их было не видно
            self.ly.set_xdata(None)


# виджет-график
class PlotCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure(figsize=(5, 4), dpi=100)
        FigureCanvas.__init__(self, self.fig)
        self.data = None  # данные графика
        self.cursor = None  # курсор
        self.plot = None  # график
        self.markersData = None  # маркеры

    def loadData(self, data):  # загрузка графика
        self.data = data
        self.plot = self.fig.add_subplot(1, 1, 1)
        self.plot.plot(self.data.measurementNumber, self.data.magnitudeX)  # сделать, чтоб было 3 графика
        self.plot.plot(self.data.measurementNumber, self.data.magnitudeY)
        self.plot.plot(self.data.measurementNumber, self.data.magnitudeZ)
        self.cursor = SnaptoCursor(self.plot, self.data.measurementNumber, self.data.magnitudeX)
        self.fig.canvas.mpl_connect("motion_notify_event", self.cursor.mouseMove)  # привязываем события к обработчикам
        self.fig.canvas.mpl_connect("button_press_event", self.mousePress)

    def mousePress(self, event):  # обработчик события, нажатия кнопки мыши
        if not event.inaxes:
            return
        if self.cursor.active:
            x, y = self.cursor.ly.get_xdata(), self.cursor.lx.get_ydata()  # получение текущих значений вертикальной и
            # горизонтальной линий
            self.plot.scatter(x, y, s=50)  # ставим маркер на график, толщина 50 попугаев
            self.setMarker(self, self.cursor, x, y)  # вызываем ф-ию обработчик того, что мы поставили маркер

    def setMarker(self, cursor, x, y):  # ф-ия для перегрузки, вызывается, когда ставится маркер
        pass


class NavigationToolbar(NavigationToolbar2GTK3):
    toolitems = [tool for tool in NavigationToolbar2GTK3.toolitems if
                 tool[0] in ('Home', 'Back', 'Forward', 'Pan', 'Zoom', 'Save')]


class PlotWindow(Gtk.Window):  # отдельное окно с графиком
    def __init__(self, title="Figure"):
        Gtk.Window.__init__(self, title=title)
        self.set_property("width_request", 300)
        self.set_property("height_request", 300)
        self.plotCanvas = PlotCanvas()  # график
        self.toolbar = NavigationToolbar(self.plotCanvas, self)  # toolbar matplotlib'a

        self.markerImage = Gtk.Image()  # изображение маркера
        self.markerImage.set_from_file("images/marker25x25.png")
        self.rebuildImage = Gtk.Image(stock=Gtk.STOCK_EXECUTE)  # изображение шестеренок

        self.rebuildButton = Gtk.Button(label=None, image=self.rebuildImage)  # кнопка перекомпановки графиков

        self.setMarkerToggleButton = Gtk.ToggleButton(label=None, image=self.markerImage)  # кнопка-переключатель,
        # при нажании на которую можно ставить маркеры
        self.setMarkerToggleButton.connect("toggled", self.setMarkerToggleButton_Click)

        self.customToolBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        self.customToolBox.pack_start(self.toolbar, False, False, 1)
        self.customToolBox.pack_start(self.setMarkerToggleButton, False, False, 0)
        self.customToolBox.pack_start(self.rebuildButton, False, False, 0)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.box.pack_start(self.plotCanvas, True, True, 0)
        self.box.pack_start(self.customToolBox, False, False, 1)
        self.add(self.box)

    def setMarkerToggleButton_Click(self, button):
        self.plotCanvas.cursor.active = button.get_active()     # делаем курсор активным/неактивным


if __name__ == "__main__":
    PlotWindow().show_all()
    Gtk.main()
