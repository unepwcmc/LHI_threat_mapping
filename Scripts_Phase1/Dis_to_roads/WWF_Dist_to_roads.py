#Python 2.7.5 (default, May 15 2013, 22:43:36) [MSC v.1500 32 bit (Intel)] on win32
#Type "copyright", "credits" or "license()" for more information.
#>>> 
# Script created to separate one shapefile in multiple ones by one specific
# attribute

# Example for a Inputfile called "my_shapefile" and a field called "my_attribute"

import sys, os
import os
import arcpy
from arcpy import env

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
PP_list_fishnet=[]
PP_list_temp=[]
PP_list_roads=[]
for row in cursor:
    t=row.getValue(field)
    PP_list_temp.append(t)
    for i in PP_list_temp:
        t=str(i)
    g = t.replace(" ", "_")
    PP_list_temp.append(g)
    for i in PP_list_temp:
        g=str(i)+ "_fishnet"
        h=str(i)+ "_roads"
    PP_list_roads.append(h)
    PP_list_fishnet.append(g)
    PP_list_roads.sort()
    PP_list_fishnet.sort()
#print PP_list_roads

#Loop over the roads file in each GDB to split into different road types
for gdb in gdbList:
    if gdb=="Global_Processing.gdb":
        pass
    else:
        arcpy.env.workspace = gdb #--change working directory to each GDB in list
        WSpace=arcpy.env.workspace
        #arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(r"C:\Data\WWF\Processing\WWF_5min_grid_Moll.prj")
        fclist = arcpy.ListFeatureClasses()  
        for fc in fclist:
            for i in  PP_list_roads:
                # SPLIT OUT THE ROADS LAYER BY FUNCTIONAL CLASS AND CREATE NEW LAYERS FOR EACH CLASS
                if fc==i:
                    pos= fc.index('_roads')
                # CONVERT THE GRID CELLS TO POINTS(CENTROIDS)
                    if  arcpy.Exists(fc[:pos] + "_fishnet_GridToPoint"):
                        print fc[:pos] + "_fishnet_GridToPoint" + " exists - skipping file creation"
                    else:
                        #arcpy.FeatureToPoint_management(fc,fc + "_GridToPoint",point_location="CENTROID")
                        print "converting the grid cells to points %s" %fc[:pos] + "_fishnet"
                 # PROJECT TO WGS84    
                    if arcpy.Exists(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84"):
                        print fc[:pos] + "_GridToPoint" + "_WGS84" + " exists - skipping file creation"   
                    else:
                        #arcpy.Project_management(fc + "_GridToPoint",fc + "_GridToPoint" + "_WGS84",out_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]",transform_method="#",in_coor_system="PROJCS['World_Mollweide',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mollweide'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],UNIT['Meter',1.0]]")
                        print "projecting s%" + fc[:pos] + "_fishnet_GridToPoint" + " to WGS84" 
                    fullPath = os.path.join(WSpace, fc)
          # Reads My_shapefile for different values in the attribute
                    rows = arcpy.SearchCursor(fullPath)
                    row = rows.next()
                    attribute_types = set([])
                    while row:
                        attribute_types.add(row.FCLASS) #<-- CHANGE my_attribute to the name of your attribute
                        row = rows.next()
                    result = list(attribute_types)
                    result.sort
                    arcpy.env.overwriteOutput=True

                    for i in range(len(result)):
                        if result[i] == 0:
                            result[i] = 'Unspecified'
                        if result[i] == 1:
                            result[i] = 'Highway'
                        if result[i] == 2:
                            result[i] = 'Primary'
                        if result[i] == 3:
                            result[i] = 'Secondary'
                        if result[i] == 4:
                            result[i] = 'Tertiary'
                        if result[i] == 5:
                            result[i] = 'Local_Urban'
                        if result[i] == 6:
                            result[i] = 'Trail'
                        if result[i] == 7:
                            result[i] = 'Private'

#Make a list of tuples with FClass and correspondng attribute value
                    zipped=zip(list(attribute_types),result)                       
                    
                    #for field in lstFields:
                    for j,k in zipped:
                        near_features= fc + k 
                      #  else:   
                    #AND CALCULATE DISTANCE FROM POINT TO NEAREST ROAD (BY CLASS OF ROAD)
                        if len(arcpy.ListFields(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84","NEAR_FID" + k))>0:  
                            print "Field exists not calculating nearest distance %s" %k
                        else:
                            arcpy.Near_analysis(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84",near_features,search_radius="100 Kilometers",location="NO_LOCATION",angle="NO_ANGLE",method="GEODESIC")
                            print "calculating nearest distance %s" %fc[:pos] + "_fishnet_GridToPoint" + "_WGS84",near_features
                            arcpy.AlterField_management(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84","NEAR_FID","NEAR_FID" + "%s" %k,"NEAR_FID" + "%s" %k)
                            print "appending field name %s" %fc + "NEAR_FID" + "%s" %k
                            arcpy.AlterField_management(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84","NEAR_DIST","NEAR_DIST" + "%s" %k,"NEAR_DIST" + "%s" %k)
                            print "appending field name %s" %fc + "NEAR_DIST" + "%s" %k

#END
