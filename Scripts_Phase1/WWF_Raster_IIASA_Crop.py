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
arcpy.env.workspace=r"C:\Data\WWF\Processing"
#tempFolder="C:\Data\WWF\Processing"
InData=["CropFraction_14052014V8","field_size_10_40_cropland"]

#Get list of priority places features
fc = r"C:\Data\WWF\Study_scope\WWF_PP_Terr.gdb\WWF_PP_Terr"
field = "FLAG_NAME"
cursor = arcpy.SearchCursor(fc)
PP_list_temp=[]
PP_list=[]
PP_list_buff=[]
PP_list_fishnet=[]
PP_list_fishnet_buff=[]
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
    PP_list_fishnet_buff.append(g)
    PP_list.sort()
    PP_list_buff.sort()
    PP_list_fishnet.sort()
    PP_list_fishnet_buff.sort()
    Fishnet_list = PP_list_fishnet + PP_list_fishnet_buff
    PP_buffer_list=PP_list+PP_list_buff

#define variables for join



    
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
                            arcpy.gp.ZonalStatisticsAsTable_sa(t,"OBJECTID","C:\Data\WWF\Processing\Global_Processing.gdb" + "\\" + raster,i + "\\" + "ZonalStats" + "%s" %raster[0:7],"DATA","ALL")
                            print "calculating ALL of the stats per grid cell " + "%s" %t + " " + "%s" %raster
                            arcpy.JoinField_management(t,"OBJECTID",i + "\\" + "ZonalStats" + "%s" %raster[0:7],"OBJECTID","MEAN")
                            print "joining MEAN to fishnet grid " + "%s" %t
                            arcpy.AlterField_management(t,"MEAN","Mean_" + "%s" %raster[0:9],"Mean "+ "%s" %raster[0:9])
                            print "appending field name" + "%s" %t
                        except:
                            print "could not perform stats calc" + " " + "%s" %t + " " + "%s" %raster









            
            if "_mean_crop" in str(raster): 
                #outZonalStats=ZonalStatistics(fc,"OBJECTID",InData,"MEAN","DATA")
                #outZonalStats.save(i + "\\" + str(fc) + "_mean_crop")
                inRaster = raster
                # Execute Int
                outInt = Int(inRaster)
                # Save the output 
                outInt.save(i + "\\" + str(raster) + "_int")               
                print "calculating mean crop fraction per 10km grid cell "+ "%s" %outInt
                #Apply land Mask                
                arcpy.gp.ExtractByMask_sa(outInt,r"C:\Data\WWF\Processing\Global_Processing.gdb\landmask",i + "\\" + str(raster) + "_masked")
                print "masking mean crop fraction "+ "%s" %outInt
                arcpy.Delete_management(inRaster, data_type="#")
                #arcpy.Delete_management(outInt, data_type="#")
                print "deleting redundant files " + "%s" %inRaster
                #print "deleting redundant files " + "%s" %outInt
        #elif "_buff_fishnet" in str(fc):
           # arcpy.gp.ZonalStatistics_sa(fc,"OBJECTID",InData,gdb + "\\" + fc + "_mean_crop" ,"MEAN","DATA")
            else:
                print "Not calculating mean crop fraction for " + "%s" %raster
