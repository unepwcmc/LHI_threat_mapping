#Python 2.7.5 (default, Dec 10 2013, 22:43:36) [MSC v.1500 32 bit (Intel)] on win32
#Type "copyright", "credits" or "license()" for more information.
#Python code for ArcMap 10.2, Python v 2.7

# Code development by Brian O'Connor September 2016
import sys, os
import os
import arcpy
from arcpy import env
import time

beginTime = time.clock()

# Name: WWF_Biome_RasterProcessing.py
# Description: Processes raster data by interescting them with fishnet gird
# Notes - 


#set to overwrite existing outputs
arcpy.env.overwriteOutput = True

#set workspace for inputs and outputs
arcpy.env.workspace=r"C:\Data\WWF\Processing\Global_Processing.gdb" #CHANGE AS NEEDED
#tempFolder="C:\Data\WWF\Processing\Global_Processing.gdb"
InData=[]
#for x in tempFolder:
rasterlist=arcpy.ListRasters("*_Production","")# CHANGE Wild card if needed
for raster in rasterlist:
    #print (raster)
    InData.append(str(raster))
print "there are " + "%s" %len(InData) + " crop layers to be processed"

#Get list of BIOME features by reading their name from parent file, i.e. WWF Biomes
arcpy.env.workspace=r"C:\Data\WWF\Processing" #CHANGE AS NEEDED
fc = r"C:\Data\WWF\Study_scope\WWF_PP_Terr.gdb\WWF_PP_Terr" #CHANGE AS NEEDED
field = "FLAG_NAME" #CHANGE AS NEEDED
cursor = arcpy.SearchCursor(fc)
PP_list_temp=[]
PP_list=[]
PP_list_buff=[]
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
        h=str(i)+ "_sp_buff"
        g=str(i)+ "_sp_buff_fishnet"
        s=str(i)+ "_fishnet"
    PP_list_buff.append(h)
    PP_list_fishnet.append(s)
    #PP_list_fishnet_buff.append(g)
    PP_list.sort()
    PP_list_buff.sort()
    PP_list_fishnet.sort()
    #PP_list_fishnet_buff.sort()
    #Fishnet_list = PP_list_fishnet + PP_list_fishnet_buff
   # PP_buffer_list=PP_list+PP_list_buff

#SET UP Loop - list all the GDBs in the workspace 
 
workspaces = arcpy.ListWorkspaces("*", "FileGDB")
for i in workspaces:
    arcpy.env.overwriteOutput=True  
    if i==r"C:\Data\WWF\Processing\Global_Processing.gdb":
        pass # skip the gdb where raw data are stored
    else:
        arcpy.env.workspace=i # set workspace as GDB with a biome name
        fclist =  arcpy.ListFeatureClasses()
        #rasters = arcpy.ListRasters("*", "GRID")
        for fc in fclist:
            for t in PP_list_fishnet:
                if fc==t: # if the GDB name matches the respective name of a biome in the biome list name, ensures that a different biome is processed on each loop 
                    for raster in InData:
            #run zonal stats
                        try:
                            #PLEASE modify the following lines according to the raster data being used
                            arcpy.gp.ZonalStatisticsAsTable_sa(t,"OBJECTID","C:\Data\WWF\Processing\Global_Processing.gdb" + "\\" + raster,i + "\\" + "ZonalStats" + "_" + "%s" %raster,"DATA","ALL")# performs zonal stats on raster cells in fishnet grid 
                            print "calculating ALL of the stats per grid cell " + "%s" %t + " " + "%s" %raster
                            # performs join on the zonal table back to the attribute table of fishnet
                            arcpy.JoinField_management(t,"OBJECTID",i + "\\" + "ZonalStats" + "_" + "%s" %raster,"OBJECTID","MEAN")
                            print "joining MEAN to fishnet grid " + "%s" %t
                             # alters the field name of the appended column based on the raster quantity #CHANGE AS NEEDED
                            arcpy.AlterField_management(t,"MEAN","Mean_" + "%s" %raster + "_t","Mean " + "%s" %raster[0:-11] + " production (tonnes) in 2000")
                            print "appending field name" + "%s" %t
                            # adds another field,e.g. for the calculation of crop density
                            arcpy.AddField_management(t, "%s" %raster[0:-10] + "_prod_dens", "DOUBLE", "", "", "", "refcode", "NULLABLE", "REQUIRED")
                            print "adding field for calculation of crop prodcution density"
                            # calculates value for the above field
                            arcpy.CalculateField_management(t, , "Mean_" + "%s" %raster + "_tonnes"/"!AREA_GEO!", "PYTHON", "")
                            #print "calculating tonnes per square kilometre" + "%s" %t
                        except:
                            print "could not perform stats calc" + " " + "%s" %fc + " " + "%s" %raster


#To delete unwanted fields:

fieldNameList=[]
fields=arcpy.ListFields(fc,'MEAN_1*')
for field in fields:
    fieldNameList.append(field.name)
arcpy.DeleteField_management(fc,fieldNameList)

