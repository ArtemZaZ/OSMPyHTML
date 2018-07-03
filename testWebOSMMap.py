#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gi
gi.require_version('WebKit', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import WebKit, Gtk
from matplotlib.figure import Figure
from matplotlib.backends.backend_gtk3 import (
    NavigationToolbar2GTK3 as NavigationToolbar)
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)
import numpy as np
import gpxpy.gpx
from datetime import timedelta
import Plot
import threading

class Pult:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("interface.glade")
        self.window = self.builder.get_object("window1")
        self.scrolledWindow = self.builder.get_object("scrolledwindow1")
        #self.box = self.builder.get_object("box3")  # бокс под виджет
        #self.box5 = self.builder.get_object("box5")  # бокс под виджет

        self.window.connect("delete-event", self.delete_event)
        self.window.set_title("Webkit")
        self.webview = WebKit.WebView()
        self.webview.open("file:///home/artem/Pyhtml/drawingGPX.html")
        self.scrolledWindow.add(self.webview)

        self.LatLon = []

        gpxFile = open("GPXCreator/testGPX.gpx")
        gpx = gpxpy.parse(gpxFile)
        for route in gpx.routes:
            for point in route.points:
                self.LatLon.append([point.vertical_dilution, point.latitude, point.longitude, point.horizontal_dilution])
                
        f = Figure(figsize=(5, 4), dpi=100)
        a = f.add_subplot(1, 1, 1)
        t = [i[0] for i in self.LatLon]
        s = [i[3] for i in self.LatLon]
        a.plot(t, s)

        #self.canvas = Plot.PlotCanvas()
        #self.box.pack_start(self.canvas, True, True, 0)

        # Create toolbar
        #self.toolbar = NavigationToolbar(self.canvas, self.canvas.figure)
        #self.box.pack_start(self.toolbar, True, True, 0)
        #self.canvas.loadGpx("GPXCreator/testGPX.gpx")

        #self.canvas.draw()

        self.P = Plot.PlotWindow()
        self.P.plotCanvas.loadGpx("GPXCreator/testGPX.gpx")

        def loadMarkers(plotCanvas, cursor):
            self.loadToGpx()    # ставим маркер
            self.webview.reload()   # обновляем html страницу

        self.P.plotCanvas.setMarker = loadMarkers
        self.P.show_all()
        self.window.show_all()
        Gtk.main()

    def delete_event(self, widget, event, data=None):
        Gtk.main_quit()
        open("GPXCreator/markers.gpx", 'w').close()

    def loadToGpx(self):
        gpxMarkerFile = open("GPXCreator/markers.gpx", 'w')
        gpx = gpxpy.gpx.GPX()

        for marker in self.P.plotCanvas.markers:    # по каждому маркеру
            gpxWpt = gpxpy.gpx.GPXWaypoint(longitude=self.P.plotCanvas.tastyData[2][int(marker[0])],
                                           latitude=self.P.plotCanvas.tastyData[1][int(marker[0])])  #
            #  значение берем по номеру исчисления, т.е. по x маркера
            gpx.waypoints.append(gpxWpt)

        gpxMarkerFile.write(gpx.to_xml())
        gpxMarkerFile.close()


p = Pult()

