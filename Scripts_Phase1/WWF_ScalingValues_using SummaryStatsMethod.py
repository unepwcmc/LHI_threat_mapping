arcpy.env.workspace=r"C:\Data\WWF\Processing\African_Rift_Lakes.gdb"
fc= "African_Rift_Lakes_fishnet"
arcpy.env.overwriteOutput=True

intable = fc
outtable = "minstats"
casefield = ""
stats = []

for field in arcpy.ListFields(intable):
    if field.type != "Geometry":
        stats.append([field.name, "MIN"])


arcpy.Statistics_analysis(intable, outtable, stats[6:],casefield)
