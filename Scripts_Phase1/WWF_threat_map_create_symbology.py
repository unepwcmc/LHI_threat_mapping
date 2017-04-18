#This script is 1 of 2 in threat map production. Its purpose is to change the layer names to generic ones and update their symbology.
#Once finished the layers are ready for step 2 - map layout and export to final map

#NOTE: The user has to manually load all the datasets (.tif) into the TOC of the MXD first with an appropriate WWF-PP boundary and country layer

import arcpy
import time
beginTime = time.clock()

#set to overwrite existing outputs
arcpy.env.overwriteOutput = True
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
#Create lists of layers in current data frame
#mxd = arcpy.mapping.MapDocument("C:\\Data\\WWF\\MXD\\Test_layout.mxd")
mxd = arcpy.mapping.MapDocument("CURRENT")
layers = arcpy.mapping.ListLayers(mxd)
for layer in layers:
    for PP in PP_list:
        if layer.name  == str(PP):
            newname = str(PP).replace("_"," ")
            layer.name = newname

        if layer.name  == str(PP) + "_access_risk_road.tif":
            newname = "Road accessibility risk" #str(PP).replace("_"," ") + " " + "Number of active mine facilities in 2008"
            layer.name = newname
            
        if layer.name  == str(PP) + "_ACT_MINE_COMMODITY.tif":
            newname = "Mining plant commodity" #str(PP).replace("_"," ") + " " + "Number of active mine facilities in 2008"
            layer.name = newname

        if layer.name  == str(PP) + "_ACT_MINE_COUNT.tif":
            newname = "Number of  mining plants" #str(PP).replace("_"," ") + " " + "Number of active mine facilities in 2008"
            layer.name = newname    
            
        if layer.name  == str(PP) + "_access_risk_port.tif":
            newname = "Port accessibility risk" #str(PP).replace("_"," ") + " " + "Number of active mine facilities in 2008"
            layer.name = newname    
                #Layer 1
        if layer.name  == str(PP) + "_AREA_GEO_LOG.tif":
            newname = "Area of logging concession(2014)" #str(PP).replace("_"," ") + " " + "Number of active mine facilities in 2008"
            layer.name = newname    
            
        if layer.name  == str(PP) + "_AREA_GEO_OIL.tif":
            newname = "Area of oil concession(2013)" #str(PP).replace("_"," ") + " " + "Number of active mine facilities in 2008"
            layer.name = newname
            
        if layer.name  == str(PP) + "_AREA_GEO_WOOD.tif":
            newname = "Area of wood fibre concession(2013)" #str(PP).replace("_"," ") + " " + "Number of active mine facilities in 2008"
            layer.name = newname
            
        if layer.name  == str(PP) + "_AREA_GEO_MINE.tif":
            newname = "Area of mining concession(2013)" #str(PP).replace("_"," ") + " " + "Number of active mine facilities in 2008"
            layer.name = newname
            
                #Layer 1
        if layer.name  == str(PP) + "_ACT_MINE_FACILITIES.tif":
            newname = "Number of active mine facilities in 2008" #str(PP).replace("_"," ") + " " + "Number of active mine facilities in 2008"
            layer.name = newname
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()
                #Layer 2
        if layer.name  == str(PP) + "_AREA_GEO_Res.tif":
            newname = "Reservoir area (km2) in 2010"
            layer.name = newname
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()
                #Layer 3
        if layer.name  == str(PP) + "_ARMED_CONFLICT.tif":
            newname =  "Number of armed conflicts (1997-2014)"
            layer.name = newname
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()
#Layer 4

        if layer.name  == str(PP) + "_DAM_COUNT.tif":
            newname = "Number of dams (2010)"
            layer.name = newname
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()   


        if layer.name  == str(PP) + "_Mean_barley_Production_t.tif":
            newname =  "Mean barley production (tonnes)in 2000"
            layer.name = newname   
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()


        if layer.name  == str(PP) + "_Mean_rapeseed_Production_t.tif":
            newname = "Mean rapeseed production (tonnes)in 2000"
            layer.name = newname    
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()
            
        if layer.name  == str(PP) + "_Mean_cassava_Production_t.tif":
            newname = "Mean cassava production (tonnes)in 2000"
            layer.name = newname    
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()
 
        if layer.name  == str(PP) + "_Mean_cotton_Production_t.tif":
            newname ="Mean cotton production (tonnes)in 2000"
            layer.name = newname    
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()
    
  
        if layer.name  == str(PP) + "_Mean_CropFract.tif":
            newname =  "Mean crop fraction (2005)"
            layer.name = newname    
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()   


        if layer.name  == str(PP) + "_Mean_Glb_Cat_density.tif":
            newname = "Mean cattle density (2006) in heads per km2"
            layer.name = newname    
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()   

        if layer.name  == str(PP) + "_Mean_Glb_chi_density.tif":
            newname =  "Mean chicken density (2006) in heads per km2"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()  


        if layer.name  == str(PP) + "_Mean_GLb_Duc_density.tif":
            newname ="Mean duck density (2006) in heads per km2"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC() 


        if layer.name  == str(PP) + "_Mean_Glb_Goa_density.tif":
            newname = "Mean goat density (2006) in heads per km2"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC() 


        if layer.name  == str(PP) + "_Mean_Glb_Pig_density.tif":
            newname =  "Mean pig density (2006) in heads per km2"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC() 


        if layer.name  == str(PP) + "_Mean_Glb_She_density.tif":
            newname =  "Mean sheep density (2006) in heads per km2"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC() 


        if layer.name  == str(PP) + "_Mean_groundnut_Production_t.tif":
            newname =  "Mean groundnut production (tonnes)in 2000"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()

 
        if layer.name  == str(PP) + "_Mean_millet_Production_t.tif":
            newname = "Mean millet production (tonnes)in 2000"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()

        if layer.name  == str(PP) + "_Mean_maize_Production_t.tif":
            newname = "Mean maize production (tonnes)in 2000"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()


        if layer.name  == str(PP) + "_Mean_Nitroge_kg.tif":
            newname =  "Excess nitrogen application (kg)in 2000"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()


        if layer.name  == str(PP) + "_Mean_oilpalm_Production_t.tif":
            newname = "Mean oilpalm production (tonnes)in 2000"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()

 
        if layer.name  == str(PP) + "_Mean_Phospho_kg.tif":
            newname =  "Excess phosphorus application (kg)in 2000"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()



        if layer.name  == str(PP) + "_Mean_potato_Production_t.tif":
            newname =  "Mean potato production (tonnes)in 2000"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()



        if layer.name  == str(PP) + "_Mean_rice_Production_t.tif":
            newname =  "Mean rice production (tonnes)in 2000"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()


        if layer.name  == str(PP) + "_Mean_rye_Production_t.tif":
            newname = "Mean rye production (tonnes)in 2000"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()


        if layer.name  == str(PP) + "_Mean_sorghum_Production_t.tif":
            newname =  "Mean sorghum production (tonnes)in 2000"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()


        if layer.name  == str(PP) + "_Mean_soybean_Production_t.tif":
            newname =  "Mean soybean production (tonnes)in 2000"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()


        if layer.name  == str(PP) + "_Mean_sugarbeet_Production_t.tif":
            newname = "Mean sugarbeet production (tonnes)in 2000"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()


        if layer.name  == str(PP) + "_Mean_sugarcane_Production_t.tif":
            newname =  "Mean sugarcane production (tonnes)in 2000"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()


        if layer.name  == str(PP) + "_Mean_sunflower_Production_t.tif":
            newname = "Mean sunflower production (tonnes)in 2000"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()


        if layer.name  == str(PP) + "_Mean_travel_time_hrs.tif":
            newname = "Mean travel time (hours) in 2000"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()


        if layer.name  == str(PP) + "_Mean_wheat_Production_t.tif":
            newname = "Mean wheat production (tonnes) in 2000"
            layer.name = newname      
