import Plot
import gi
gi.require_version('WebKit', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import WebKit, Gtk
from matplotlib.backends.backend_gtk3 import (
    NavigationToolbar2GTK3 as NavigationToolbar)
from matplotlib.backends.backend_gtk3agg import (
    FigureCanvasGTK3Agg as FigureCanvas)


class Pult:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("interface.glade")
        self.window = self.builder.get_object("window1")
        self.scrolledWindow = self.builder.get_object("scrolledwindow1")
        self.box = self.builder.get_object("box3")  # бокс под виджет
        self.window.connect("delete-event", self.delete_event)
        self.window.set_title("Webkit")
        self.webview = WebKit.WebView()
        self.webview.open("file:///home/artem/Pyhtml/drawingGPX.html")
        self.scrolledWindow.add(self.webview)
        self.window.add(self.scrolledWindow)
        self.canvas = Plot.PlotCanvas()
        self.canvas.set_property("expand", False)

        self.box.pack_start(self.canvas, True, True, 0)

        # Create toolbar
        self.toolbar = NavigationToolbar(self.canvas, self.box)
        self.box.pack_start(self.toolbar, False, False, 0)

        self.canvas.loadGpx("GPXCreator/testGPX.gpx")

        self.window.show_all()
        Gtk.main()

    def delete_event(self, widget, event, data=None):
        Gtk.main_quit()


p = Pult()
