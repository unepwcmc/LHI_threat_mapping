#Python code for ArcMap 10.2, Python v 2.7
# Code development by Brian O' Connor June 2015
import sys, os
import os
import arcpy
from arcpy import env
import time

beginTime = time.clock()

#set to overwrite existing outputs
arcpy.env.overwriteOutput = True

#set workspace for inputs and outputs

myWorkspace=r"P:\PROJECTS\7100s\07104.00.E GEO6 Regional Assessments\GIS_Analysis\post_workshop_work\Europe_regional_mapping\scratch\grid_geometry_calcs.gdb"
#myWorkspace=r"C:\Data\geo6\scratch\grid_geometry_calcs.gdb"

arcpy.env.workspace = myWorkspace
print "Workspace: " + myWorkspace
#env.outputCoordinateSystem = r"C:\Users\briano\AppData\Roaming\ESRI\Desktop10.2\ArcMap\Coordinate Systems\WGS 1984.prj"


#Set enviroenment extent
#arcpy.env.extent = 'C:\Data\GEO6\Extractives_Map\EU_geodatabase.gdb\EU_boundary'

#Point_feature_type='Point'
fclist = arcpy.ListFeatureClasses()
#Point_fclist = arcpy.ListFeatureClasses("trans_*",Point_feature_type,"")
    
#Intersect transport layers with the grid
#Note - the grid should be in an equal area projection, e.g. Mercator for later calcs
# Set up loop for points and polygons

target_layer = "eur"
target_field = "FID_"+target_layer
target_fid_field="OBJECTID"
#calculate areas for main target layer if not already
#arcpy.AddGeometryAttributes_management(target_layer,Geometry_Properties="AREA_GEODESIC",Length_Unit="",Area_Unit="SQUARE_KILOMETERS",Coordinate_System="#") 
#print "Geodesic area calculated for", target_layer



countLine=0
countPoint=0
countArea=0
countOther=0
Parser="_intersect"
for feature in fclist:
    if feature == target_layer:
        pass
    else:
        desc = arcpy.Describe(feature)
        desc = desc.shapeType
        print  "Featureclass is type :" + str(desc)
        #lastchar = feature[-1]
        
        if str(desc)=='Point':
           countPoint=countPoint+1
           inFeatures = [feature, target_layer]
           arcpy.Intersect_analysis(inFeatures, feature + Parser,"ONLY_FID","#","POINT")
        
        if str(desc)=='Polyline':
           countLine=countLine+1
           inFeatures = [feature, target_layer]
           arcpy.Intersect_analysis(inFeatures, feature + Parser, "ONLY_FID", "","LINE")

        elif str(desc)=='Polygon':
            countArea=countLine+1
            inFeatures = [feature, target_layer]
            arcpy.Intersect_analysis(inFeatures, feature + Parser, "ONLY_FID", "","INPUT")
    
    #else:
        #countOther=countOther+1
print fclist
print countLine,"line features have been intersected,",countPoint,"point features have been intersected and", countArea,"polygon features have been intersected" #countOther "features remain in the workspace"


#Make a separate list of the intersected point and line layers
feature_type_line='Polyline'
feature_type_point='Point'
feature_type_area='Polygon'
fclistLine = arcpy.ListFeatureClasses("*_intersect",feature_type_line,"")
fclistPoint = arcpy.ListFeatureClasses("*_intersect",feature_type_point,"")
fclistArea = arcpy.ListFeatureClasses("*_intersect",feature_type_area,"")

# Project layers to an equidistant projection for correct calculation of length (note - only need to do this for line files):
#NOTE- this step has been omitted and replaced with a geodesic length calculation
for feature in fclistLine:
    arcpy.AddGeometryAttributes_management(feature,Geometry_Properties="LENGTH_GEODESIC",Length_Unit="KILOMETERS",Area_Unit="#",Coordinate_System="#")
print "Geodesic length calculated for", feature

for feature in fclistArea:
    arcpy.AddGeometryAttributes_management(feature,Geometry_Properties="AREA_GEODESIC",Length_Unit="",Area_Unit="SQUARE_KILOMETERS",Coordinate_System="#") 
print "Geodesic area calculated for", feature

     
# calculate summary stats and output a table
# for lines
count=0
for feature in fclistLine:
    count=count+1
    #Generate stats table
    arcpy.Statistics_analysis(feature,feature+"_sum_table_l","LENGTH_GEO SUM",target_field)
    print count, " sum line tables written to file"
