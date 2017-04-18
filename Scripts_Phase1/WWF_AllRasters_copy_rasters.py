#Python 2.7.5 (default, May 15 2013, 22:43:36) [MSC v.1500 32 bit (Intel)] on win32
#Type "copyright", "credits" or "license()" for more information.
#>>> 

#NOTE: v2 adds an extra field to the table for the ranking of threat on an ordinal scale, in addtion to the 'categories' of road access. This is to bring it closer to the method used for ports

import sys, os
import os
import arcpy
from arcpy import env

#start time
import datetime
start = datetime.datetime.now()
print 'start run: %s\n' % (start)



#Starts Geoprocessing
arcpy.env.overwriteOutput = True

myWorkspace=r"C:\Data\WWF\Processing"
arcpy.env.workspace = myWorkspace
gdbList = arcpy.ListWorkspaces("*", "FileGDB")

#Set Input Output variables
#inputFile = fc #<-- CHANGE
#outDir = u"C:\Data\WWF\Test_processes\\" #<-- CHANGE
#Get list of priority places
fc = r"C:\Data\WWF\Study_scope\WWF_PP_Terr.gdb\WWF_PP_Terr"
field = "FLAG_NAME"
cursor = arcpy.SearchCursor(fc)
PP_list_temp=[]
PP_list=[]
PP_list_fishnet=[]
#PP_list_fishnet_buff=[]
for row in cursor:
    t=row.getValue(field)
    PP_list_temp.append(t)
    for i in PP_list_temp:
        t=str(i)
    g = t.replace(" ", "_")
    PP_list.append(g)
    for i in PP_list:
        s=str(i)+ "_fishnet"
    PP_list_fishnet.append(s)
    PP_list.sort()
    PP_list_fishnet.sort()
    
#Loop over the roads file in each GDB to split into different road types
for gdb in gdbList[3:]:
    if gdb=="Global_Processing.gdb":
        pass
    else:
        arcpy.env.workspace = gdb #--change working directory to each GDB in list
        WSpace=arcpy.env.workspace
        #arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(r"C:\Data\WWF\Processing\WWF_5min_grid_Moll.prj")
        #rasters = arcpy.ListRasters("*", "GRID")
        fclist = arcpy.ListFeatureClasses()  
        for fc in fclist:
            for t in PP_list_fishnet:
                if fc==t:
                    field_names = [field.name for field in arcpy.ListFields(fc)] 
                    #print field_names [7:]
                    for name in field_names [7:]:
                        # Process: Polygon to Raster
                        inFeature = fc
                        index = str(fc).find('_fishnet')
                        outRaster = "C:/Data/WWF/Final_layers/" + str(fc[:index]) + "_" + "%s" %name  + ".tif"
                        cellSize = 10000
                        field = str(name)
                        if arcpy.Exists(outRaster):
                            print "%s" %outRaster + " exists"
                        else:
                            arcpy.FeatureToRaster_conversion(inFeature, field, outRaster, cellSize)
                            print  "printing" + "%s" %outRaster
arcpy.env.workspace = "C:/Data/WWF/Final_layers"
rasters = [raster for raster in arcpy.ListRasters() if raster.endswith('dens.tif')]
rasters2 = [raster for raster in arcpy.ListRasters() if raster.endswith('_siz.tif')]
if len(rasters)>0:
    for raster in rasters:
        print "deleting " + str(raster)
        arcpy.Delete_management(raster)
else:
    print "raster does not exist"
if len(rasters2)>0:
    for raster in rasters2:
        print "deleting " + str(raster)
        arcpy.Delete_management(raster)
else:
    print "raster does not exist"
                        


# end time
print 'finished run: %s\n' % (datetime.datetime.now() - start)
