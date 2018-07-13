# Модуль работы с данными


class Data:     # класс данных одного файла измерений, сделано для удобства
    def __init__(self):
        self.measurementNumber = []     # список с номером измерений
        self.longitude = []
        self.latitude = []
        self.magnitude = []
        self.elevation = []

    def append(self, mN, lon, lat, mag, el):
        self.measurementNumber.append(mN)
        self.longitude.append(lon)
        self.latitude.append(lat)
        self.magnitude.append(mag)
        self.elevation.append(el)

    def __getitem__(self, key):     # возвращает объект по ключу

        class __SingleDimentionData:  # данные одного измерения
            def __init__(self, mN, lon, lat, mag, el):
                self.measurementNumber = mN  # номером измерения
                self.longitude = lon
                self.latitude = lat
                self.magnitude = mag
                self.elevation = el

        return __SingleDimentionData(self.measurementNumber[key], self.longitude[key],
                                     self.latitude[key], self.magnitude[key], self.elevation[key])


class DataWorker:
    def __init__(self):
        self.dataLists = []  # список списков данных данных

    def loadData(self, path):   # загружаем данные из файла в dataList
        file = open(path, 'r')
        lines = [line for line in file]     # разделяем файл на строки
        tokens = [i.split("\t") for i in lines]   # парсим строки на токены с разделителем \t
        dataList = [[]]


d = Data()
d.append(1, 1, 1, 1, 1)
d.append(1, 2, 3, 4, 5)

print(d[1].longitude)