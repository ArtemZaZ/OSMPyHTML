import gpxpy
from gpxpy import gpx
# Модуль работы с данными


class Data:     # класс данных одного файла измерений, сделано для удобства
    def __init__(self, name):
        self.name = name  # имя траектории
        self.measurementNumber = []     # список с номером измерений
        self.longitude = []
        self.latitude = []
        self.magnitudeX = []
        self.magnitudeY = []
        self.magnitudeZ = []
        self.elevation = []
        self.plotMarkers = []   # маркеры с графиков данной траектории измерений

    def append(self, mN, lon, lat, magX, magY, magZ, el):
        self.measurementNumber.append(mN)
        self.longitude.append(lon)
        self.latitude.append(lat)
        self.magnitudeX.append(magX)
        self.magnitudeY.append(magY)
        self.magnitudeZ.append(magZ)
        self.elevation.append(el)

    def __getitem__(self, key):     # возвращает объект по ключу

        class __SingleDimentionData:  # данные одного измерения дополнительный класс для того, чтобы можно было дальше
            # удобнее оперировать с данными
            def __init__(self, mN, lon, lat, magX, magY, magZ, el):
                self.measurementNumber = mN  # номером измерения
                self.longitude = lon
                self.latitude = lat
                self.magnitudeX = magX
                self.magnitudeY = magY
                self.magnitudeZ = magZ
                self.elevation = el

        return __SingleDimentionData(self.measurementNumber[key], self.longitude[key],
                                     self.latitude[key], self.magnitudeX[key], self.magnitudeZ[key],
                                     self.magnitudeY[key], self.elevation[key])


class DataWorker:
    def __init__(self):
        self.dataLists = [] # список списков данных данных Routes

    def loadData(self, path):   # загружаем данные из файла в dataList
        file = open(path, 'r')
        lines = [line for line in file]     # разделяем файл на строки
        tokens = [i.split("\t") for i in lines]   # парсим строки на токены с разделителем \t
        data = Data(path.split("/.")[-1])   # берем название файла
        for i, took in enumerate(tokens[1:], start=1):     # идем по токенам с нумерацией, начиная с 1
            data.append(mN=i, lon=float(took[5][1:]), lat=float(took[6][1:]),
                        magX=int(took[1]), magY=int(took[2]), magZ=int(took[3]), el=float(took[7]))
        self.dataLists.append(data)
        file.close()

    def loadSelfDataToGpxRoute(self, path):     # загружает все распарсенные данные в gpx траектории
        file = open(path, 'w')

        gpx = gpxpy.gpx.GPX()   # создаем gpx
        for data in self.dataLists:     # проходимся по каждому маршруту
            gpxRoute = gpxpy.gpx.GPXRoute()     # создаем маршрут
            gpx.routes.append(gpxRoute)     # добавляем маршрут

            for i in data:  # проходимся по каждому измерению в маршруте
                gpxRoute.points.append(gpxpy.gpx.GPXRoutePoint(longitude=i.longitude, elevation=i.elevation,    # добавляем точки
                                                               latitude=i.latitude))
        file.write(gpx.to_xml())    # записываем в файл
        file.close()

    def loadMarkersToGpxPoint(self, path):  # загружает все маркеры с matplotlib в gpx c именем path
        file = open(path, 'w')
        gpx = gpxpy.gpx.GPX()
        for data in self.dataLists:
            for marker in data.plotMarkers:     # проходимся по каждому маркеру
                gpxWpt = gpxpy.gpx.GPXWaypoint(longitude=marker.longitude, elevation=marker.elevation,
                                               latitude=marker.latitude)
                gpx.waypoints.append(gpxWpt)
        file.write(gpx.to_xml())
        file.close()



"""
dataWorker = DataWorker()
dataWorker.loadData("Выборг/Участок2/пролет над врезкой1.txt")
dataWorker.loadData("Выборг/Участок2/пролет над врезкой2.txt")
dataWorker.loadData("Выборг/Участок2/пролет над врезкой3.txt")
dataWorker.loadSelfDataToGpxRoute("GPXRoutes.gpx")
"""
