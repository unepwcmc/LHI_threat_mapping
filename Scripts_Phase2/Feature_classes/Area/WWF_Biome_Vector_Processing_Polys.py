#Python 2.7.5 (default, Dec 10 2013, 22:43:36) [MSC v.1500 32 bit (Intel)] on win32
#Type "copyright", "credits" or "license()" for more information.
#Python code for ArcMap 10.2, Python v 2.7

# Code development by Brian O'Connor October 2015
import sys, os
import os
import arcpy
from arcpy import env
import time

beginTime = time.clock()

# Name: WWF_Biome_Vector_Processing_Areas.py
# Description: Processes polygon feature classes by intersecting them with fishnet grid and tabulating area
# Notes - 



# set workspace environment
myWorkspace=r"C:\Data\WWF\Processing"
arcpy.env.workspace = myWorkspace

# Set coordinate system of the output fishnet
#env.outputCoordinateSystem = arcpy.SpatialReference("Mollweide")

# Each output cell will be a polygon
#geometryType = 'POLYGON'
gdbList = arcpy.ListWorkspaces("*", "FileGDB")

#Get list of priority places # BIOMES
fc = r"C:\Data\WWF\Study_scope\WWF_PP_Terr.gdb\WWF_PP_Terr" #CHANGE to BIOMES
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
    PP_buffer_list=PP_list+PP_list_buff#print PP_list
#print PP_list_buff
#print PP_list_fishnet
#print PP_list_fishnet_buff



#Define parameters for area tabulation
zoneFld="OBJECTID"
Coordinate_System="PROJCS['World_Mollweide',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mollweide'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],UNIT['Meter',1.0]]"
Area_Unit="SQUARE_KILOMETERS"
Length_Unit="#"
Geometry_Properties="AREA_GEODESIC"
#classFld="#" # for areas
class_fields="COMMODITY"
sum_fields="#"
xy_tolerance="#"
out_units="UNKNOWN"
#sum_Fields="AREA_GEO" # for areas
xy_tol="#"
#outUnits="SQUARE_KILOMETERS" # for areas
#ingridList=[] # for areas
# define projection of output
arcpy.env.outputCoordinateSystem = "PROJCS['World_Mollweide',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mollweide'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],UNIT['Meter',1.0]]"

#Loop over GDBs in workspace 
for gdb in gdbList:
    # skip the GDB where raw data are stored
    if gdb=="Global_Processing.gdb":
        pass
    else:
        arcpy.env.workspace = gdb #--change working directory to each GDB in list
        # list feature classes in the GDB
        fclist = arcpy.ListFeatureClasses()  
        for fc in fclist:
            # identify the feature class you want to intersect with fishnet , i.e. using the string of fc name
            stpos=str(fc).find("_mineplant_layer")
            #define starting position of string characters
            if stpos != -1: # if the fc exists in the folder!
                fc_temp=fc[:stpos]# creates temporary filename for the fc
                fc_fishnet=fc_temp + "_fishnet" # appends fishnet to the fc name, to find the fishnet already in the working space
                fc_GFW=fc_temp + "_mineplant" #adds desired string extension to the fc, describing contents
                 #print fc_fishnet,fc_GFW
            #for i in  Fishnet_list:
                #if fc==i:  
                  #if 'GFW_logging' in str(fc):
                        #ingridList.append(fc)
                        #arcpy.AddGeometryAttributes_management(fc,Geometry_Properties,Length_Unit,Area_Unit,Coordinate_System)
                 try:
                            #for t in ingridList:
                     #if i + '_GFW_mining_updated_201402_layer' in str(fc):
                     # perform intersection using parameters defined above
                     arcpy.TabulateIntersection_analysis(fc_fishnet, zoneFld, fc_GFW, gdb + "\\" + fc_fishnet + "_mining", class_fields, sum_fields, xy_tol, out_units)
                     #print "intersecting " + "%s" %fc_fishnet + "%s" %fc_GFW
                     # Join table created above back to the fishnet grid using #OBJECTID as join field
                     arcpy.JoinField_management(fc_fishnet,"OBJECTID",fc_fishnet + "_mineplant","OBJECTID_1",["COMMODITY","PNT_COUNT"])
                     print "Joining " + "%s" %fc_fishnet  + "to the " + "%s" %fc_fishnet + "_mineplant"
                except:
                     print "intersection failed " + "%s" %fc_fishnet + "%s" %fc_GFW
                      
                            #convert 'geodesic area' features created above to raster
                            in_features=fc_fishnet
                            field="DAM_COUNT"
                            out_raster=str(fc_fishnet) + "_dams"
                            cell_size="10000"
                            # Set Mask environment
                            arcpy.env.mask = r"C:\Data\WWF\Processing\Global_Processing.gdb\landmask"
                            arcpy.env.snapRaster = r"C:\Data\WWF\Processing\Global_Processing.gdb\landmask"
                            #run tool
                            arcpy.FeatureToRaster_conversion(in_features,field,out_raster,cell_size)
                            print "making raster layer" + "%s" %field + "for " + "%s" %in_features
                        except:
                            print "failed to make raster " + "%s" %in_features




















#Delete Area_geo fields
                    
arcpy.DeleteField_management(in_table="Amazon_and_Guianas_fishnet",drop_field="AREA_GEO_1")

#change field names of the added geodesic area fields

#Loop through feature classes looking for a field named 'elev'
fcList = arcpy.ListFeatureClasses() #get a list of feature classes
for fc in fcList:  #loop through feature classes
    for i in Fishnet_list:
...     if fc==i:
...         fieldList = arcpy.ListFields(fc)
...         field_names = [f.name for f in arcpy.ListFields(fc)]
...         for name in field_names:
...             if str(name) == "Density":
...                 arcpy.AlterField_management(fc, name, 'Road Density', 'Density of Roads')
...                 print "altering" + "%s" %fc       
#convert 'density' feature to raster




















            
