# парсер логи из txt файлов
f = open("07_12_47_log.txt", "r")
l = [line.strip() for line in f]    # проходимся по каждой линии и создаем список
data = [i.split("\t") for i in l]   # проходимся по каждой линии и разбиваем из на списки по разделителю \t
LatLon = [[q, float(i[2]), float(i[3]), int(i[1])] for q, i in enumerate(data[1:], start=1)]    # из полученных
# списков берем значения, номера измерения, долготы, широты
print(len(LatLon))
LatLon[:] = [x for i, x in enumerate(LatLon, start=1)] #if (i % 10 == 0)]  # можно брать одно из 10 знвчений
f.close()


print(len(LatLon))
