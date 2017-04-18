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
Raster_list_acces_port=[]
PP_list_temp=[]
Raster_list_acces_road=[]
Raster_list_acces_road_cats=[]
for row in cursor:
    t=row.getValue(field)
    PP_list_temp.append(t)
    for i in PP_list_temp:
        t=str(i)
    g = t.replace(" ", "_")
    PP_list_temp.append(g)
    for i in PP_list_temp:
        g=str(i)+ "_access_risk_port"
        h=str(i)+ "_access_risk_road"
        #t=str(i)+ "_access_risk"
    Raster_list_acces_port.append(g)
    Raster_list_acces_road.append(h)
    #Raster_list_acces_road_cats.append(t)
    Raster_list_acces_port.sort()
    Raster_list_acces_road.sort()
    #Raster_list_acces_road_cats.sort()
    
#Loop over the roads file in each GDB to split into different road types
for gdb in gdbList:
    if gdb=="Global_Processing.gdb":
        pass
    else:
        arcpy.env.workspace = gdb #--change working directory to each GDB in list
        WSpace=arcpy.env.workspace
        #arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(r"C:\Data\WWF\Processing\WWF_5min_grid_Moll.prj")
        rasters = arcpy.ListRasters("*", "GRID")
        for raster in rasters:
            for i in Raster_list_acces_road:
                if raster==i:
                    index = str(raster).find('_access_risk')            
                    try:
                   # Set local variables
                        out_data = "C:/Data/WWF/Final_layers/" + str(raster[:index]) + "_access_risk_road" + ".tif"
                        # Execute Rename
                        #arcpy.Rename_management(in_data, out_data)
                        #print  in_data + " renamed "
                        arcpy.CopyRaster_management(raster,out_data,"#","#","#","NONE","NONE","#","NONE","NONE")
                        print "Copied: " + raster  
                    except:
                        print "Failed to copy: " + raster   


# end time
print 'finished run: %s\n' % (datetime.datetime.now() - start)
