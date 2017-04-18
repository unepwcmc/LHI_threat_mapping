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
   # return        
