#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gi
gi.require_version('WebKit', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Soup', '2.4')
from gi.repository import WebKit, Gtk, Soup
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3 import (
    NavigationToolbar2GTK3 as NavigationToolbar)
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
import gpxpy.gpx
import Plot
import DataWorker
import TraectoryListBoxRow


class Pult:
    def __init__(self):
        """развертываем интерфейс из interface.glade"""
        self.builder = Gtk.Builder()
        self.builder.add_from_file("testInterface.glade")
        self.window = self.builder.get_object("window1")
        self.mapScrolledWindow = self.builder.get_object("MapScrolledWindows")
        self.listBox = self.builder.get_object("ListBox")
        self.traectoryFileChooserButton = self.builder.get_object("TraectoryFileChooserButton")
        self.addTraectoryButton = self.builder.get_object("AddTraectoryButton")
        self.clearButton = self.builder.get_object("ClearButton")
        self.clearButton.connect("clicked", self.clearButton_Click)
        self.addTraectoryButton.connect("clicked", self.addTraectoryButton_Click)

        self.window.connect("delete-event", self.delete_event)
        self.window.set_title("Webkit")
        self.webview = WebKit.WebView()
        self.webview.open("http://localhost:8000/drawingGPX.html")  # если делать через file:///... то нельзя будет
        # сохранять куки
        self.mapScrolledWindow.add(self.webview)

        self.cookiejar = Soup.CookieJarText.new("cookie.txt", False)   # хрень для работы с куки
        self.cookiejar.set_accept_policy(Soup.CookieJarAcceptPolicy.ALWAYS)
        self.session = WebKit.get_default_session()     # получаем текущую сессию от webkit
        self.session.add_feature(self.cookiejar)    # и добавляем в нее хрень для работы с куки

        self.plots = []     # список с графиками

        self.dataWorker = DataWorker.DataWorker()
        #self.dataWorker.loadData("Выборг/Участок2/пролет над врезкой1.txt")
        #self.dataWorker.loadData("Выборг/Участок2/пролет над врезкой2.txt")
        #self.dataWorker.loadData("Выборг/Участок2/пролет над врезкой3.txt")
        #self.dataWorker.loadSelfDataToGpxRoute("GPXRoutes.gpx")

        self.window.show_all()
        Gtk.main()

    def addRowToListBox(self, listBox, row):
        def deleteTraectoryFunc(row, w):    # тут весь процесс удаления траекторий
            self.dataWorker.removeDataByName(row.label.get_text())  # удаляем траекторию из dataWorker'a по названию row
            listBox.remove(row)     # удаляем row
            self.updateWebMapWorker()   # обновляем web

        row.deleteRowCallBack = deleteTraectoryFunc     # заглушка, вызывается при нажатии любой из кнопок удаления
        # траектории
        listBox.add(row)

    def addPlotToPlotList(self, plotList, plot):
        def loadMarkers(plotCanvas, cursor, x, y):    # обработчик установки маркера на график, ставит маркер на карте
            plotCanvas.data.plotMarkers.append(plotCanvas.data[x])
            self.dataWorker.loadMarkersToGpxPoint("markers.gpx")
            self.webview.reload()   # обновляем html страницу

        plot.plotCanvas.setMarker = loadMarkers   # запихиваем обработчик в plotCanvas
        plot.show_all()
        plotList.append(plot)

    def delete_event(self, widget, event, data=None):
        Gtk.main_quit()
        open("markers.gpx", 'w').close()     # чистим файл с маркерами

        # глушняк с маркерами
        #temp = Soup.URI.new("file:///home/artem/Pyhtml/drawingGPX.html")
        #self.cookiejar.set_cookie(temp, "cas=dsddas")

        #self.cookie = self.cookiejar.all_cookies()  # заглушка для проверки куки
        #self.cookiejar.save()

    def addTraectoryButton_Click(self, w):
        traectoryPath = self.traectoryFileChooserButton.get_filename()
        if traectoryPath is not None:
            data = self.dataWorker.loadData(traectoryPath)     # загружаем данные из файла
            plot = Plot.PlotWindow()  # создаем окно с графиком
            self.addPlotToPlotList(self.plots, plot)
            plot.plotCanvas.loadData(data)
            row = TraectoryListBoxRow.TraectoryListBoxRow(data.name)     # берем только имя файла
            self.addRowToListBox(self.listBox, row)     # добавляем row в listBox
            self.updateWebMapWorker()
            self.window.show_all()

    def clearButton_Click(self, w):     # просто очистка web'a
        open("GPXRoutes.gpx", 'w').close()
        open("markers.gpx", 'w').close()
        self.webview.reload()

    def updateWebMapWorker(self):     # обновляем данные карты
        self.dataWorker.loadSelfDataToGpxRoute("GPXRoutes.gpx")
        self.webview.reload()   # обновляем html страницу


p = Pult()  # запускаем приложение






