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
geometryType = 'POINT'
gdbList = arcpy.ListWorkspaces("*", "FileGDB")

#Get list of priority places and read into a list
fc = r"C:\Data\WWF\Study_scope\WWF_PP_Terr.gdb\WWF_PP_Terr"
field = "FLAG_NAME"
cursor = arcpy.SearchCursor(fc)
PP_list_temp=[]
PP_list=[]
for row in cursor:
    t=row.getValue(field)
    PP_list_temp.append(t)
    for i in PP_list_temp:
        t=str(i)
    g = t.replace(" ", "_")
    PP_list.append(g)
    for i in PP_list:
        h=str(i)+ "_sp_buff"
    PP_list.sort()


#Loop over the GDB and read the fc from the list - to be used as a template for the fishnet  

for gdb in gdbList:
    if gdb=="Global_Processing.gdb":
        pass
    else:
        arcpy.env.workspace = gdb #--change working directory to each GDB in list
        #arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(r"C:\Data\WWF\Processing\African_Rift_Lakes.gdb\African_Rift_Lakes")
        fclist = arcpy.ListFeatureClasses()  
        for fc in fclist:
            for i in PP_list:
                if fc==i:
                    in_grid = "C:\Data\WWF\Processing\Global_Processing.gdb\WPI"
                    out_grid=  fc + "_WPI_layer"
# First, make a layer from the feature class
                    arcpy.MakeFeatureLayer_management(in_grid,out_grid)
                    #print out_grid
                    #try:
                        # select ports within the boundaries of the WWF-PP and a distance of 110km (to ensure search radius for calculating nearest distance works later on)
                    arcpy.SelectLayerByLocation_management(out_grid,"WITHIN_A_DISTANCE",fc,"110 Kilometers","NEW_SELECTION")                        
                    print "Selecting overlapping POINTS from " + "%s" %out_grid
                    # Within the previous selection sub-select ports layer which have values for both harbour size AND max vessel size
                    arcpy.SelectLayerByAttribute_management(out_grid, 'SUBSET_SELECTION', """"HARBORSIZE" <> ' '""")
                    arcpy.SelectLayerByAttribute_management(out_grid, 'SUBSET_SELECTION', """"MAX_VESSEL" <> ' '""")
                    # If features matched criteria write them to a new feature class
                    matchcount = int(arcpy.GetCount_management(out_grid)[0])
                    if matchcount == 0:
                        print('no ports matched spatial and attribute criteria')
                        arcpy.Delete_management(fc + "_ports", data_type="#")
                        print "%s" %fc + "_ports" + " deleted"
                    else:                            
                        arcpy.CopyFeatures_management(out_grid, fc + "_ports")
                        print('{0} ports that matched criteria written to {1}'.format(
                            matchcount,"%s" %fc + "_ports"))
                   # except:
                       # print "fail"

                    
print ("Total elapsed time (seconds): " + str(time.clock() - beginTime))
#Delete redundant files
                #if "ACLED_" in str(fc): #replace string to find apporiate files for deletion
                    #print "deleting " + "%s" %fc
                    #arcpy.Delete_management(fc, data_type="#")
               #else:
                    #print"No files exist for deletion in " + "%s" %gdb 

