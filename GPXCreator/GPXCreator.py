import LogParser
import gpxpy.gpx

gpx = gpxpy.gpx.GPX()

gpx_route = gpxpy.gpx.GPXRoute()
gpx.routes.append(gpx_route)

for i in LogParser.LatLon:
    gpx_route.points.append(gpxpy.gpx.GPXRoutePoint(i[0], i[1], elevation=i))

print('Created GPX:', gpx.to_xml())

file = open("testGPX.gpx", "w")

file.write(gpx.to_xml())
file.close()