# for areas
count=0  
for feature in fclistArea:
    count=count+1
    #Generate stats table
    arcpy.Statistics_analysis(feature,feature+"_sum_table_a","AREA_GEO SUM",target_field)
    print count, " sum area tables written to file"

#For points - need to count the number of points in the grid cell, i.e. frequency
count=0
FieldNameList=[]
for feature in fclistPoint:
    #parsing the field name for stats calc from the file name 
    count=count+1
    FieldName=fclistPoint[count-1:count] 
    for i in FieldName:
        x=i.find('_intersect')
        statsField = "FID_"+i[0:x]
        #statsFieldStr= statsField.encode('utf8')
        print   statsField
        FieldNameList.append(statsField)
        print FieldNameList
    #Generate 2-way matrix of file name and field name
zipped = zip (fclistPoint,FieldNameList)
count=0
for i,j in zip(fclistPoint,FieldNameList):
    statsFields = [[j, "COUNT"]]
    arcpy.Statistics_analysis(i,i+ "_count_table", statsFields,target_field)
    count=count+1
    print count, " count point tables written to file"    

# Join the count and sum fields back to the original grid cells (using FID) via a table join
#for lines
Tablelist = arcpy.ListTables("*_sum_table_l")
# Set the local parameters:
#for lines
indata = target_layer
in_field=target_fid_field
joinField = target_field
fieldList = ["SUM_LENGTH_GEO"]
print"Joining line distance tables to the original grid"
for table in Tablelist:
    try:
        arcpy.JoinField_management (indata, in_field, table, joinField, fieldList)
        print "joined %s successfully" % table
    except:
        print arcpy.GetMessages()
        break
count=0

#for areas
Tablelist = arcpy.ListTables("*_sum_table_a")
indata = target_layer
in_field=target_fid_field
joinField = target_field
fieldList = ["SUM_AREA_GEO"]

print "Joining area tables to the original grid"
for table in Tablelist:
    try:
        arcpy.JoinField_management (indata, in_field, table, joinField, fieldList)
        print "joined %s successfully" % table
    
    except:
        print arcpy.GetMessages()
        break
#for points    
Tablelist = arcpy.ListTables("*_count_table")
# Set the local parameters
indata = target_layer
in_field=target_fid_field
joinField = target_field
fieldList = ["FREQUENCY"]
print "Joining point frequency tables to the original grid"
for table in Tablelist:
    try:
        arcpy.JoinField_management (indata, in_field, table, joinField, fieldList)
        print "joined %s successfully" % table
    except:
        print arcpy.GetMessages()
        break
    


#Create list of file names and field names
#FileNameList= fclistLine + fclistArea + fclistPoint
#FieldNames = arcpy.ListFields(target_layer)
#FieldNameList = [f.name for f in arcpy.ListFields(target_layer)]

#for field in FieldNames:
   # FieldNameList =  field.name
#FieldNameList= FieldNameList[6:]

#z = zip(FileNameList,FieldNameList)
#count = 0

#for i,j in z:
#    count = count+1
#    i=i[:15]
#    arcpy.PolygonToRaster_conversion(target_layer,j,i,"#","#",0.5)  
#    print "Exported field "+ j + " to file: " + i + ",raster: " + str(count)
#print count, "rasters exported"
#delete unnecessary feature classes 
dataType="#"
#Create safe list of files for non-deletion
#SaveFiles=[target_layer,"WA_boundary", "Mines_all_prospect_p", "all_oil_gas_pipes_l", "Mines_all_future_p","Mines_all_current_p","Fields_all_overlap_futureincurrent_diss_a","Fields_all_future_dissolve_a","Fields_all_current_dissolve_a"]

#Create list of files to delete
#DeleteList=[]
#for feature in fclist:
#    if not feature in SaveFiles:
#        DeleteList.append (feature)
#    else:
#        pass
#for item in DeleteList:
#    arcpy.Delete_management(item, dataType)
#    print "%s deleted" % (item)

print "deleting unnecesary featureclasses"
for feature in fclist:
        if feature == target_layer:
            pass
        else:    
            arcpy.Delete_management(feature + Parser)
            
print "deleting unnecessary tables" 
tables = arcpy.ListTables()
for table in tables:
    arcpy.Delete_management(table, dataType)  
    print "%s deleted" % (table)    

print ("Total elapsed time (seconds): " + str(time.clock() - beginTime))

