import sys, os
import os
import arcpy
from arcpy import env
import time

arcpy.env.workspace=r"C:\Data\threat_mapping_lhi_2017\scratch"

#list geodatabases
workspaces = arcpy.ListWorkspaces("*", "FileGDB")

#Get list of biomes and read into a list
fc = r"C:\Data\threat_mapping_lhi_2017\raw\Ecoregions2017.gdb\Ecoregions2017" # CHANGE TO THE MOST RECENT VERSION OF WWF BIOMES


field = "BIOME_NUM"#"FIRST_Biom"
cursor = arcpy.SearchCursor(fc)
biome_list_temp=[]
biome_list=[]
for row in cursor:
    t=row.getValue(field)
    #t=arcpy.ValidateTableName(t)
    if len(str(t))>1:
        biome_list_temp.append(t)
        for i in biome_list_temp:
            t=str(i)
            g = t.replace(" ","")
            g = t.replace("/","Or")
            g = t.replace("_","")
            t=arcpy.ValidateTableName(t)
    biome_list.append(g)
    biome_list.sort()
print biome_list


#create list of gdb
gdb_list=list(set(biome_list))
print gdb_list

##for workspace in workspaces:
##   # create list of ws names
##    temp_str = workspace[27:] #+ "\\"#)# THIS REMOVES THE CHARACTERS FOR FILE PATH LEAVING ROOT NAME (BIOME) - there may be a better way than explicitly stating character '27'  
##    gdb_list.append (temp_str[:-4])
# Manually correct name for this biome
#gdb_list[1]="DesertsXericShrublands"


for gdb in gdb_list:
    #selectString=""" "BIOME_NUM" = """
    arcpy.Select_analysis(inFC,outFC,selectString)
    
##        arcpy.MakeFeatureLayer_management(inFC, in_memory_feature2,selectString)
##        result = arcpy.GetCount_management(in_memory_feature2)
##        count = int(result.getOutput(0))
##        print "FeatureClass stored: "+ str(outFC)
##        #arcpy.CopyFeatures_management(in_memory_feature2,outFC) 
##        #arcpy.env.extent = outFC
##        print("Elapsed time (minutes): " + str((time.clock() - beginTime1)/60))
####        print "Number of rows selected: " +str(count)
##        grid_national=outFC#wkspce3+"/"+prefix2+"_"+str(valClean[0:15])
##        print grid_national
##        in_memory_feature3 = "in_memory\\"+ str(i)+"3"
