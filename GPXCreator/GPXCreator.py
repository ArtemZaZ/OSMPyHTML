import LogParser    # тут парсится файл
import gpxpy.parser

gpx = gpxpy.gpx.GPX()   # создаем gpx

gpx_route = gpxpy.gpx.GPXRoute()    # создаем маршрут
gpx.routes.append(gpx_route)    # добавляем маршрут

for i in LogParser.LatLon:  # по списку с долготой и широтой
    gpx_route.points.append(gpxpy.gpx.GPXRoutePoint(i[1], i[2], vertical_dilution=i[3], horizontal_dilution=i[4], ))    # количество отсчетов запихано пока в вертикальную дисперсию


print('Created GPX:', gpx.to_xml())

file = open("Пролет над врезкой1.gpx", "w")

file.write(gpx.to_xml())
file.close()
