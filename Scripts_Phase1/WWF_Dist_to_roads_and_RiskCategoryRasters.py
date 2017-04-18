#Python 2.7.5 (default, May 15 2013, 22:43:36) [MSC v.1500 32 bit (Intel)] on win32
#Type "copyright", "credits" or "license()" for more information.
#>>> 


import sys, os
import os
import arcpy
from arcpy import env

#start time
import datetime
start = datetime.datetime.now()
print 'start run: %s\n' % (start)

#funtion to remove unwanted values from a list
def remove_values_from_list(the_list, val):
        while val in the_list:
            the_list.remove(val)

# function to find min road distance in list
def find_min_roads(major_roads):
    if major_roads == [-1]*len(major_roads):
        return -1
    else:
        remove_values_from_list(major_roads,-1)
        return min(major_roads)

# function to calculate access 'risk categories'
def Access_Risk(major_minor_roads):
    major = major_minor_roads[0]
    minor = major_minor_roads[1]
    #logic for total access cat
    if ((major <= 50000 and major != -1) and (minor <=50000 and minor != -1)):
        return 'total access'
    #logic for v high risk cat
    elif ((major<=50000 and major != -1)and (minor>50000 and minor != -1))or ((major >50000 and major!= -1) and (minor<=50000 and minor != -1)):
        return 'very high'
    #logic for high risk cat
    elif ((major<=50000 and major != -1)and minor==-1) or ((minor>50000 and minor!= -1) and (major >50000 and major!= -1)):
        return 'high'
    #logic for medium risk cat
    elif ((minor>50000 and minor!= -1) and major ==-1)or ((major>50000 and major!= -1) and minor ==-1):
        return 'medium'
    #logic for low risk cat
    elif ((minor<=50000 and minor != -1) and major ==-1):
        return 'low'
     #logic for v low risk cat
    elif minor==-1 and major ==-1:
        return 'no access'
      

    
#Starts Geoprocessing
arcpy.env.overwriteOutput = True

myWorkspace=r"C:\Data\WWF\Processing"
arcpy.env.workspace = myWorkspace
gdbList = arcpy.ListWorkspaces("*", "FileGDB")


#Set Input Output variables
#inputFile = fc #<-- CHANGE
#outDir = u"C:\Data\WWF\Test_processes\\" #<-- CHANGE
#Get list of priority places
fc = r"C:\Data\WWF\Study_scope\WWF_PP_Terr.gdb\WWF_PP_Terr"
field = "FLAG_NAME"
cursor = arcpy.SearchCursor(fc)
PP_list_fishnet=[]
PP_list_temp=[]
PP_list_roads=[]
for row in cursor:
    t=row.getValue(field)
    PP_list_temp.append(t)
    for i in PP_list_temp:
        t=str(i)
    g = t.replace(" ", "_")
    PP_list_temp.append(g)
    for i in PP_list_temp:
        g=str(i)+ "_fishnet"
        h=str(i)+ "_roads"
    PP_list_roads.append(h)
    PP_list_fishnet.append(g)
    PP_list_roads.sort()
    PP_list_fishnet.sort()
#print PP_list_roads

