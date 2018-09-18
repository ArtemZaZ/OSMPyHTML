import numpy as np
import gi
import numpy

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

    def __init__(self, ax, data):  # ax - plot, x - набор данных по x, y - набор данных по y,
        self.__active = False  # активен ли курсор
        self.ax = ax
        self.lx = ax.axhline(color='k', lw=1)  # the horiz line
        self.ly = ax.axvline(color='k', lw=1)  # the vert line
        self.index = None  # индекс графика, на котором находится указатель
        self.active = False     # убираем линии
        self.data = data

    def mouseMove(self, event):
        if not event.inaxes:  # за пределами осей
            return
        # в данном случае x - является номером измерений, нумерация с 1 -> можно использовать, как индекс
        try:
            mx, my = event.xdata, event.ydata  # получение данных о положении курсора
            x = self.data.measurementNumber[int(mx)]     # получаем значение по X # можно опустить
            tempList = [abs(i - my) for i in [self.data.magnitudeX[x], self.data.magnitudeY[x], self.data.magnitudeZ[x]]]
            ind = tempList.index(min(tempList))     # получаем индекс ближайшего графика 0 - X, 1 - Y, 2 - Z

            if ind == 0:
                y = self.data.magnitudeX[x]
                self.index = 'magX'
            elif ind == 1:
                y = self.data.magnitudeY[x]
                self.index = 'magY'
            elif ind == 2:
                y = self.data.magnitudeZ[x]
                self.index = 'magZ'
            else:
                return

            # update the line positions
            if self.__active:
                self.lx.set_ydata(y)
                self.ly.set_xdata(x)
            self.ax.figure.canvas.draw()  # обновляем данные график
        except:
            pass

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
        self.__markerStyle = dict(linestyle=':', color='0.4',
                                  markersize=10, mfc="C0", mec="C0")
        self.__markersDict = {}

    def loadData(self, data):  # загрузка графика
        self.data = data
        self.plot = self.fig.add_subplot(1, 1, 1)
        self.plot.plot(self.data.measurementNumber, self.data.magnitudeX)  # сделать, чтоб было 3 графика
        self.plot.plot(self.data.measurementNumber, self.data.magnitudeY)
        self.plot.plot(self.data.measurementNumber, self.data.magnitudeZ)
        # маркеры, как отдельные графики
        magXmarkers, = self.plot.plot([], linewidth=0, marker='.', **self.__markerStyle)
        magYmarkers, = self.plot.plot([], linewidth=0, marker='1', **self.__markerStyle)
        magZmarkers, = self.plot.plot([], linewidth=0, marker='|', **self.__markerStyle)
        self.__markersDict = {  # словарь маркеров
            "magX": magXmarkers,
            "magY": magYmarkers,
            "magZ": magZmarkers
        }
        self.plot.legend(self.plot.lines, ('magX', 'magY', 'magZ'))
        self.cursor = SnaptoCursor(self.plot, self.data)
        self.fig.canvas.mpl_connect("motion_notify_event", self.cursor.mouseMove)  # привязываем события к обработчикам
        self.fig.canvas.mpl_connect("button_press_event", self.mousePress)

    def mousePress(self, event):  # обработчик события, нажатия кнопки мыши
        if not event.inaxes:
            return
        if self.cursor.active:
            x, y, index = self.cursor.ly.get_xdata(), self.cursor.lx.get_ydata(), self.cursor.index  # получение
            # текущих значений вертикальной и горизонтальной линий и индекса графика
            #scat = self.plot.scatter(x, y, s=50)  # ставим маркер на график, толщина 50 попугаев
            markers = self.__markersDict.get(index)   # получаем линиюмаркеров
            markers.set_xdata(numpy.append(markers.get_xdata(), x))
            markers.set_ydata(numpy.append(markers.get_ydata(), y))
            self.setMarker(self, self.cursor, x, y, index)  # вызываем ф-ию обработчик того, что мы поставили маркер

    def setMarker(self, cursor, x, y, index):  # ф-ия для перегрузки, вызывается, когда ставится маркер
        pass


class NavigationToolbar(NavigationToolbar2GTK3):
    toolitems = [tool for tool in NavigationToolbar2GTK3.toolitems if
                 tool[0] in ('Home', 'Back', 'Forward', 'Pan', 'Zoom', 'Save')]


class PlotWindow(Gtk.Window):  # отдельное окно с графиком
    def __init__(self, title="Figure"):
        Gtk.Window.__init__(self, title=title)
        self.set_property("width_request", 400)
        self.set_property("height_request", 300)
        self.plotCanvas = PlotCanvas()  # график
        self.toolbar = NavigationToolbar(self.plotCanvas, self)  # toolbar matplotlib'a

        self.markerImage = Gtk.Image()  # изображение маркера
        self.markerImage.set_from_file("images/marker25x25.png")
        self.rebuildImage = Gtk.Image(stock=Gtk.STOCK_EXECUTE)  # изображение шестеренок

        self.rebuildButton = Gtk.Button(label=None, image=self.rebuildImage)  # кнопка перекомпановки графиков
        self.rebuildButton.set_tooltip_text("Изменить конфигурацию графиков")
        self.setMarkerToggleButton = Gtk.ToggleButton(label=None, image=self.markerImage)  # кнопка-переключатель,
        # при нажании на которую можно ставить маркеры
        self.setMarkerToggleButton.connect("toggled", self.setMarkerToggleButton_Click)
        self.setMarkerToggleButton.set_tooltip_text("Разрешить ставить маркеры")

        self.customToolBox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        self.customToolBox.pack_start(self.toolbar, False, False, 1)
        self.customToolBox.pack_end(self.rebuildButton, False, False, 0)
        self.customToolBox.pack_end(self.setMarkerToggleButton, False, False, 0)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        self.box.pack_start(self.plotCanvas, True, True, 0)
        self.box.pack_start(self.customToolBox, False, False, 1)
        self.add(self.box)

    def setMarkerToggleButton_Click(self, button):
        self.plotCanvas.cursor.active = button.get_active()     # делаем курсор активным/неактивным


if __name__ == "__main__":
    PlotWindow().show_all()
    Gtk.main()
