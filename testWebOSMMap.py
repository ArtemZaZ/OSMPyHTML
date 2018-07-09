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


class Pult:
    def __init__(self):
        """развертываем интерфейс из interface.glade"""
        self.builder = Gtk.Builder()
        self.builder.add_from_file("interface.glade")
        self.window = self.builder.get_object("window1")
        self.scrolledWindow = self.builder.get_object("scrolledwindow1")

        self.window.connect("delete-event", self.delete_event)
        self.window.set_title("Webkit")
        self.webview = WebKit.WebView()
        self.webview.open("file:///home/artem/Pyhtml/drawingGPX.html")
        self.scrolledWindow.add(self.webview)

        self.cookiejar = Soup.CookieJar()   # хрень для работы с куки
        self.cookiejar.set_accept_policy(Soup.CookieJarAcceptPolicy.ALWAYS)
        self.session = WebKit.get_default_session()     # получаем текущую сессию от webkit
        self.session.add_feature(self.cookiejar)    # и добавляем в нее хрень для работы с куки

        self.LatLon = []    # переменная для сохранения значений долготы, широты и т.д.

        gpxFile = open("GPXCreator/testGPX.gpx")    # открываем тестовый файл
        gpx = gpxpy.parse(gpxFile)  # парсим файл
        for route in gpx.routes:    # по каждому маршруту
            for point in route.points:  # по каждой точке
                self.LatLon.append([point.vertical_dilution, point.latitude, point.longitude, point.horizontal_dilution])   # добавляем в latlon данные точек

        self.P = Plot.PlotWindow()  # создаем окно с графиком
        self.P.plotCanvas.loadGpx("GPXCreator/testGPX.gpx")  # грузим туда график

        def loadMarkers(plotCanvas, cursor):    # обработчик установки маркера на график, ставит маркер на карте
            self.loadToGpx()    # ставим маркер, записываем в новый gpx файл
            self.webview.reload()   # обновляем html страницу

        self.P.plotCanvas.setMarker = loadMarkers   # запихиваем обработчик в plotCanvas
        self.P.show_all()
        self.window.show_all()
        Gtk.main()

    def delete_event(self, widget, event, data=None):
        Gtk.main_quit()
        open("GPXCreator/markers.gpx", 'w').close()     # чистим файл с маркерами

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

        #self.cookie = self.cookiejar.all_cookies()  # заглушка для проверки куки
        #print(self.cookie[1].get_value())


p = Pult()  # запускаем приложение

