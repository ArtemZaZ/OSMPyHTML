# парсер логи из txt файлов
f = open("пролет над врезкой1.txt", "r")
l = [line.strip() for line in f]    # проходимся по каждой линии и создаем список
data = [i.split("\t") for i in l]   # проходимся по каждой линии и разбиваем из на списки по разделителю \t
LatLon = [[q, float(i[6][1:]), float(i[5][1:]), int(i[1]), int(i[2]), int(i[3])] for q, i in enumerate(data[1:], start=1)]    # из полученных
# списков берем значения, номера измерения, долготы, широты
print(len(LatLon))
LatLon[:] = [x for i, x in enumerate(LatLon, start=1)] #if (i % 10 == 0)]  # можно брать одно из 10 знвчений
f.close()


print(len(LatLon))
