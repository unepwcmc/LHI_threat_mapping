#Python code for ArcMap 10.2, Python v 2.7
# Code development by Brian O' Connor October 2015
import sys, os
import os
import arcpy
from arcpy import env
import time

beginTime = time.clock()

# Description: Selects roads which intersect the grids and produces road density maps
# set workspace environment
myWorkspace=r"C:\Data\WWF\Processing"
arcpy.env.workspace = myWorkspace

# Set coordinate system of the output fishnet
#env.outputCoordinateSystem = arcpy.SpatialReference("Mollweide")

# Each output cell will be a polygon
geometryType = 'POLYGON'
gdbList = arcpy.ListWorkspaces("*", "FileGDB")

#Get list of priority places
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
print PP_list
print PP_list_buff
print PP_list_fishnet
print PP_list_fishnet_buff

#Loop over the GDB (Roads) and read the fc from the list
in_grid = "C:\Data\WWF\Processing\Global_Processing.gdb\Global_Roads" #define location of roads layer
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
                    out_grid= gdb + "\\" + fc + "_roads_layer"
# First, make a layer from the feature class
                    arcpy.MakeFeatureLayer_management(in_grid,out_grid)
# Select roads from the global layer which overlap the PP polygon and create a feature layer for each new selection (stored in the respective PP gdb)
                    try:
                        arcpy.SelectLayerByLocation_management(out_grid, 'intersect', fc)
                        print "Selecting overlapping roads from " + "%s" %fc
                        arcpy.CopyFeatures_management(out_grid, fc + "_roads")
                        print "writing the overlapping roads to a new feature class " +  "%s" %fc + "_roads"
                    except:
                        print "fail"

            #New loop for tabulating intersection          
            #for t in PP_list_fishnet_buff:
                #if fc==t:
                #in_zone_features=t
                #zone_fields="OBJECTID"
                #in_class_features = str(fc).replace("fishnet","roads")
                #out_table=gdb + "\\" + fc + "_f"
                #class_fields="#"
                #sum_fields="LENGTH_KM"
                #xy_tolerance="#"
                #out_units="KILOMETERS"
                #arcpy.TabulateIntersection_analysis(in_zone_features,zone_fields,in_class_features,out_table,class_fields,sum_fields,xy_tolerance,out_units)
                #print "tabulating intersection " + "%s" %in_class_features                      
             
#Manage geodesic area fields in fishnet grids
for i in PP_list_fishnet:
    in_table=i
    drop_field=["AREA_GEO", "FREQUENCY"]
    arcpy.DeleteField_management(in_table,drop_field)
    Geometry_Properties="AREA_GEODESIC"
    Length_Unit="#"
    Area_Unit="SQUARE_KILOMETERS"
    Coordinate_System="#"
    try:
        arcpy.AddGeometryAttributes_management(in_table,Geometry_Properties,Length_Unit,Area_Unit,Coordinate_System)
        print "Deleting old and adding new geodesic area field to the " + "%s" %in_table
    except: 
        print arcpy.GetMessages(2)
    
    # If using this code within a script tool, AddError can be used to return messages 
    #   back to a script tool.  If not, AddError will have no effect.
    arcpy.AddError(e.message)
        

## PermanentJoin.py: Join one field from a table to a feature class 
# Set the local parameters
#tables = arcpy.ListTables()
#for table in tables:
    #if 
    
in_data = i
in_field = "OBJECTID"
joinTable = str(i) + "_f"
join_field="OBJECTID_1"
fields="LENGTH_KM"
arcpy.JoinField_management(in_data,in_field,join_table,join_field,fields)
print "Joining " + "%s" %in_data  + "to the " + "%s" %joinTable
# Replace a layer/table view name with a path to a dataset (which can be a layer file) or create the layer/table view within the script
# The following inputs are layers or table views: "African_Rift_Lakes_sp_buff_fishnet"
in_table=i
field_name="Density"
field_type="DOUBLE"
field_precision="#"
field_scale="#"
field_length="#"
field_alias="#"
field_is_nullable="NULLABLE"
field_is_required="NON_REQUIRED"
field_domain="#"
expression="[LENGTH_KM] / [AREA_GEO]"
expression_type="VB"
code_block="#"
arcpy.AddField_management(in_table,field_name,field_type,field_precision,field_scale,field_length,field_alias,field_is_nullable,field_is_required,field_domain)
print "adding field " + "%s" %field_name +"to " + "%s" %i
arcpy.CalculateField_management(in_table,field_name,expression,expression_type,code_block)
print "calculating " + "%s" %expression +"for " + "%s" %i
print ("Total elapsed time (seconds): " + str(time.clock() - beginTime))

#convert 'density' feature to raster
in_features=i
field="Density"
out_raster=str(i) + "_roads"
cell_size="10000"
# Set Mask environment
arcpy.env.mask = r"C:\Data\WWF\Processing\Global_Processing.gdb\landmask"
arcpy.env.snapRaster = r"C:\Data\WWF\Processing\Global_Processing.gdb\landmask"
#run tool
arcpy.FeatureToRaster_conversion(in_features,field,out_raster,cell_size)
print "making raster layer" + "%s" %field +"for " + "%s" %i
#Delete redundant files
               # if "ACLED_" in str(fc): #replace string to find apporiate files for deletion
                   # print "deleting " + "%s" %fc
                   # arcpy.Delete_management(fc, data_type="#")
                #else:
                   # print"No files exist for deletion in " + "%s" %gdb 

