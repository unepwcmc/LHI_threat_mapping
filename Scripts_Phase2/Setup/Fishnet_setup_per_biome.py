#Python 2.7.5 (default, May 15 2013, 22:43:36) [MSC v.1500 32 bit (Intel)] on win32
#Type "copyright", "credits" or "license()" for more information.
 
#Python code for ArcMap 10.2, Python v 2.7
# Code development by Brian O' Connor September 2016
import sys, os
import os
import arcpy
from arcpy import env
import time

beginTime = time.clock()

# Name: Fishnet_setup_per_biome.py
# Description: Creates rectangular cells per biome and adds geometry attributes (geodesic area)
# Notes - this creates an equal area grid (10km) as input to subsequent gridding operations. It uses the bounding extent of the biome to constrain the size of the fishnet. It uses the method desribed in the protocol document
#(see P:\PROJECTS\6400s\06459.00.E Drivers & Pressures Threat Mapping\GIS_Analysis\Scripts\Scripts_Phase2\Global_fishnet). It assumes the biomes have already been split out from their parent shapefile and saved to the workspace. 

# # Set the workspace and outputCoordinateSystem 
myWorkspace=r"C:\Data\WWF_Ph2\Biomes"
arcpy.env.workspace = myWorkspace
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(r"C:\Data\WWF\Processing\WWF_5min_grid_Moll.prj")
#set to overwrite existing outputs
arcpy.env.overwriteOutput = True

#list all directories
fclist = arcpy.ListFeatureClasses()
inpath=r"C:\Data\WWF_Ph2\Biomes"
outpath=r"C:\Data\WWF_Ph2\Fishnets"
# Execute CreateFolder
out_name = "Processing.gdb"
out_table_dir=os.path.join (outpath, out_name)
if arcpy.Exists(out_table_dir):
    print "gdb exists - not creating new one!"
else:
    arcpy.CreateFileGDB_management(outpath, out_name)

#set geometry attributes for fishnet and processing
intersect_feature="INTERSECTFEATURE"
use_page_unit="NO_USEPAGEUNIT"
scale="#"
polygon_width="10 Kilometers"
polygon_height="10 Kilometers"
origin_coord=""
number_rows=""
number_columns=""
starting_page_number="1"
label_from_origin="NO_LABELFROMORIGIN"
drop_fields=["PageName","PageNumber"]
Geometry_Properties="AREA_GEODESIC"
Length_Unit="#"
Area_Unit="SQUARE_KILOMETERS"
Coordinate_System="PROJCS['World_Mollweide',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mollweide'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],UNIT['Meter',1.0]]"
zone_fields="FID"
class_fields="#"
sum_fields="#"
xy_tolerance="#"
out_units="SQUARE_KILOMETERS"
new_type = "SHORT"
fields="Area_Biome"
#Open loop:
for fc in fclist:
    #set to overwrite existing outputs
    arcpy.env.workspace = outpath
    arcpy.env.overwriteOutput = True
    # set names of source files, out files and path directories
    out_feature_string=str(fc[:-4]) + "_fishnet"
    out_feature_string_ = out_feature_string.replace(" ","_")
    out_feature_class= os.path.join(outpath, out_feature_string_)
    in_features= os.path.join(inpath, str(fc))
    out_table=os.path.join(out_table_dir, str(fc[:-4]).replace(" ","_"))
 #Make fishnet based on biome layer extent and set output projection as Mollweide
    try:
        arcpy.GridIndexFeatures_cartography(out_feature_class,in_features,intersect_feature,use_page_unit,scale,polygon_width,polygon_height,origin_coord,number_rows,number_columns,starting_page_number,label_from_origin)
        print "creating fishnet " "%s" %out_feature_class + " from " + "%s" %in_features
    except Exception:
        e = sys.exc_info()[1]
        print(e.args[0])
    arcpy.AddGeometryAttributes_management(out_feature_class + ".shp",Geometry_Properties,Length_Unit,Area_Unit,Coordinate_System)
    print "geometry attribute added :  " "%s" %Geometry_Properties + " in " + "%s" %Area_Unit
    arcpy.DeleteField_management(out_feature_class + ".shp",drop_fields)
    print "deleting fields :  " "%s" %drop_fields        
##    arcpy.TabulateIntersection_analysis(out_feature_class + ".shp",zone_fields,in_features,out_table,class_fields,sum_fields,xy_tolerance,out_units)
##    print "calculating area of biome per grid cell :  " "%s" % out_table
##    # changing field precision of area and percentage fields by creating new field, copying numbers in original field and deleting original fields   
##    arcpy.AddField_management(out_table, "New_Area", "FLOAT")
##    print "adding new field to store biome area"
##    fields = ['AREA', 'New_Area']
##    with arcpy.da.UpdateCursor(out_table,fields) as cursor:
##        for row in  cursor:
##            row[1] = row[0]
##            #row.setValue("New_Area", row.getValue("Area_Biome"))
##            cursor.updateRow(row)
##    #arcpy.DeleteField_management(out_table, "Area_Biome")
##    arcpy.DeleteField_management(out_table, ['PERCENTAGE','AREA'])
##    arcpy.AlterField_management(out_table, "New_Area", 'Area_Biome', 'Area of biome in grid cell in km')
##    print "changing field name :  'Area_Biome'" 
##    arcpy.JoinField_management(out_feature_class + ".shp",zone_fields,out_table,zone_fields,fields)
##    print "joining table of area biome  :  " "%s" % out_table + " to " "%s" % out_feature_class + ".shp"

print ("Total elapsed time (seconds): " + str((time.clock() - beginTime))/60)



##
##    fieldList = arcpy.ListFields(out_table)
##    for field in fieldList:
##        if field.name == 'AREA':
##            arcpy.AlterField_management(out_table, field.name, 'Area_Biome', 'Area of biome in grid cell in km')
##            print "changing field name :  " "%s" % field.name
##        elif field.name == 'PERCENTAGE':
##            arcpy.AlterField_management(out_table, field.name, 'Perc_Biome', 'Percentage of biome in grid cell')
##            print "changing field name :  " "%s" % field.name
##        else:
##            print "no field name found"
