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

#function to extract ports based on harbour size to new feature classes using an attribute query
##def split_ports(fc):
##        out_grid=fc + "_lyr"
##        fields=["HARBORSIZE","MAX_VESSEL"]
##        arcpy.MakeFeatureLayer_management(fc,out_grid)
##        # Use SearchCursor with list comprehension to return a  unique set of values for harbor size
##        values_HARBORSIZE=[row[0]for row in arcpy.da.SearchCursor(fc, fields)]
##        uniqueValues_HARBORSIZE = set(values_HARBORSIZE)
##        # Use SearchCursor with list comprehension to return a  unique set of values for max vessel
##        values_MAX_VESSEL=[row[1]for row in arcpy.da.SearchCursor(fc, fields)]
##        uniqueValues_MAX_VESSEL = set(values_MAX_VESSEL)
##        
##        for harbour in list(uniqueValues_HARBORSIZE):
##                for vessel in list(uniqueValues_MAX_VESSEL):
##                    where_clause="HARBORSIZE = '" + str(harbour) + "'" + " AND " + "MAX_VESSEL = '" + str(vessel)+ "'"
##                    arcpy.SelectLayerByAttribute_management(out_grid,"NEW_SELECTION",where_clause)
##                    matchcount = int(arcpy.GetCount_management(out_grid)[0])
##                    if arcpy.Exists (fc + "%s" %harbour + "%s" %vessel):
##                            print fc + "%s" %harbour + "%s" %vessel + "already exists"
##                            
##                    else:
##                         if matchcount == 0:
##                                print('no ports have a  harbour size matching criteria')
##                         else:  
##                                arcpy.CopyFeatures_management(out_grid, fc + "%s" %harbour + "%s" %vessel)
##                                print('{0} ports that matched criteria written to {1}'.format(
##                                    matchcount,"%s" %fc + "%s" %harbour + "%s" %vessel))   
        

        

# function to calculate access 'risk categories'
def Access_Risk(port_input_fields):
    Min_dist = port_input_fields[2]
    Harb_size= port_input_fields[0]
    Vess_size= port_input_fields[1]                       
   
    #logic for LARGE/LARGE cat
    if ((Min_dist < 500000 and Min_dist != -1) and Harb_size=='L'and Vess_size=='L'):
        return '17'
    elif (Min_dist >= 500000 and Harb_size=='L'and Vess_size=='L'):
        return '16'
    # Large/med
    elif ((Min_dist < 500000 and Min_dist != -1) and Harb_size=='L'and Vess_size=='M'):
        return '15'
    elif (Min_dist >= 500000 and Harb_size=='L'and Vess_size=='M'):
        return '14'
    # Med/large
    elif ((Min_dist < 500000 and Min_dist != -1) and Harb_size=='M'and Vess_size=='L'):
        return '13'
    elif (Min_dist >= 500000 and Harb_size=='M'and Vess_size=='L'):
        return '12'
    # mED/med
    elif ((Min_dist < 500000 and Min_dist != -1) and Harb_size=='M'and Vess_size=='M'):
        return '11'
    elif (Min_dist >= 500000 and Harb_size=='M'and Vess_size=='M'):
        return '10'
    # small/large
    elif ((Min_dist < 500000 and Min_dist != -1) and Harb_size=='S'and Vess_size=='L'):
        return '9'
    elif (Min_dist >= 500000 and Harb_size=='S'and Vess_size=='L'):
        return '8'
   # Small/Med
    elif ((Min_dist < 500000 and Min_dist != -1) and Harb_size=='S'and Vess_size=='M'):
        return '7'
    elif (Min_dist >= 500000 and Harb_size=='S'and Vess_size=='M'):
        return '6'
   # V small/large
    elif ((Min_dist < 500000 and Min_dist != -1) and Harb_size=='V'and Vess_size=='L'):
        return '5'
    elif (Min_dist >= 500000 and Harb_size=='V'and Vess_size=='L'):
        return '4'
      # V small/Med
    elif ((Min_dist < 500000 and Min_dist != -1) and Harb_size=='V'and Vess_size=='M'):
        return '3'
    elif (Min_dist >= 500000 and Harb_size=='V'and Vess_size=='M'):
        return '2'
      # No threat
    elif (Min_dist ==-1 or (Min_dist <> -1 and Harb_size== None and Vess_size==None)):
        return '1'


    
#Starts Geoprocessing
arcpy.env.overwriteOutput = True
myWorkspace=r"C:\Data\WWF\Processing"
arcpy.env.workspace = myWorkspace
gdbList = arcpy.ListWorkspaces("*", "FileGDB")


