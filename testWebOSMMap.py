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


class Pult:
    def __init__(self):
        """развертываем интерфейс из interface.glade"""
        self.builder = Gtk.Builder()
        self.builder.add_from_file("testInterface.glade")
        self.window = self.builder.get_object("window1")
        self.mapScrolledWindow = self.builder.get_object("MapScrolledWindows")
        self.listBox = self.builder.get_object("ListBox")

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

        self.dataWorker = DataWorker.DataWorker()

        self.dataWorker = DataWorker.DataWorker()
        self.dataWorker.loadData("Выборг/Участок2/пролет над врезкой1.txt")
        self.dataWorker.loadData("Выборг/Участок2/пролет над врезкой2.txt")
        self.dataWorker.loadData("Выборг/Участок2/пролет над врезкой3.txt")
        self.dataWorker.loadSelfDataToGpxRoute("GPXRoutes.gpx")

        self.P = Plot.PlotWindow()  # создаем окно с графиком
        self.P.plotCanvas.loadData(self.dataWorker.dataLists[0])

        def loadMarkers(plotCanvas, cursor, x, y):    # обработчик установки маркера на график, ставит маркер на карте
            point = plotCanvas.data[x]
            self.dataWorker.markers.append(mN=point.measurementNumber, lon=point.longitude, magX=point.magnitudeX,
                                           lat=point.latitude, magY=point.magnitudeY, el=point.elevation,
                                           magZ=point.magnitudeZ)
            self.dataWorker.loadMarkersToGpxPoint("markers.gpx")
            self.webview.reload()   # обновляем html страницу

        self.P.plotCanvas.setMarker = loadMarkers   # запихиваем обработчик в plotCanvas
        self.P.show_all()
        self.window.show_all()
        Gtk.main()

    def delete_event(self, widget, event, data=None):
        Gtk.main_quit()
        open("markers.gpx", 'w').close()     # чистим файл с маркерами

    def loadToGpx(self):
        gpxMarkerFile = open("GPXCreator/markers.gpx", 'w')     # создаем gpx файл
        gpx = gpxpy.gpx.GPX()

        for marker in self.P.plotCanvas.markers:    # по каждому маркеру
            gpxWpt = gpxpy.gpx.GPXWaypoint(longitude=self.P.plotCanvas.tastyData[2][int(marker[0])],
                                           latitude=self.P.plotCanvas.tastyData[1][int(marker[0])])  #
            #  значение берем по номеру исчисления, т.е. по x маркера
            gpx.waypoints.append(gpxWpt)    # добавляем точку в gpx файл

        gpxMarkerFile.write(gpx.to_xml())
        gpxMarkerFile.close()

        #temp = Soup.URI.new("file:///home/artem/Pyhtml/drawingGPX.html")
        #self.cookiejar.set_cookie(temp, "cas=dsddas")

        #self.cookie = self.cookiejar.all_cookies()  # заглушка для проверки куки
        #self.cookiejar.save()


p = Pult()  # запускаем приложение