#arcpy.RefreshActiveView()
#arcpy.RefreshTOC()


        if layer.name  == str(PP) + "_Road_Density.tif":
            newname = "Mean road density (km per km2) 1980-2010"
            layer.name = newname      
arcpy.RefreshActiveView()
arcpy.RefreshTOC()

#############################     
#update their symbology:

#Retrieve the symbology from existing layer files:
  
#Create new list of layers with their new names
for df in arcpy.mapping.ListDataFrames(mxd):
    if (df.name=='Layers'):
            layers=arcpy.mapping.ListLayers(mxd,"*", df) 
            #for layer in layers:
               # if layer not in  NonList:
                   # LayerList.append(layer)
#layers=layers[1:19]
print layers
#Source layer files
##lyrFile1 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Excess nitrogen application (kg)in 2000.lyr")
##lyrFile2 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Excess phosphorus application (kg)in 2000.lyr")
##lyrFile3 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean barley production (tonnes)in 2000.lyr")
##lyrFile4 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean cassava production (tonnes)in 2000.lyr")
##lyrFile5 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean cattle density (2006) in heads per km2.lyr")
##lyrFile6 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean chicken density (2006) in heads per km2.lyr")
##lyrFile7 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean pig density (2006) in heads per km2.lyr")
##lyrFile8 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean cotton production (tonnes)in 2000.lyr")
##lyrFile9 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean crop fraction (2005).lyr")
##lyrFile10 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean duck density (2006) in heads per km2.lyr")
##lyrFile11 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean goat density (2006) in heads per km2.lyr")
##lyrFile12 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean groundnut production (tonnes)in 2000.lyr")
##lyrFile13 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean maize production (tonnes)in 2000.lyr")
##lyrFile14 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean millet production (tonnes)in 2000.lyr")
##lyrFile15 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean oilpalm production (tonnes)in 2000.lyr")
##lyrFile16 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean potato production (tonnes)in 2000.lyr")
##lyrFile17 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean rapeseed production (tonnes)in 2000.lyr")
##lyrFile18 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean road density (km per km2) 1980-2010.lyr")
##lyrFile19 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean rye production (tonnes)in 2000.lyr")
##lyrFile20 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean sheep density (2006) in heads per km2.lyr")
##lyrFile21 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean sorghum production (tonnes)in 2000.lyr")
##lyrFile22 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean soybean production (tonnes)in 2000.lyr")
##lyrFile23 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean sugarbeet production (tonnes)in 2000.lyr")
##lyrFile24 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean sugarcane production (tonnes)in 2000.lyr")
##lyrFile25 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean sunflower production (tonnes)in 2000.lyr")
##lyrFile26 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean travel time (hours) in 2000.lyr")
##lyrFile27 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean wheat production (tonnes) in 2000.lyr")
##lyrFile28 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Number of active mine facilities in 2008.lyr")
##lyrFile29 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Number of armed conflicts (1997-2014).lyr")
##lyrFile30 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Number of dams (2010).lyr")
##lyrFile31 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Reservoir area (km2) in 2010.lyr")
##lyrFile32 = arcpy.mapping.Layer(r"C:\Data\WWF\Layer_files\Mean rice production (tonnes)in 2000.lyr")


# update the symbology of re-named rasters with the layer files
df = arcpy.mapping.ListDataFrames(mxd)[0]
import glob
import arcpy
import arcpy.mapping

#get list of lyr files in file directory
lyr_list=[]
filenames = glob.glob(r"C:\Data\WWF\Layer_files\*.lyr")
for filename in filenames:
    lyr_list.append(filename[24:])
    #lyr_list.sort
updateLayer = arcpy.mapping.ListLayers(mxd, "*", "")
#updateLayer.sort
count=0
for updatelyr in updateLayer:
    for sourcelyr in lyr_list:     
        if updatelyr.name == sourcelyr[:-4]:
            count=count+1
            #print updatelyr.name,sourcelyr, count
            #if count-1==len(filenames):
                #for lyr in updateLayer:
            sourceLayer = arcpy.mapping.Layer('C:\\Data\\WWF\\Layer_files\\' + sourcelyr)
            arcpy.mapping.UpdateLayer(df, updatelyr,sourceLayer)
            print updatelyr, "symbology updated"
            print "%s" %count + " layers updated"                
    
print "Finished processing"
print("Total elapsed time (minutes): " + str((time.clock() - beginTime)/60))

    
    



