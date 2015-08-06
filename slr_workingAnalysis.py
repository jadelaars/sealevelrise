import slr
import arcpy
import time
from datetime import datetime as dt

start = dt.now()
print start

mxdPath = r"C:\\Users\\jadelaars\\Desktop\\ANALYSIS3.mxd"
mxd = arcpy.mapping.MapDocument(mxdPath)
#domain = 'IMPACTED_LAYERS'

haz = slr.list_domain(mxdPath,'Hazards')
points = slr.list_domain(mxdPath,'Points')
polygons = slr.list_domain(mxdPath,'Polygons')
lines = slr.list_domain(mxdPath,'Lines')


for p in points:
    print str(p)
    slr.point(p,haz)


for polygon in polygons:
    print str(polygon)
    slr.poly(polygon,haz)



for l in lines:
    print str(1)
    slr.line(1,haz)