#Loop over the roads file in each GDB to split into different road types
for gdb in gdbList:
    if gdb=="Global_Processing.gdb":
        pass
    else:
        arcpy.env.workspace = gdb #--change working directory to each GDB in list
        WSpace=arcpy.env.workspace
        #arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(r"C:\Data\WWF\Processing\WWF_5min_grid_Moll.prj")
        fclist = arcpy.ListFeatureClasses()  
        for fc in fclist:
            for i in  PP_list_roads:
                # SPLIT OUT THE ROADS LAYER BY FUNCTIONAL CLASS AND CREATE NEW LAYERS FOR EACH CLASS
                if fc==i:
                    pos= fc.index('_roads')
                # CONVERT THE GRID CELLS TO POINTS(CENTROIDS)
                    if  arcpy.Exists(fc[:pos] + "_fishnet_GridToPoint"):
                        print fc[:pos] + "_fishnet_GridToPoint" + " exists - skipping file creation"
                    else:
                        #arcpy.FeatureToPoint_management(fc,fc + "_GridToPoint",point_location="CENTROID")
                        print "converting the grid cells to points %s" %fc[:pos] + "_fishnet"
                 # PROJECT TO WGS84    
                    if arcpy.Exists(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84"):
                        print fc[:pos] + "_GridToPoint" + "_WGS84" + " exists - skipping file creation"   
                    else:
                        #arcpy.Project_management(fc + "_GridToPoint",fc + "_GridToPoint" + "_WGS84",out_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]",transform_method="#",in_coor_system="PROJCS['World_Mollweide',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mollweide'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],UNIT['Meter',1.0]]")
                        print "projecting s%" + fc[:pos] + "_fishnet_GridToPoint" + " to WGS84" 
                    fullPath = os.path.join(WSpace, fc)
          # Reads My_shapefile for different values in the attribute
                    rows = arcpy.SearchCursor(fullPath)
                    row = rows.next()
                    attribute_types = set([])
                    while row:
                        attribute_types.add(row.FCLASS) #<-- CHANGE my_attribute to the name of your attribute
                        row = rows.next()
                    #Master result list: all roads
                    result = list(attribute_types)
                    result.sort
                    arcpy.env.overwriteOutput=True

                    for i in range(len(result)):
                        if result[i] == 0:
                            result[i] = 'Unspecified'
                        if result[i] == 1:
                            result[i] = 'Highway'
                        if result[i] == 2:
                            result[i] = 'Primary'
                        if result[i] == 3:
                            result[i] = 'Secondary'
                        if result[i] == 4:
                            result[i] = 'Tertiary'
                        if result[i] == 5:
                            result[i] = 'Local_Urban'
                        if result[i] == 6:
                            result[i] = 'Trail'
                        if result[i] == 7:
                            result[i] = 'Private'

#TO CALCULATE ACCESSIBILITY METRICS
                        #1. ADD 3 NEW FIELDS FOR 2 GROUPS OF ROADS: MAJOR_ROADS (HIGHWAY, UNSPECIFIED, PRIM,SEC,TERT), MINOR_ROADS (TRAIL,LOCAL/URBAN,PRIVATE) AND ACCESSIBLITY CATEGORY 4 GROUPS OF ACCESS: HIGH, MEDIUM,LOW AND VERY LOW 
                    fields = [("MAJOR_RDS","DOUBLE","7","2","","Major Road Groups(Highway,Secondary,Primary,Tertiary,Unspec)","NULLABLE","NON_REQUIRED",""),
                                 ("MINOR_RDS","DOUBLE","7","2","","Minor Road Groups(Loc/Urban,Trail,Private)","NULLABLE","NON_REQUIRED",""),
                                  ("ACCESS_CAT","TEXT","","","15","Access category based on nearest distance and type of road","NULLABLE","NON_REQUIRED","")]
                    if len(arcpy.ListFields(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84","MAJOR_RDS"))>0:
                        print "Major and minor road fields already exist therefore not created" 
                    else:
                        for field in fields:
                            arcpy.AddField_management(*(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84",) + field)
                            print "Adding major , minor road and accessibility fields" 
#Make a list of tuples with FClass and correspondng attribute value
                    zipped=zip(list(attribute_types),result)                       
                    
                    #for field in lstFields:
        
                    for j,k in zipped:
                        near_features= fc + k 
                      #  else:   
                    #AND CALCULATE DISTANCE FROM POINT TO NEAREST ROAD (BY CLASS OF ROAD)
                        if len(arcpy.ListFields(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84","NEAR_FID" + k))>0:  
                            print "Field exists not calculating nearest distance %s" %k
                        else:
                            arcpy.Near_analysis(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84",near_features,search_radius="100 Kilometers",location="NO_LOCATION",angle="NO_ANGLE",method="GEODESIC")
                            print "calculating nearest distance %s" %fc[:pos] + "_fishnet_GridToPoint" + "_WGS84",near_features
                            arcpy.AlterField_management(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84","NEAR_FID","NEAR_FID" + "%s" %k,"NEAR_FID" + "%s" %k)
                            print "appending field name %s" %fc + "NEAR_FID" + "%s" %k
                            arcpy.AlterField_management(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84","NEAR_DIST","NEAR_DIST" + "%s" %k,"NEAR_DIST" + "%s" %k)
                            print "appending field name %s" %fc + "NEAR_DIST" + "%s" %k
                        # list of field names containing road type nearest distance values adn the field to be updated by the cursor
                    Allfields = arcpy.ListFields(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84")

                  #  print arcpy.env.workspace + os.sep + fc[:pos] + "_fishnet_GridToPoint" + "_WGS84"

                    # logic for finding the min major roads and populate the target field 'MAJOR_RDS'
                    MajorRoadfields=[]
                    for field in  Allfields:
                        if str(field.name).startswith("NEAR_DIST"):
                            if 'Unspecified' in str(field.name)or 'Highway' in str(field.name) or 'Primary' in str(field.name) or 'Secondary' in str(field.name) or 'Tertiary' in str(field.name):
                                MajorRoadfields.append(field.name)
                            else:
                                pass
                        else:
                            pass

                    for field in Allfields:

                        if str(field.name)=="MAJOR_RDS":
                            MajorRoadfields.append(field.name)
                        else:
                            pass
                        
                    if 'MAJOR_RDS' not in MajorRoadfields:
                        raise Exception('target field not found')

                    with arcpy.da.UpdateCursor(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84", MajorRoadfields) as cursor:
                        for row in cursor:
                            # all input major road
                            major_roads = row[:-1]

                            # the target major road field
                            row[-1] = find_min_roads(major_roads)

                            cursor.updateRow(row)
                    print "nearest distance to major road  calculated!"
                    #==============                                

                         # logic for finding the min minor roads and populate the target field 'MINOR_RDS'
                    MinorRoadfields=[]
                    for field in  Allfields:
                        if str(field.name).startswith("NEAR_DIST"):
                            if 'Trail' in str(field.name)or 'Private' in str(field.name) or 'Local_Urban'in str(field.name):
                                MinorRoadfields.append(field.name)
                            else:
                                pass
                        else:
                            pass

                    for field in Allfields:

                        if str(field.name)=="MINOR_RDS":
                            MinorRoadfields.append(field.name)
                        else:
                            pass
                        
                    if 'MINOR_RDS' not in MinorRoadfields:
                        raise Exception('target field not found')
                            
                    with arcpy.da.UpdateCursor(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84", MinorRoadfields) as cursor:
                        for row in cursor:
                            # all input major road
                            minor_roads = row[:-1]

                            # the target major road field
                            row[-1] = find_min_roads(minor_roads)

                            cursor.updateRow(row)
                    print "nearest distance to minor road  calculated!"
                        #==============
                    # logic for  populate the target field 'ACCESS_CAT'
                    
                    Access_cat_fields=[]
                    for field in  Allfields:
                        if str(field.name).endswith("_RDS"):
                            if 'MAJOR' in str(field.name) or 'MINOR' in str(field.name):
                                Access_cat_fields.append(field.name)
                            else:
                                pass
                        else:
                            pass

                    for field in  Allfields:
                        if str(field.name)=="ACCESS_CAT":
                            Access_cat_fields.append(field.name)
                        else:
                            pass
                                                
                    if 'ACCESS_CAT' not in Access_cat_fields:
                        raise Exception('target field not found')   
                        

                    with arcpy.da.UpdateCursor(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84", Access_cat_fields) as cursor:
                        for row in cursor:
                              # both input road categories
                            major_minor_roads = row[:-1]
                              # the target access field
                            row[-1] = Access_Risk(major_minor_roads)
                            
                            cursor.updateRow(row)
                    print "accessibility categories updated!"
                    temp_list_access_cats=[]
                # to know the number of accessiblity categories per PP

                    with arcpy.da.SearchCursor(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84", "ACCESS_CAT") as cursor:
                            for row in cursor:
                                    temp_list_access_cats.append(row[0])

                    print "%s" %len(list(set(temp_list_access_cats))) + " access categories calculated"
                     
                          #==============
                    # Create categorical 'access risk' raster layer
                   # if arcpy.Exists(fc[:pos] + "_access_risk"):
                       # print str(fc[:pos]).replace("_"," ") + " accessiblity map exists - skipping raster creation"
                   # else:                       
                    arcpy.FeatureToRaster_conversion(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84","ACCESS_CAT",fc[:pos] + "_access_risk","0.1")
                    print str(fc[:pos]).replace("_"," ") + " access risk map created!"



# end time
print 'finished run: %s\n\n' % (datetime.datetime.now() - start)
