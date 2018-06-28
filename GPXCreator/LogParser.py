import time
f = open("07_12_47_log.txt", "r")
l = [line.strip() for line in f]
data = [i.split("\t") for i in l]
LatLon = [[q, float(i[2]), float(i[3]), int(i[1])] for q, i in enumerate(data[1:], start=1)]
print(len(LatLon))
LatLon[:] = [x for i, x in enumerate(LatLon, start=1)] #if (i % 10 == 0)]
f.close()

print(len(LatLon))
