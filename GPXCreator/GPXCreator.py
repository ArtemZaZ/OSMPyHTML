import LogParser
import gpxpy.gpx
import gpxpy.parser
import time as t

gpx = gpxpy.gpx.GPX()

gpx_route = gpxpy.gpx.GPXRoute()
gpx.routes.append(gpx_route)

for i in LogParser.LatLon:
    gpx_route.points.append(gpxpy.gpx.GPXRoutePoint(i[1], i[2], vertical_dilution=i[0], horizontal_dilution=i[3]))    # количество отсчетов запихано пока в вертикальную дисперсию

print('Created GPX:', gpx.to_xml())

file = open("testGPX.gpx", "w")

file.write(gpx.to_xml())
file.close()
