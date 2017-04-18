#Python code for ArcMap 10.2, Python v 2.7
# Code development by Brian O' Connor June 2015 (and later adapted for WWF threat mapping work October 2015)
import sys, os
import os
import arcpy
from arcpy import env
import time

beginTime = time.clock()

#set to overwrite existing outputs
arcpy.env.overwriteOutput = False

#set workspace for inputs and outputs
arcpy.env.workspace=r"C:\Data\WWF\Study_scope\Buffer\Terrestrial_PP"
#tempFolder="C:\Data\WWF\Processing"
outfolder=r"C:\Data\WWF\Processing"
#infolder=r"C:\Data\WWF\Study_scope\Buffer\Terrestrial_PP"

# make list of the Priority Places (PP) shapefiles
fclist =  arcpy.ListFeatureClasses()

# STEP1: Create file geodatabases to store results of processing (one per PP)
      #create a series of lists to get root name of file geodatabase
for fc in fclist:
    fc=arcpy.ValidateTableName(str(fc[:-4]))
    str(fc)
    out_name = str(fc)
    #Create GDB (if they don't already exist)
    newDB = outfolder + "\\" + out_name

    if os.path.exists(newDB + ".gdb"):
        print "Output database" +newDB+ " exists - skipping database creation"
    else:
        print "Executing CreateFileGDB: "+newDB
        arcpy.CreateFileGDB_management(outfolder,out_name)
        
# STEP2:Copy PP shapefile to its respective file geodatabase
arcpy.env.workspace =r"C:\Data\WWF\Processing"
workspaces = arcpy.ListWorkspaces("*", "FileGDB")
for i in workspaces:
    for fc in fclist:
        if fc [:-4]== i[23:-4]: # if root name of shapefile matches root name of GDB
            try:
                print "copying " + fc + " to " + i
                arcpy.CopyFeatures_management("C:\\Data\\WWF\\Study_scope\\Buffer\Terrestrial_PP\\"+fc,i+"\\"+fc [:-4])
            except:
                print "shapefiles already copied over"

# STEP3: Convert multipart polygons to single part
myWorkspace=r"C:\Data\WWF\Processing"
arcpy.env.workspace = myWorkspace #refresh workspace location
# Create variables for the input and output feature classes
gdbList = arcpy.ListWorkspaces("*", "FileGDB")
for gdb in gdbList:
    arcpy.env.workspace = gdb               #--change working directory to each GDB in list
    fclist = arcpy.ListFeatureClasses()  
    for fc in fclist:
        inFeatureClass = myWorkspace + "\\" + fc + ".gdb"+ "\\" + fc
        outFeatureClass =  inFeatureClass + "_sp"
        try:
    # Create list of all fields in inFeatureClass
            fieldNameList = [field.name for field in arcpy.ListFields(inFeatureClass)]
 # Add a field to the input this will be used as a unique identifier
            arcpy.AddField_management(inFeatureClass, "tmpUID", "double")
            print "adding unique identifier field to the table" + "'%s'" %fc
 
    # Determine what the name of the Object ID is 
            OIDFieldName = arcpy.Describe(inFeatureClass).OIDFieldName
   
    # Calculate the tmpUID to the OID
            arcpy.CalculateField_management(inFeatureClass, "tmpUID","[" + OIDFieldName + "]")
            print "Calculating the tmpUID to the OID" + "'%s'" %fc
    # Run the tool to create a new fc with only singlepart features
            arcpy.MultipartToSinglepart_management(inFeatureClass, outFeatureClass)
            print "creating a new fc with only singlepart features" + "'%s'" %fc
    # Check if there is a different number of features in the output
    #   than there was in the input
            inCount = int(arcpy.GetCount_management(inFeatureClass).getOutput(0))
            outCount = int(arcpy.GetCount_management(outFeatureClass).getOutput(0))
            print "There are" + "%d" %inCount + " input features and " + "%d" %outCount + "output features for " + "'%s'" %fc
            #if inCount != outCount:
        # If there is a difference, print out the FID of the input 
        #   features which were multipart
                #arcpy.Frequency_analysis(outFeatureClass,outFeatureClass + "_freq", "tmpUID")
 
        # Use a search cursor to go through the table, and print the tmpUID 
               # print("Multipart features from {0}".format(inFeatureClass))
                #for row in arcpy.da.SearchCursor(outFeatureClass + "_freq","tmpUID"], "FREQUENCY > 1"):
                   # print int(row[0])
          #  else:
               #print("No multipart features were found")
        except arcpy.ExecuteError:
            print arcpy.GetMessages()
        except Exception as e:
            print e


