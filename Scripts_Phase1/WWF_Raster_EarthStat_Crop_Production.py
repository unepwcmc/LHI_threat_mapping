#Python 2.7.5 (default, Dec 10 2013, 22:43:36) [MSC v.1500 32 bit (Intel)] on win32
#Type "copyright", "credits" or "license()" for more information.
import sys, os
import os
import arcpy
from arcpy import env
import time
# Import system modules
from arcpy.sa import *

beginTime = time.clock()

#set to overwrite existing outputs
arcpy.env.overwriteOutput = True

#set workspace for inputs and outputs
arcpy.env.workspace=r"C:\Data\WWF\Processing\Global_Processing.gdb"
#tempFolder="C:\Data\WWF\Processing\Global_Processing.gdb"
InData=[]
#for x in tempFolder:
rasterlist=arcpy.ListRasters("*_Production","")
for raster in rasterlist:
    #print (raster)
    InData.append(str(raster))
print "there are " + "%s" %len(InData) + " crop layers to be processed"

#Get list of priority places features
arcpy.env.workspace=r"C:\Data\WWF\Processing"
fc = r"C:\Data\WWF\Study_scope\WWF_PP_Terr.gdb\WWF_PP_Terr"
field = "FLAG_NAME"
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

 
workspaces = arcpy.ListWorkspaces("*", "FileGDB")
for i in workspaces:
    arcpy.env.overwriteOutput=True  
    if i==r"C:\Data\WWF\Processing\Global_Processing.gdb":
        pass
    else:
        arcpy.env.workspace=i
        fclist =  arcpy.ListFeatureClasses()
        #rasters = arcpy.ListRasters("*", "GRID")
        for fc in fclist:
            for t in PP_list_fishnet:
                if fc==t:
                    for raster in InData:
            #run zonal stats
                        try:
                           # arcpy.gp.ZonalStatisticsAsTable_sa(t,"OBJECTID","C:\Data\WWF\Processing\Global_Processing.gdb" + "\\" + raster,i + "\\" + "ZonalStats" + "_" + "%s" %raster,"DATA","ALL")
                            #print "calculating ALL of the stats per grid cell " + "%s" %t + " " + "%s" %raster
                            arcpy.JoinField_management(t,"OBJECTID",i + "\\" + "ZonalStats" + "_" + "%s" %raster,"OBJECTID","MEAN")
                            print "joining MEAN to fishnet grid " + "%s" %t
                            arcpy.AlterField_management(t,"MEAN","Mean_" + "%s" %raster + "_t","Mean " + "%s" %raster[0:-11] + " production (tonnes) in 2000")
                            print "appending field name" + "%s" %t
                            arcpy.AddField_management(t, "%s" %raster[0:-10] + "_prod_dens", "DOUBLE", "", "", "", "refcode", "NULLABLE", "REQUIRED")
                            print "adding field for calculation of crop prodcution density"
                            #arcpy.CalculateField_management(t, , "Mean_" + "%s" %raster + "_tonnes"/"!AREA_GEO!", "PYTHON", "")
                            #print "calculating tonnes per square kilometre" + "%s" %t
                        except:
                            print "could not perform stats calc" + " " + "%s" %fc + " " + "%s" %raster


#To delete unwanted fields:

fieldNameList=[]
fields=arcpy.ListFields(fc,'MEAN_1*')
for field in fields:
    fieldNameList.append(field.name)
arcpy.DeleteField_management(fc,fieldNameList)

