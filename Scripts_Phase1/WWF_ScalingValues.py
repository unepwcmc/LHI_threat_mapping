import sys, os
import os
import arcpy
from arcpy import env
import time
# Import system modules
from arcpy.sa import *

#Set variables, lists etc.
arcpy.env.workspace=r"C:\Data\WWF\Processing"

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
    if g== "Arctic_sp_buff_fishnet":
        pass
    elif g== "Amur_Heilong_sp_buff_fishnet":
        pass
    else:
        PP_list_fishnet_buff.append(g)
    PP_list.sort()
    PP_list_buff.sort()
    PP_list_fishnet.sort()
    PP_list_fishnet_buff.sort()
    Fishnet_list = PP_list_fishnet + PP_list_fishnet_buff
    PP_buffer_list=PP_list+PP_list_buff
    temp_list=PP_list_fishnet[0:2]

#STEP 1: Define function to normalise values
def NormalizedNumbersToField(table, field, scratchGDB):
    arcpy.env.overwriteOutput=True
    arcpy.AddField_management(table, "NORMALIZED_%s"%field, "DOUBLE")
    scratchTable = os.path.join(scratchGDB, "Temp_Feat")
    arcpy.Statistics_analysis(table,scratchTable, [[str(field),"MIN"],[str(field),"MAX"]])
    with arcpy.da.SearchCursor(scratchTable, ("MAX_" + str(field) , "MIN_" + str(field))) as cursor:
        for row in cursor:
            maxNum = row[0]
            minNum = row[1]
    del cursor, row
    arcpy.Delete_management(scratchTable)
    with arcpy.da.UpdateCursor(table, (field , "NORMALIZED_%s"%field )) as cursor:
        for row in cursor:
            try:
                number = row[0]
                if type(number) == type(None):
                    number =  minNum
                row[1] = (( number - minNum ) / ( maxNum - minNum ))
                cursor.updateRow(row)
            except:
                print "error %s" %field
    del cursor, row
    
#create list of fieldnames
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
                    fieldnamelist=[]
                    field_names = arcpy.ListFields(fc,"",'Integer')
                    for field in field_names:
                        if field.type != "Geometry":
                            fieldnamelist.append(field.name)
                    for field in fieldnamelist[1:]:
                        NormalizedNumbersToField(fc,field,i)
                        print "Normalising %s" %field + " in %s" %fc 









#In case needing to delete the normalised fields:
list=[]
    for i in workspaces:
...     arcpy.env.overwriteOutput=True  
...     if i==r"C:\Data\WWF\Processing\Global_Processing.gdb":
...         pass
...     else:
...         arcpy.env.workspace=i
...         fclist =  arcpy.ListFeatureClasses()
...         #rasters = arcpy.ListRasters("*", "GRID")
...         for fc in fclist:
...             for t in temp_list:
...                 if fc==t:
...                     for field in arcpy.ListFields(fc, "NORMALIZED_*"):
...                         list.append(field.name)
...                         arcpy.DeleteField_management(fc, list)  



#To obtain a value from 0 to 1:
# add field to store result

arcpy.AddField_management(fc,field + "_scaled","FLOAT","#","#","#","#","NULLABLE","NON_REQUIRED","#")
arcpy.CalculateField_management(fc,field + "_scaled","( !field!  - min(listname) ) / ( max(listname) - min(listname) ) ","PYTHON","#")


