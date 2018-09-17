#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gi
import FileServer
import Plot
import DataWorker
import TraectoryListBoxRow
import WarningDialog
gi.require_version('WebKit', '3.0')
gi.require_version('Gtk', '3.0')
gi.require_version('Soup', '2.4')
from gi.repository import WebKit, Gtk, Soup


class Pult:
    def __init__(self):
        """развертываем интерфейс из interface.glade"""
        self.builder = Gtk.Builder()
        self.builder.add_from_file("interface.glade")

        # главное окно с аттрибутами
        self.window = self.builder.get_object("MainWindow")
        self.mapScrolledWindow = self.builder.get_object("MapScrolledWindows")
        self.listBox = self.builder.get_object("ListBox")
        self.traectoryFileChooserButton = self.builder.get_object("TraectoryFileChooserButton")
        self.addTraectoryButton = self.builder.get_object("AddTraectoryButton")
        self.clearAllButton = self.builder.get_object("ClearAllButton")
        self.updateButton = self.builder.get_object("UpdateButton")
        self.clearAllButton.connect("clicked", self.clearAllButton_Click)
        self.addTraectoryButton.connect("clicked", self.addTraectoryButton_Click)
        self.updateButton.connect("clicked", self.updateButton_Click)

        self.window.connect("delete-event", self.delete_event)
        self.window.set_title("Webkit")
        self.webview = WebKit.WebView()
        self.webview.open("http://localhost:8000/drawingGPX.html")  # если делать через file:///... то нельзя будет
        # сохранять куки
        self.mapScrolledWindow.add(self.webview)

        self.cookiejar = Soup.CookieJarText.new("cookie.txt", False)  # хрень для работы с куки
        self.cookiejar.set_accept_policy(Soup.CookieJarAcceptPolicy.ALWAYS)
        self.session = WebKit.get_default_session()  # получаем текущую сессию от webkit
        self.session.add_feature(self.cookiejar)  # и добавляем в нее хрень для работы с куки

        self.plots = []  # список с графиками

        self.dataWorker = DataWorker.DataWorker()  # обработчик данных

        self.colorGenerator = TraectoryListBoxRow.DefaultColors.generator()

        self.window.show_all()
        Gtk.main()

    def addRowToListBox(self, listBox, row):
        def deleteTraectoryFunc(row, w):  # тут весь процесс удаления траекторий
            if w is None:  # удаляем все без каких-либо предупреждений ( была вызвана ф-ия очистить все)
                name = row.label.get_text()
                self.dataWorker.removeDataByName(name)  # удаляем траекторию из dataWorker'a по названию row
                self.removePlotInPlotListByName(name)  # закрываем и удаляем график
                listBox.remove(row)  # удаляем row
                self.updateWebMapWorker()  # обновляем web
                return False
            else:  # предупреждаем об удалении траектории(удаляется одна траектория)
                warning = WarningDialog.WarningDialog(self.window, "Удалить траекторию?")
                response = warning.run()
                if response == Gtk.ResponseType.OK:  # нажата кнопка ок
                    name = row.label.get_text()
                    self.dataWorker.removeDataByName(name)  # удаляем траекторию из dataWorker'a по названию row
                    self.removePlotInPlotListByName(name)  # закрываем и удаляем график
                    listBox.remove(row)  # удаляем row
                    self.updateWebMapWorker()  # обновляем web
                warning.destroy()  # закрываем окно
                return True

        row.deleteRowCallBack = deleteTraectoryFunc  # заглушка, вызывается при нажатии любой из кнопок удаления
        # траектории
        try:
            # берем цвет из генератора
            row.colorButton.set_rgba(self.colorGenerator.__next__()[1])
        except StopIteration:
            # создаем новый генератор
            self.colorGenerator = TraectoryListBoxRow.DefaultColors.generator()
            row.colorButton.set_rgba(self.colorGenerator.__next__()[1])
        listBox.add(row)

    def addPlotToPlotList(self, plotList, plot):
        def loadMarkers(plotCanvas, cursor, x, y, index):  # обработчик установки маркера на график, ставит маркер на карте
            plotCanvas.data.plotMarkers.append(plotCanvas.data[x])
            self.dataWorker.loadMarkersToGpxPoint("markers.gpx")
            self.webview.reload()  # обновляем html страницу

        def deletePlot(plot, event):    # обработчик удаления окна графика - удаляет и строку с траекторией
            request = True
            for row in self.listBox:
                if row.label.get_text() == plot.get_title():
                    request = row.deleteRowCallBack(row, True)
                    break
            return request

        plot.connect("delete-event", deletePlot)
        plot.plotCanvas.setMarker = loadMarkers  # запихиваем обработчик в plotCanvas

        plot.show_all()
        plotList.append(plot)

    def removePlotInPlotListByName(self, name):
        for i in range(len(self.plots)):
            if self.plots[i].plotCanvas.data.name == name:
                self.plots[i].destroy()  # закрываем окно
                del self.plots[i]  # удаляем график
                break

    def updateWebMapWorker(self):  # обновляем данные карты
        self.dataWorker.loadSelfDataToGpxRoute("GPXRoutes.gpx")
        self.dataWorker.loadMarkersToGpxPoint("markers.gpx")
        self.webview.reload()  # обновляем html страницу

    def delete_event(self, widget, event, data=None):
        [plot.destroy() for plot in self.plots]
        Gtk.main_quit()
        open("markers.gpx", 'w').close()  # чистим файл с маркерами

        # глушняк с маркерами
        # self.cookiejar.set_cookie(temp, "cas=dsddas")

        # self.cookie = self.cookiejar.all_cookies()  # заглушка для проверки куки
        # self.cookiejar.save()

    """ обработчики нажатия кнопок"""

    def addTraectoryButton_Click(self, w):
        dialog = Gtk.FileChooserDialog("Traectory Chooser", self.window, Gtk.FileChooserAction.OPEN,
                                       (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        filterRoute = Gtk.FileFilter()
        filterRoute.set_name("Magnitude filter (*.mag)")
        filterRoute.add_pattern("*.mag")
        dialog.add_filter(filterRoute)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            traectoryPath = dialog.get_filename()
            if traectoryPath is not None:
                #try:
                    data = self.dataWorker.loadData(traectoryPath)  # загружаем данные из файла
                    plot = Plot.PlotWindow(title=data.name)  # создаем окно с графиком
                    self.addPlotToPlotList(self.plots, plot)
                    plot.plotCanvas.loadData(data)
                    row = TraectoryListBoxRow.TraectoryListBoxRow(data.name)  # берем только имя файла
                    self.addRowToListBox(self.listBox, row)  # добавляем row в listBox
                    self.updateWebMapWorker()
                    self.window.show_all()
                #except:
                #    warning = WarningDialog.WarningDialog(self.window, "Не удалось загрузить траекторию\n"
                #                                                       "  проверьте целостность файла")
                #    warning.run()
                #    warning.destroy()
        dialog.destroy()

    def clearAllButton_Click(self, w):  # очистка всех траекторий
        warning = WarningDialog.WarningDialog(self.window, "Удалить траектории?")
        response = warning.run()
        if response == Gtk.ResponseType.OK:
            for row in self.listBox:
                row.deleteRowCallBack(row, None)  # чистим все, None - заглушка, чтоб не реализовывать более сложную
                #  логику, вместо None должен быть виджет кнопка, т.к. это калл-бэк ф-ия
        warning.destroy()

    def updateButton_Click(self, w):  # обновить web
        self.updateWebMapWorker()


FileServer.server.start()  # запускаем сервер
p = Pult()  # запускаем приложение
