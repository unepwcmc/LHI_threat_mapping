#Python code for ArcMap 10.2, Python v 2.7
# Code development by Brian O' Connor October 2015 (updated 31st March 2017)
import sys, os
import os
import arcpy
from arcpy import env
import time

beginTime = time.clock()

# Description: Selects roads which intersect the grids and produces road density maps
# NOTE - needs modfication to alter for other linear features 


# set workspace environment
myWorkspace=r"P:\PROJECTS\6400s\06459.00.E Drivers & Pressures Threat Mapping\GIS_Analysis\Global_data"
arcpy.env.workspace = myWorkspace

# Each output cell will be a polygon
geometryType = 'POLYGON'
gdbList = arcpy.ListWorkspaces("*", "FileGDB")

#Get list of priority places # BIOME NAMES
fc = r"P:\PROJECTS\6400s\06459.00.E Drivers & Pressures Threat Mapping\GIS_Analysis\Global_data\Ecoregions2017.gdb\Ecoregions2017"
field = "BIOME_NAME"
cursor = arcpy.SearchCursor(fc)
Biome_list_temp=[]
Biome_list=[]
Biome_list_fishnet=[]
for row in cursor:
    t=row.getValue(field)
    Biome_list_temp.append(t)
    #convert to set to get unique list
    myset = set(Biome_list_temp)
    #convert back to list
    mynewlist = list(myset)
    #create empty list for cleaned biome names
    BiomeNameList=[]
    #create empty list for cleaned biome names+fishnet extension
    BiomeNameList_fishnet=[]
    #Get rid of unwanted characters in biome names
    char_list=['&','/',' ',',']
    for string in mynewlist:
        for ch in char_list: 
            if ch in string:
                string=string.replace(ch,"")
                #append the cleaned strings to the empty list
        BiomeNameList.append(string)
        BiomeNameList_fishnet.append(string + "_fishnet")
        #remove the NA strings in the list
BiomeNameList.remove('NA')
BiomeNameList_fishnet.remove('NA_fishnet')
print BiomeNameList, BiomeNameList_fishnet

#===================================================================
#THIS PART of CODE LOOKS AT MATCHING THE LIST OF BIOME NAMES WITH THE LIST OF GDBs IN THE WORKING DIRECTORY SO THAT BIOME LEVEL PROCESSING (INPUTS AND OUTPUTS) ARE
#COPIED TO THE RIGHT PLACE

#Define where your line feature class is saved
in_grid = "C:\Data\WWF\Processing\Global_Processing.gdb\Global_Roads" #define location of roads layer
#Loop over the GDBs
for gdb in gdbList:
    if gdb=="Global_Processing.gdb": # this is if you have a GDB you don't want to be included in list, can omit this step if not needed
        pass
    else:
        arcpy.env.workspace = gdb #--change working directory to each GDB in list
        arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(r"C:\Data\WWF\Processing\WWF_5min_grid_Moll.prj")# make sure your outputs will be in equal area proj
        fclist = arcpy.ListFeatureClasses()  #list the fc in your GDB
        for fc in fclist:
            for i in BiomeNameList:
                if fc==i:  # YOUR GDB MUST HAVE A FEATURE CLASS OF THE BIOME EXTENT IN THE GDB WITH EXACT SAME FILE NAME AS THE BIOME NAME, ELSE THIS WON'T WORK                 
                    out_grid= gdb + "\\" + fc + "_roads_layer" # create name for your output line feature
# Then, make a layer from the line feature class
                    arcpy.MakeFeatureLayer_management(in_grid,out_grid)
# Select roads from the global layer which overlap the Biome polygon and create a feature layer for each new selection (stored in the respective Biome gdb)
                    try:
                        # select linear features which intersect the biome extent
                        arcpy.SelectLayerByLocation_management(out_grid, 'intersect', fc)
                        print "Selecting overlapping roads from " + "%s" %fc
                        # copy those features to a new feature class
                        arcpy.CopyFeatures_management(out_grid, fc + "_roads")
                        print "writing the overlapping roads to a new feature class " +  "%s" %fc + "_roads"
                    except:
                        print "fail"

            #New loop for tabulating intersection, i.e. to get length of linear feature in the grid cell          
            for t in BiomeNameList_fishnet:
                if fc in str (t): # find the fishnet which matches the biome name
                in_zone_features=t
                zone_fields="OBJECTID"
                in_class_features = str(t).replace("fishnet","roads")#line fc created in above step
                out_table=gdb + "\\" + fc + "_f"
                class_fields="#"
                sum_fields="LENGTH_KM"
                xy_tolerance="#"
                out_units="KILOMETERS"
                arcpy.TabulateIntersection_analysis(in_zone_features,zone_fields,in_class_features,out_table,class_fields,sum_fields,xy_tolerance,out_units)
                print "tabulating intersection " + "%s" %in_class_features                      
             
#ONLY USE IF DOING AREAS
#Manage geodesic area fields in fishnet grids
##for i in Biome_list_fishnet:
##    in_table=i
##    drop_field=["AREA_GEO", "FREQUENCY"]
##    arcpy.DeleteField_management(in_table,drop_field)
##    Geometry_Properties="AREA_GEODESIC"
##    Length_Unit="#"
##    Area_Unit="SQUARE_KILOMETERS"
##    Coordinate_System="#"
##    try:
##        arcpy.AddGeometryAttributes_management(in_table,Geometry_Properties,Length_Unit,Area_Unit,Coordinate_System)
##        print "Deleting old and adding new geodesic area field to the " + "%s" %in_table
##    except: 
##        print arcpy.GetMessages(2)
    
    # If using this code within a script tool, AddError can be used to return messages 
    #   back to a script tool.  If not, AddError will have no effect.
    #arcpy.AddError(e.message)
        

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
               # if "ACLED_" in str(fc): #replace string to find appopriate files for deletion
                   # print "deleting " + "%s" %fc
                   # arcpy.Delete_management(fc, data_type="#")
                #else:
                   # print"No files exist for deletion in " + "%s" %gdb 

