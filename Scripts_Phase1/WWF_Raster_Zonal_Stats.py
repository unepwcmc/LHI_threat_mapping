#Python 2.7.5 (default, May 15 2013, 22:43:36) [MSC v.1500 32 bit (Intel)] on win32
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
InData=r"C:\Data\WWF\Data\IIASA\Hybrid_14052014V8_Moll.img"

workspaces = arcpy.ListWorkspaces("*", "FileGDB")
for i in workspaces:
    if i==r"C:\Data\WWF\Processing\Global_Processing.gdb":
        pass
    else:
        arcpy.env.workspace=i
        fclist =  arcpy.ListFeatureClasses()
        rasters = arcpy.ListRasters("*", "GRID")
        #for fc in fclist:
        for raster in rasters:
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