#Get list of priority place names to be used as a root name for the port feature classes
fc = r"C:\Data\WWF\Study_scope\WWF_PP_Terr.gdb\WWF_PP_Terr"
field = "FLAG_NAME"
cursor = arcpy.SearchCursor(fc)
PP_list_ports=[]
PP_list_temp=[]
for row in cursor:
    t=row.getValue(field)
    PP_list_temp.append(t)
    for i in PP_list_temp:
        t=str(i)
    g = t.replace(" ", "_")
    PP_list_temp.append(g)
    for i in PP_list_temp:
        g=str(i)+ "_ports"
  # create port feature classes
    PP_list_ports.append(g)
    PP_list_ports.sort()


#Loop over each GDB to perform the work
for gdb in gdbList:
    if gdb=="Global_Processing.gdb":
        pass
    else:
        arcpy.env.workspace = gdb #--change working directory to each GDB in list
        WSpace=arcpy.env.workspace
        #arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(r"C:\Data\WWF\Processing\WWF_5min_grid_Moll.prj")
        fclist = arcpy.ListFeatureClasses()  
        for fc in fclist:
            for i in  PP_list_ports:
                if fc==i:
                        #Use the below function if needing to split harbour and vessel combinations and create new feature classes 
                    #split_ports(fc)
                        #===================================================================================
                    pos= fc.index('_ports')
                # CONVERT THE GRID CELLS TO POINTS(CENTROIDS)
                    if  arcpy.Exists(fc[:pos] + "_fishnet_GridToPoint"):
                        print fc[:pos] + "_fishnet_GridToPoint" + " exists - skipping file creation"
                    else:
                        arcpy.FeatureToPoint_management(fc,fc + "_GridToPoint",point_location="CENTROID")
                        print "converting the grid cells to points %s" %fc[:pos] + "_fishnet"
                 # PROJECT TO WGS84    
                    if  arcpy.Exists(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84"):
                        print fc[:pos] + "_GridToPoint" + "_WGS84" + " exists - skipping file creation"   
                    else:
                        arcpy.Project_management(fc + "_GridToPoint",fc + "_GridToPoint" + "_WGS84",out_coor_system="GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]",transform_method="#",in_coor_system="PROJCS['World_Mollweide',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mollweide'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],UNIT['Meter',1.0]]")
                        print "projecting s%" + fc[:pos] + "_fishnet_GridToPoint" + " to WGS84" 
## #===================================================================================
                         # THIS STEP CREATES A LIST OF VALUES FOR THE 2 ATTRIBUTES IN EACH FC:  HARBOR & VESSEL
                         # for the  'update cursor' method only
                        #fullPath = os.path.join(WSpace, fc)
##          # Reads My_shapefile for different values in the attribute
##                    rows = arcpy.SearchCursor(fullPath)
##                    row = rows.next()
##                    HARBOR_attribute_types = set([])
##                    VESSEL_attribute_types = set([])
##                    while row:
##                         HARBOR_attribute_types.add(row.HARBORSIZE) #<-- CHANGE my_attribute to the name of your attribute
##                         VESSEL_attribute_types.add(row.MAX_VESSEL)
##                         row = rows.next()
##                    #Master result list: all roads
##                    HARBOR_result = list(HARBOR_attribute_types)
##                    VESSEL_result = list(VESSEL_attribute_types)
##                    HARBOR_result.sort
##                    VESSEL_result.sort
##                    arcpy.env.overwriteOutput=True
                    # list of field names containing road type nearest distance values and the field to be updated by the cursor
#===================================================================================
                    #list all fields in the giant table
                    Allfields = arcpy.ListFields(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84")
                    
                     #Use the below function if needing to delete fields created already, e.g. in case of errors
                    
                            #Drop_fields="MIN_PORT_CLASS;ACCESS_PORT_RANK"
##                    for field in Allfields:
##                        if "_PORT" in str(field.name):
##                            arcpy.DeleteField_management(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84",field.name)
##                            print "deleting fields" "%s" %fc , "%s" %field.name
##                        elif str(field.name)=='NEAR_FID':
##                            arcpy.DeleteField_management(fc,field.name)
##                        elif str(field.name)=='NEAR_DIST':
##                            arcpy.DeleteField_management(fc,field.name)
##                            print "deleting " + "%s" %fc + "%s" %field.name
##                        else:
##                           pass   
#=====================================================================================
                    # THIS STEP ADDs A NEW FIELD: ACCESS_PORT_RANK from 1 (highest) to 17 (lowest)
                    #These fields ar optional if you want to use the 'update cursor' method and not the 'join' method 
                   #fields = [("MIN_DIST_PORT","DOUBLE","7","2","","Nearest distance to a port","NULLABLE","NON_REQUIRED",""),("MIN_PORT_CLASS","TEXT","","","","Combination of harbour size and max vessel size","NULLABLE","NON_REQUIRED",""),
                                  #("ACCESS_PORT_RANK","SHORT ","","","","Access category scaled from 1 (highest) to 7(no port within search radius)","NULLABLE","NON_REQUIRED","")]
                    fields = [("ACCESS_PORT_RANK","SHORT","","","","Access category scaled from 1 (highest) to 17(no port within search radius)","NULLABLE","NON_REQUIRED","")]
                    if len(arcpy.ListFields(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84","ACCESS_PORT_RANK"))>0:
                            print "Nearest port field already exist therefore not created" 
                    else:
                        for field in fields:
                            arcpy.AddField_management(*(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84",) + field)
                            print "Adding accessibility field"
#=====================================================================================
                              # THIS STEP calculates nearest distance to port
## # for the  'update cursor' method only:
                            
##                #Calculate nearest distance to port
##                            
##                    for i in HARBOR_result:
##                            for j in VESSEL_result:
##                                    near_features=fc + "%s"%i + "%s"%j
##                                    if arcpy.Exists (near_features):
                            #don't overwrite nearest distance field if it exists
                    if len(arcpy.ListFields(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84","NEAR_DIST"))>0:
                            print "field already exists  - nearest distance will not be calculated"
                    else:
                                   # CALCULATE DISTANCE FROM POINT TO NEAREST port (using combinations of port and vessel size)
                            arcpy.Near_analysis(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84",fc,search_radius="1000 Kilometers",location="NO_LOCATION",angle="NO_ANGLE",method="GEODESIC")
                            print "calculating nearest distance %s" %fc[:pos] + "_fishnet_GridToPoint" + "_WGS84",fc
                            # join the max vessel size and harbour size fields back to main table
                    if len(arcpy.ListFields(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84","HARBORSIZE"))>0:
                            print "fields already JOINED"
                    else:        
                            arcpy.JoinField_management(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84","NEAR_FID",fc,"OBJECTID","HARBORSIZE;MAX_VESSEL")
                            print "joining NEAR_FID" + " from " + fc
                            ### CLEAN UP UNWANTED FIELDS
                            arcpy.DeleteField_management(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84","NEAR_FID")
                            print "deleting NEAR_FID" + " from " + fc

#=====================================================================================
#TO CALCULATE ACCESSIBILITY METRICS

                    # logic for finding the min distance and populate the target fields 'ACCESS_PORT_RANK'
                    port_fields=[]

                    for field in  Allfields:
                        if str(field.name)=='NEAR_DIST':
                                port_fields.append(field.name)
                        elif str(field.name)=='HARBORSIZE':
                             port_fields.append(field.name)
                        elif str(field.name)=='MAX_VESSEL':
                              port_fields.append(field.name)
                        elif str(field.name)=='ACCESS_PORT_RANK':
                              port_fields.append(field.name)     
                        else:
                             pass
                        #sort the list
                    port_fields.sort()
                    
######                        
                    if 'ACCESS_PORT_RANK' not in port_fields:
                        raise Exception('target field not found')
                    if 'HARBORSIZE' not in port_fields:
                        raise Exception('target field not found')   
####
####                # to get the minimum distance:
####
                    with arcpy.da.UpdateCursor(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84", port_fields) as cursor:
                        for row in cursor:
                            # all input port distances and attributes of interest
                            port_input_fields = row[1:4]
                            # the target field: port accessibility class
                            row[0] = Access_Risk(port_input_fields)
                            cursor.updateRow(row)
######                            
                    print "port accessibility category updated!"
  #=====================================================================================

                    # Create categorical 'access risk' raster layer
                    if arcpy.Exists(fc[:pos] + "_access_ports"):
                         print str(fc[:pos]).replace("_"," ") + " port accessiblity map exists - skipping raster creation"
                    else:
                         arcpy.env.overwriteOutput=True
                         arcpy.FeatureToRaster_conversion(fc[:pos] + "_fishnet_GridToPoint" + "_WGS84","ACCESS_PORT_RANK",fc[:pos] + "_access_risk_port","0.1")
                         print str(fc[:pos]).replace("_"," ") + " port accessiblity map created!"



# end time
print 'finished run: %s\n\n' % (datetime.datetime.now() - start)