# STEP4: Calculate 50% buffer area using geodesic area tool
#(a) create a temporary copy of the layer
for i in workspaces:
    arcpy.env.workspace = i              #--change working directory to each GDB in list
    fclist = arcpy.ListFeatureClasses()  
    fc_temp=fclist[1] 
    if fc_temp [:-4]== i[23:-5]: # if root name of shapefile matches root name of GDB
        arcpy.CopyFeatures_management(fc_temp,i+"\\"+fc_temp + "_temp")
        print "copying " + fc_temp + " to " + i+"\\"+fc_temp + "_temp"
#(b) reproject it to Equal Area
    in_dataset= fc_temp + "_temp"
    out_dataset= fc_temp + "_temp_eq"
    arcpy.Project_management(in_dataset,out_dataset,out_coor_system="PROJCS['World_Mollweide',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mollweide'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],UNIT['Meter',1.0]]",transform_method="#",in_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]")                                                   
    print "projecting " + "%s" %fc_temp + " to  Equal Area projection"

#(c) calculate the geodesic areas
    Input_Features=out_dataset
    Geometry_Properties="AREA_GEODESIC"
    Length_Unit="#"
    Area_Unit="SQUARE_KILOMETERS"
    Coordinate_System="#"
    arcpy.AddGeometryAttributes_management(Input_Features,Geometry_Properties,Length_Unit,Area_Unit,Coordinate_System)
    print "adding geodesic area field to " + "%s" %Input_Features

#(d) join the results to the original table(feature id and area)
    in_data=fc_temp
    in_field="OBJECTID"
    join_table=Input_Features
    join_field="OBJECTID"
    fields="AREA_GEO"
    arcpy.JoinField_management(in_data,in_field,join_table,join_field,fields)
    print "joining geodesic area field back to table: " + "%s" %Input_Features
#(e) Apply 50% of surface area buffer
# Add a distance field for the buffer(50% Of geodesic area)
    in_table=Input_Features
    field_name="buffer_dist"
    field_type="DOUBLE"
    field_precision="#"
    field_scale="#"
    field_length="#"
    field_alias="#"
    field_is_nullable="NULLABLE"
    field_is_required="NON_REQUIRED"
    field_domain="#"
    arcpy.AddField_management(in_table,field_name,field_type,field_precision,field_scale,field_length,field_alias, field_is_nullable,field_is_required,field_domain)
    print "Adding field to table: " + "%s" %in_table
    arcpy.CalculateField_management(in_table,field_name,expression="[AREA_GEO] *0.5",expression_type="VB",code_block="#")
    print "Calculating field: " + "%s" %in_table

# Apply buffer
    in_features=Input_Features
    out_feature_class=Input_Features + "_buff"
    buffer_distance_or_field="buffer_dist"
    line_side="OUTSIDE_ONLY"
    line_end_type="ROUND"
    dissolve_option="ALL"
    dissolve_field="#"
    arcpy.Buffer_analysis(in_features,out_feature_class,buffer_distance_or_field,line_side,line_end_type,dissolve_option,dissolve_field)
print "Buffering: " + "%s" %in_features
for i in workspaces:
    arcpy.env.workspace = i              #--change working directory to each GDB in list
    fclist = arcpy.ListFeatureClasses()  
        for fc in fclist:
            Input_Features=fclist[1]
    
    



# STEP5:Intersect threat layers with the grid

