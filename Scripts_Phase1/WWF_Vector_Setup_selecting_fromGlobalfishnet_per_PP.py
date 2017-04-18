#Python code for ArcMap 10.2, Python v 2.7
# Code development by Brian O' Connor October 2015
import sys, os
import os
import arcpy
from arcpy import env
import time

beginTime = time.clock()

# Name: CreateFishnet.py
# Description: Creates rectangular cells
# set workspace environment
myWorkspace=r"C:\Data\WWF\Processing"
arcpy.env.workspace = myWorkspace
#set to overwrite existing outputs
arcpy.env.overwriteOutput = True
# Set coordinate system of the output fishnet
#env.outputCoordinateSystem = arcpy.SpatialReference("Mollweide")

# Each output cell will be a polygon
geometryType = 'POLYGON'
gdbList = arcpy.ListWorkspaces("*", "FileGDB")

#Get list of priority places and read into a list
fc = r"C:\Data\WWF\Study_scope\WWF_PP_Terr.gdb\WWF_PP_Terr"
field = "FLAG_NAME"
cursor = arcpy.SearchCursor(fc)
PP_list_temp=[]
PP_list=[]
PP_list_buff=[]
for row in cursor:
    t=row.getValue(field)
    PP_list_temp.append(t)
    for i in PP_list_temp:
        t=str(i)
    g = t.replace(" ", "_")
    PP_list.append(g)
    for i in PP_list:
        h=str(i)+ "_sp_buff"
    PP_list_buff.append(h)
    PP_list.sort()
    PP_list_buff.sort()
print PP_list
print PP_list_buff

#Loop over the GDB and read the fc from the list - to be used as a template for the fishnet  

for gdb in gdbList:
    if gdb=="Global_Processing.gdb":
        pass
    else:
        arcpy.env.workspace = gdb #--change working directory to each GDB in list
        arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(r"C:\Data\WWF\Processing\WWF_5min_grid_Moll.prj")
        fclist = arcpy.ListFeatureClasses()  
        for fc in fclist:
            for i in PP_list_buff:
                if fc==i:
                    arcpy.env.extent = r"C:\Data\WWF\Processing\Global_Processing.gdb\landmask"
                    arcpy.env.mask = r"C:\Data\WWF\Processing\Global_Processing.gdb\landmask"
                    in_grid = "C:\Data\WWF\Processing\Global_Processing.gdb\WWF_5min_grid_Moll"
                    out_grid= gdb + "\\" + fc + "_layer"
# First, make a layer from the feature class
                    arcpy.MakeFeatureLayer_management(in_grid,out_grid)
# Select cells from the global layer which overlap the PP polygon and create a feature layer for each new selection (stored in the respective PP gdb)
                    try:
                        arcpy.SelectLayerByLocation_management(out_grid, 'intersect', fc)
                        print "Selecting overlapping grid cells from " + "%s" %fc
                        arcpy.CopyFeatures_management(out_grid, fc + "_fishnet")
                        print "writing the overlapping grid cells to a new feature class " + + "%s" %fc
                    except:
                        print "fail"

                    
print ("Total elapsed time (seconds): " + str(time.clock() - beginTime))
#Delete redundant files
                if "ACLED_" in str(fc): #replace string to find apporiate files for deletion
                    print "deleting " + "%s" %fc
                    arcpy.Delete_management(fc, data_type="#")
                else:
                    print"No files exist for deletion in " + "%s" %gdb 


                











            
    #spatial_ref = arcpy.Describe(fc).spatialReference
    desc = arcpy.Describe(fc)
    print desc.extent
    print desc.spatialReference
    print desc.name
    print desc.dataType
    arcpy.CreateFishnet_management(fc + "_fishnet",origin_coord="7570350.5012 5965313.1202",y_axis_coord="7570350.5012 5965323.1202",cell_width="10000",cell_height="10000",number_rows="#",number_columns="#",corner_coord="8037192.9762 6565844.8399",labels="NO_LABELS",template="7570350.5012 5965313.1202 8037192.9762 6565844.8399",geometry_type="POLYGON")                    
print ("Total elapsed time (seconds): " + str(time.clock() - beginTime))
