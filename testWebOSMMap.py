#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gi
gi.require_version('WebKit', '3.0')
gi.require_version('Gtk', '3.0')
from gi.repository import WebKit, Gtk

window = Gtk.Window()
window.set_default_size(800, 600)

def on_destroy(window):
    Gtk.main_quit()
window.connect("destroy",on_destroy)

window.set_title("Webkit")
webview = WebKit.WebView()
webview.open("file:///home/artem/Pyhtml/drawingGPX.html")
scrolledWindow = Gtk.ScrolledWindow()
scrolledWindow.add(webview)
window.add(scrolledWindow)

window.show_all()

Gtk.main()
