#Python 2.7.5 (default, May 15 2013, 22:43:36) [MSC v.1500 32 bit (Intel)] on win32
#Type "copyright", "credits" or "license()" for more information.
#>>> 
# Script created to separate one shapefile in multiple ones by one specific
# attribute

# Example for a Inputfile called "my_shapefile" and a field called "my_attribute"

import sys, os
import os
import os.path
import arcpy
from arcpy import env

#Starts Geoprocessing



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
        arcpy.env.overwriteOutput = False
        #arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(r"C:\Data\WWF\Processing\WWF_5min_grid_Moll.prj")
        fclist = arcpy.ListFeatureClasses()  
        for fc in fclist:
            for i in  PP_list_roads:
                # SPLIT OUT THE ROADS LAYER BY FUNCTIONAL CLASS AND CREATE NEW LAYERS FOR EACH CLASS
                if fc==i:
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
                    
# CREATE SEPERATE FEATURE CLASSES FOR EVERY CLASS OF ROAD AND COPY THEM TO THE .GDB
            # Output a Shapefile for each different attribute
                    field="FCLASS"
                    for j,k in zipped:
                        outSHP = str(fullPath) + str(k)
                        print fullPath
                        if arcpy.Exists(fc+k):
                            print "Road layer exists - skipping file creation"
                        else:
                            arcpy.Select_analysis(fullPath, fc + k, field + "=" + str(j)) #<-- CHANGE my_attribute to the name of your attribute
                    del rows, row, attribute_types


#END
