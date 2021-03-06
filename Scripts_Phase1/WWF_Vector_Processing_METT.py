#Python code for ArcMap 10.2, Python v 2.7
# Code development by Brian O' Connor October 2015
import sys, os
import os
import arcpy
from arcpy import env
import time
import csv

beginTime = time.clock()

# Description: Selects roads which intersect the grids and produces road density maps
# set workspace environment
myWorkspace=r"C:\Data\WWF\Processing"
arcpy.env.workspace = myWorkspace
arcpy.env.overwrite=True

# Set coordinate system of the output fishnet
#env.outputCoordinateSystem = arcpy.SpatialReference("Mollweide")

# Each output cell will be a polygon
#geometryType = 'POLYGON'
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
    Fishnet_list = PP_list_fishnet + PP_list_fishnet_buff
    PP_buffer_list=PP_list+PP_list_buff
#print PP_list
#print PP_list_buff
#print PP_list_fishnet
#print PP_list_fishnet_buff

#Loop over the GDB (Roads) and read the fc from the list
#in_grid = "C:\Data\WWF\Processing\Global_Processing.gdb\Global_Roads" #define location of roads layer
# Identify the GFW layers and out in a list
#arcpy.env.workspace=r"C:\Data\WWF\Processing\Global_Processing.gdb"
#WSpace=r"C:\Data\WWF\Processing\Global_Processing.gdb"
#fclist = arcpy.ListFeatureClasses()
   # in_grids=[]
#for fc in fclist:
    #if "GFW_" in fc:
       # fullPath = os.path.join(WSpace, fc)
        #print fullPath
        #in_grids.append(fullPath)
#print in_grids

#Loop over GDBs to intersect PP shapes with GFW features      
in_grid = r"C:\Data\WWF\Processing\Global_Processing.gdb\WDPA_Nov_2015_METT1_Assessed" 
for gdb in gdbList:
    if gdb=="Global_Processing.gdb":
        pass
    else:
        arcpy.env.workspace = gdb #--change working directory to each GDB in list
        #arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(r"C:\Data\WWF\Processing\WWF_5min_grid_Moll.prj")
        fclist = arcpy.ListFeatureClasses()  
        for fc in fclist:
            for i in  PP_list:
                if fc==i:                   
                    #for feature in in_grids:
                    #in_grid = #in_grids[1]
                    out_grid = str(in_grid[59:] + "_lyr")
                    #for fc in fclist:                          
# First, make a layer from the feature class
                    #count1 = str(arcpy.GetCount_management(fc))
                   # if count1 == "0":
                       # pass
                    #else:
                    arcpy.MakeFeatureLayer_management(in_grid,out_grid)
                    print "making feature layer " + "%s" %out_grid
# Select roads from the global layer which overlap the PP polygon and create a feature layer for each new selection (stored in the respective PP gdb)
                    try:
                        arcpy.SelectLayerByLocation_management(out_grid, 'intersect', fc)
                        print "Selecting overlapping " + "%s" %out_grid + " from " + "%s" %fc
                        # Within the previous selection sub-select PAs which have year assessed = 2003 (METT1)
                        arcpy.SelectLayerByAttribute_management(out_grid, 'SUBSET_SELECTION', '"Year" = 2013')
                        # Only if features matched criteria write them to a new feature class
                        matchcount = int(arcpy.GetCount_management(out_grid).getOutput(0))
                        if matchcount == 0:
                            print('no features matched spatial and attribute criteria')
                        else:
                            arcpy.CopyFeatures_management(out_grid, fc + "_2013" + "%s" %out_grid)
                            print ('{0} PAs that matched criteria written to {1}'.format(matchcount, fc + "_2013" + "%s" %out_grid))
                    except:
                        print "failed " + "%s" %out_grid




# Create a dictionary to store the METT threat codes and their meaning , i.e. key (code) and value (meaning), stored as strings

#in_table = r"C:\Data\WWF\Data\METT\Key_METT1_Threats.csv" 
myWorkspace=r"C:\Data\WWF\Data\METT"
arcpy.env.workspace = myWorkspace

with open('C:\Data\WWF\Data\METT\Key_METT3_Threats.csv', mode='r') as infile:
     reader = csv.reader(infile)
     with open('C:\Data\WWF\Data\METT\Key_METT3_Threats_new.csv', mode='w') as outfile:
         writer = csv.writer(outfile)
         mydict = {rows[0]:rows[1] for rows in reader}
         print mydict



#Get a list of field names from the column headers of 
FieldNameList=[]
#cursor = arcpy.SearchCursor("C:\Data\WWF\Processing\Coastal_East_Africa.gdb\Coastal_East_Africa_2004METT1_Assessed_lyr")
fc="C:\Data\WWF\Processing\Coastal_East_Africa.gdb\Coastal_East_Africa_2004METT1_Assessed_lyr"
fieldList = arcpy.ListFields(fc)
field_names = [f.name for f in arcpy.ListFields(fc)]
for name in field_names:
    if str(name[0:1]) == "F":
        FieldNameList.append(name)
        

            
# Split out the feature classes by their threat code (per year)

for gdb in gdbList:
    if gdb=="Global_Processing.gdb":
        pass
    else:
        arcpy.env.workspace = gdb #--change working directory to each GDB in list
        #arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(r"C:\Data\WWF\Processing\WWF_5min_grid_Moll.prj")
        fclist = arcpy.ListFeatureClasses()  
        for fc in fclist:
            for i in FieldNameList:
                if "2004METT" in str(fc):
                    field = FieldNameList[0]
                    cursor = arcpy.SearchCursor(fc)
                    for row in cursor:
                        t=row.getValue(field)
                        if str(t) == 'yes':
                            arcpy.env.overwrite=False
                            arcpy.Split_analysis(fc,fc,i,gdb,cluster_tolerance="#")
                            print "splitting " + "%s" %fc + "by " + "%s" %i    
                




#Delete all empty feature classes

#env.workspace = r"C:\Temp\Test.gdb"  
  
listFCs = arcpy.ListFeatureClasses("*")  
  
for fc in listFCs:  
    count1 = str(arcpy.GetCount_management(fc))  
    if count1 == "0":  
        arcpy.Delete_management(fc)  
































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

print ("Total elapsed time (seconds): " + str(time.clock() - beginTime))