#Note - the grid is in an equal area projection, e.g. Mercator, and has been manually copied over to a geodatabase before running this script

#Select the features in the threat layer that touch the boundaries of the Priority places or its buffers and have some attribute criteria (to avoid processing data outside PPs)
    # Get the processing grid ready for intersection first  

target_layer = r"C:\Data\WWF\Processing\Global_Processing.gdb\WWF_5min_grid_Moll"
target_field = "FID_"+target_layer[45:]
target_fid_field="OBJECTID"

#calculate areas for main target layer if not already
#arcpy.AddGeometryAttributes_management(target_layer,Geometry_Properties="AREA_GEODESIC",Length_Unit="",Area_Unit="SQUARE_KILOMETERS",Coordinate_System="#") 
print "Geodesic area calculated for", target_layer
#Set variables for input threat layers:
countLine=0
countPoint=0
countArea=0
Parser="_intersect"

    #Select the threat layer 
arcpy.env.workspace=r"C:\Data\WWF\Processing\Global_Processing.gdb"
InFeatures = arcpy.ListFeatureClasses() 
Test=InFeatures[1]
# Make a layer from threat dataset
arcpy.MakeFeatureLayer_management(Test, 'Test_lyr') 
#Loop over each gdb and read fc into a list
arcpy.env.workspace=r"C:\Data\WWF\Processing"
gdbList = arcpy.ListWorkspaces("*", "FileGDB")
for gdb in gdbList:
    arcpy.env.workspace = gdb               #--change working directory to each GDB in list
    fclist = arcpy.ListFeatureClasses()  
    for fc in fclist:
        arcpy.env.extent = fclist[0]
        PP_temp = fclist[0]
# Select features from the threat layer which overlap the PP polygon and create a feature layer for each new selection (stored in the respective PP gdb)
        try:
            arcpy.SelectLayerByLocation_management(Test, 'intersect', PP_temp)
            # Within the previous selection, create a sub-selection 
            arcpy.SelectLayerByAttribute_management(Test, 'SUBSET_SELECTION', '"FATALITIES" > 0')
            print "running selection by location and attribute rules " + "%s" %PP_temp
            # If features matched criteria write them to a new feature class
            matchcount = int(arcpy.GetCount_management(Test).getOutput(0)) 
            if matchcount == 0:
                print('no features matched spatial and attribute criteria')
            else:
                arcpy.CopyFeatures_management(Test, Test + "_selection")
                print('{0} features that matched criteria written to {0}'.format(matchcount, Test + "_selection"))
        except:
            print "fail " + "%s" %PP_temp
# Begin intersections
        if fc != "ACLED_GIS_2015_selection": #swap in name of threat layer
            pass
        else:
            desc = arcpy.Describe(fc)
            desc = desc.shapeType
            print  "Featureclass is type :" + str(desc)
            if str(desc)=='Point':
                countPoint=countPoint+1
                inFeatures = [fc, target_layer]
                arcpy.Intersect_analysis(inFeatures, fc + Parser,"ONLY_FID","#","POINT")

            if str(desc)=='Polyline':
                countLine=countLine+1
                inFeatures = [fc, target_layer]
                arcpy.Intersect_analysis(inFeatures, fc + Parser, "ONLY_FID", "","LINE")

            elif str(desc)=='Polygon':
                countArea=countLine+1
                inFeatures = [fc, target_layer]
                arcpy.Intersect_analysis(inFeatures, fc + Parser, "ONLY_FID", "","INPUT")

print fclist
print countLine,"line features have been intersected,",countPoint,"point features have been intersected and", countArea,"polygon features have been intersected"
#Make a separate list of the intersected point and line layers
feature_type_line='Polyline'
feature_type_point='Point'
feature_type_area='Polygon'
fclistLine = arcpy.ListFeatureClasses("*_intersect",feature_type_line,"")
fclistPoint = arcpy.ListFeatureClasses("*_intersect",feature_type_point,"")
fclistArea = arcpy.ListFeatureClasses("*_intersect",feature_type_area,"")


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
    









