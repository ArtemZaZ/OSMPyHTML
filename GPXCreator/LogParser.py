f = open("07_12_47_log.txt", "r")
l = [line.strip() for line in f]
data = [i.split("\t") for i in l]
LatLon = [[float(i[2]), float(i[3])] for i in data[1:]]
print(len(LatLon))
LatLon[:] = [x for i, x in enumerate(LatLon, start=1) if (i % 10 == 0)]
f.close()

print(len(LatLon))