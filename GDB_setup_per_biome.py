#Python code for ArcMap 10.2, Python v 2.7
# Code development by Brian O' Connor September 2016 whic makes a copy of fishnets in file geodatabases for subsequent processing

import sys, os
import os
import arcpy
from arcpy import env
import time

# Name: GDB_setup_per_biome.py
# Description:
#1. Creates a new geodatabase (GDB) for every biome and skips it if it already exists
#2. Looks for a fishnet for that biome in a 'fishnets' folder (created in previous script)
#3. Copies the fishnet to teh respective folder and skips it if it already exists
#4. Performs an intersection between the fishnet (per biome) and the extent of biome to calculate the area coverage of the biome per grid cell (in km2) and the % coverage of that cell by the biome.
#Having this information will be useful for later i.e. to look at proportion of threat per grid cells vs. proportion of biome per grid cell
# Notes - The code will require the original shapefile of WWF biomes


beginTime = time.clock()
# set workspace environment
myWorkspace=r"C:\Data\threat_mapping_lhi_2017\scratch"
arcpy.env.workspace = myWorkspace

#set to overwrite existing outputs
arcpy.env.overwriteOutput = True

#Get list of biomes and read into a list
fc = r"C:\Data\threat_mapping_lhi_2017\raw\Ecoregions2017.gdb\Ecoregions2017" # CHANGE TO THE MOST RECENT VERSION OF WWF BIOMES

field = "BIOME_NUM"#"FIRST_Biom"
cursor = arcpy.SearchCursor(fc)
biome_list_temp=[]
biome_list=[]
for row in cursor:
    t=row.getValue(field)
    if len(str(t))>1:
        biome_list_temp.append(t)
        for i in biome_list_temp:
            t=str(i)
            g = t.replace(" ","")
    biome_list.append(g)
    biome_list.sort()
print biome_list

#create gdb per biome
for biome in biome_list:
    if arcpy.Exists(str(biome) + ".gdb"):
        print "skipping GDB creation : " "%s" % myWorkspace, "%s" %biome
    else:
        arcpy.CreateFileGDB_management(myWorkspace, str(biome))
        print "creating file GDB : " "%s" % myWorkspace, "%s" %biome

#list geodatabases
workspaces = arcpy.ListWorkspaces("*", "FileGDB")
#create list of gdb
gdb_list=[]

##for workspace in workspaces:
##   # create list of ws names
##    temp_str = workspace[27:] #+ "\\"#)# THIS REMOVES THE CHARACTERS FOR FILE PATH LEAVING ROOT NAME (BIOME) - there may be a better way than explicitly stating character '27'  
##    gdb_list.append (temp_str[:-4])
# Manually correct name for this biome
#gdb_list[1]="DesertsXericShrublands"
    
#print gdb_list     
##
###list fishnets in source folder:
##myWorkspace=r"C:\Data\threat_mapping_lhi_2017\raw\"
##arcpy.env.workspace = myWorkspace
##fclist = arcpy.ListFeatureClasses()
###create list of gdb and list of fishnets
##fish_list=[]

##for fc in fclist :
##    if "fishnet" in str(fc):
##        #a=str(fc).strip(".shp")
##        a=str(fc) #.replace("_",""))
##        fullPath = os.path.join(myWorkspace,a)
##        fish_list.append(fullPath)
###print fish_list

#define parameters for intersection
zone_fields="FID"
join_field = "OBJECTID"
inpath=r"C:\Data\threat_mapping_lhi_2017\"
class_fields="#"
sum_fields="#"
xy_tolerance="#"
out_units="SQUARE_KILOMETERS"
fields1 = ['AREA', 'New_Area']
fields2 = ['PERCENTAGE', 'New_Perc']
keep_fields=['Area_Biome','Perc_Biome']
#copy fishnet to the respective GDB
for gdb in gdb_list:
    for fish in fish_list:
        if gdb in str(fish).replace("_",""):
            new_Workspace = os.path.join("C:\Data\WWF_Ph2\Processing",gdb + ".gdb")
            arcpy.env.workspace = new_Workspace
            fcs=arcpy.ListFeatureClasses()
            if not fcs:
                arcpy.FeatureClassToGeodatabase_conversion(fish,new_Workspace)
                print "copying " "%s" %fish + " to " "%s" %new_Workspace
            elif len ([x for x in fcs if "fishnet" in x]) > 0:
                print "skipping copy of fishnet to GDB : " "%s" % gdb
            #tabulate intersection in the GDB
            in_string= fish[25:]
            in_string_= in_string.replace("_fishnet","")
            in_string__= in_string_.replace("_"," ") 
            # in_string___=' '.join(in_string__.split())
            in_features = os.path.join(inpath,in_string__)
            out_table = gdb
            if arcpy.Exists(gdb):
                print "intersection already performed"
            else:    
                arcpy.TabulateIntersection_analysis(fish,zone_fields,in_features,out_table,class_fields,sum_fields,xy_tolerance,out_units)
                print "calculating area of biome per grid cell :  " "%s" % out_table
        # changing field precision of area and percentage fields by creating new field, copying numbers in original field and deleting original fields   
                arcpy.AddField_management(out_table, "New_Area", "FLOAT")
                print "adding new field to store biome area"
                arcpy.AddField_management(out_table, "New_Perc", "FLOAT")
                print "adding new field to store biome percentage cover"
                with arcpy.da.UpdateCursor(out_table,fields1) as cursor:
                    for row in  cursor:
                        row[1] = row[0]
                        cursor.updateRow(row)
                with arcpy.da.UpdateCursor(out_table,fields2) as cursor:
                    for row in  cursor:
                        row[1] = row[0]
                        cursor.updateRow(row)
                arcpy.DeleteField_management(out_table, ['PERCENTAGE','AREA'])
                print "deleting old fields"
                arcpy.AlterField_management(out_table, "New_Area", 'Area_Biome', 'Area of biome in grid cell in km')
                print "changing field name :  'Area_Biome'"
                arcpy.AlterField_management(out_table, "New_Perc", 'Perc_Biome', 'Percentge of biome in grid cell')
                print "changing field name :  'Perc_Biome'"
            lst = arcpy.ListFields(in_string.rstrip(".shp"))
            if len ([f for f in lst if f.name == "Area_Biome"]) > 0:
                print "join already performed"  
            elif len ([f for f in lst if f.name == "Area_Biome"]) == 0:
                arcpy.JoinField_management(in_string.rstrip(".shp"),join_field,out_table,join_field,keep_fields)
                print "joining table of area biome  :  " "%s" % out_table + " to " "%s" %gdb + "_fishnet"
            
            
print ("Total elapsed time (seconds): " + str(time.clock() - beginTime))
