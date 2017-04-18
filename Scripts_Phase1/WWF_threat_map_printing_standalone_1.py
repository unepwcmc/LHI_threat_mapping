#script to export maps rasters one by one to as png/pdf - part 2 of 2. Works on the assumption that all layers in the TOC have their names and symbology updated
#modified from one used in geo-6 mapping workshop in July 2015 (May 2016)

#NOTE: User must do the following before running script:
#1. Right click on the legend and push all the layers in the TOC into the legend
#2: Change the name of the admin layer so that new folder is created to store results and that extent resets to the boundary of new admin layer

import arcpy
import os
import time
#list workspaces for inputs and outputs
arcpy.env.overwriteOutput = True
beginTime=time.clock()
################################################
# Create list of PP names

#Get list of priority places
fc = r"C:\Data\WWF\Study_scope\WWF_PP_Terr.gdb\WWF_PP_Terr"
field = "FLAG_NAME"
cursor = arcpy.SearchCursor(fc)
PP_list_temp=[]
PP_list=[]
PP_list_fishnet=[]
#PP_list_fishnet_buff=[]
for row in cursor:
    t=row.getValue(field)
    PP_list_temp.append(t)
    for i in PP_list_temp:
        t=str(i)
    g = t.replace(" ", "_")
    PP_list.append(g)
    for i in PP_list:
        s=str(i)+ "_fishnet"
    PP_list_fishnet.append(s)
    PP_list.sort()
    PP_list_fishnet.sort()
############################################################
####name of admin layer to keep displaying
adminLyr='Atlantic Forests' #change as needed
out_folder_path = "C:\Data\WWF\Final_maps" 
for PP in PP_list:
    if PP == adminLyr.replace(" ","_"):
#CreateFolder to store outputs maps
# Set local variables
        out_name = PP
# Execute CreateFolder
        arcpy.CreateFolder_management(out_folder_path, out_name)
        
outPath=out_folder_path + "\\" + out_name

####list workspaces for inputs and outputs
#Define outpath and workspace
        
arcpy.env.workspace = out_folder_path
mxd = arcpy.mapping.MapDocument("CURRENT")
mxd.activeView = 'PAGE_LAYOUT'

#mxd = arcpy.mapping.MapDocument("CURRENT")


#Create a fresh layer list
for df in arcpy.mapping.ListDataFrames(mxd):
    if (df.name=='Layers'):
        layers=arcpy.mapping.ListLayers(mxd,"*", df) 
print layers

###check that only maps in TOC that have corresponding layer files are actually printed
##
##df = arcpy.mapping.ListDataFrames(mxd)[0]
##import glob
##import arcpy
##import arcpy.mapping
##
###get list of lyr files in file directory
##lyr_list=[]
##filenames = glob.glob(r"C:\Data\WWF\Layer_files\*.lyr")
##for filename in filenames:
##    lyr_list.append(filename[24:-4])
    #lyr_list.sort
#updateLayer = arcpy.mapping.ListLayers(mxd, "*", "")
###updateLayer.sort
##count=0
##for updatelyr in updateLayer:
##    for sourcelyr in lyr_list:     
##        if updatelyr.name == sourcelyr[:-4]:
##            count=count+1
##            #print updatelyr.name,sourcelyr, count            
#Export the maps:
#print "Exporting maps for each layer"
#turn all layers off except ones on permanently
import glob
import arcpy
import arcpy.mapping

#get list of lyr files in file directory
lyr_list=[]
filenames = glob.glob(r"C:\Data\WWF\Layer_files\*.lyr")
for filename in filenames:
    lyr_list.append(filename[24:-4])
    
for layer in layers:
    if layer.name== adminLyr or layer.name=='National Borders':
        layer.visible=True
    else:
        layer.visible=False

arcpy.RefreshTOC()
arcpy.RefreshActiveView()

###create list of maps in TOC that have corresponding layer files so that they are printed and not others
map_list=[]
for i in lyr_list:
     for t in layers:
        if i == t.name:
            map_list.append(i)
#set map parameters
prjFile = r"C:\Users\briano\AppData\Roaming\ESRI\Desktop10.2\ArcMap\Coordinate Systems\WGS 1984.prj"  
sr = arcpy.SpatialReference(prjFile)
count=0
for layer in layers:
    layer.visible=True
    arcpy.RefreshTOC()
    arcpy.RefreshActiveView()
    if layer.name== adminLyr  or layer.name=='National Borders':
        print "skipping  printing layer"
    if layer.name==adminLyr:
        print "map extent is " + layer.name
        df.extent = layer.getSelectedExtent(True)    
    else:
        for maps in map_list:
            if layer.name== maps:
                df.spatialReference = sr
                mxd.save()
                layer.visible=True
                arcpy.RefreshTOC()
                arcpy.RefreshActiveView()  
                out_png=outPath + "\\"+ str(layer)+".png"
                legend = arcpy.mapping.ListLayoutElements(mxd,"LEGEND_ELEMENT")[0]
                #legend.updateItem(lyr, use_visible_extent = True)
                for lyr in legend.listLegendItemLayers():
                    #legend.elementHeight = 6  
                    #legend.elementWidth = 8
                    #legend.fontSize=9
                    legend.updateItem(lyr, use_visible_extent = True)
                print 'updateLegendItem'       
                try:
                    print out_png
                    #arcpy.mapping.ExportToPNG(mxd,out_png,resolution=600)
                    arcpy.mapping.ExportToPNG(mxd,out_png,resolution=300)
                    print "printing to file", layer
                    count=count+1
                    print "%s" %count + " maps printed"
                except:
                    print 'failed to write map'
                    pass
    if layer.name== adminLyr or layer.name=='National Borders':
        layer.visible=True
    else:
        layer.visible=False
           
print "Finished processing"
print("Total elapsed time (minutes): " + str((time.clock() - beginTime)/60))
