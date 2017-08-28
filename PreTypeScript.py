# coding: utf-8
import arcpy

PATH = "c:\Users\cbrimm\Desktop\TEST_gisdata"
arcpy.env.workspace = PATH + "\streetsegment.gdb"
edit = arcpy.da.Editor(PATH + "\streetsegment.gdb")

to_add = ["PRETYPE2"]

fieldList = arcpy.ListFields("streetsegment")
fieldName = [f.name for f in fieldList]
for field in to_add:
    if field == "PRETYPE2":
        arcpy.AddField_management("streetsegment", "PRETYPE2", "TEXT", field_length=2)

edit.startEditing()
edit.startOperation()
tempPath = PATH + "\streetsegment.gdb\streetsegment"
field = "Shield"
cursor = arcpy.UpdateCursor(tempPath)
for row in cursor:
    val = row.getValue(field)
    if val == "I" or val == "IC":
        row.setValue("PRETYPE2", "I")
        cursor.updateRow(row)
    elif val == "S" or val == "SC" or val == "SH":
        row.setValue("PRETYPE2", "SR")
        cursor.updateRow(row)
    elif val == "C" or val == "CT":
        row.setValue("PRETYPE2", "CR")
        cursor.updateRow(row)
    elif val == "U" or val == "UB" or val == "UC":
        row.setValue("PRETYPE2", "US")
        cursor.updateRow(row)
edit.stopOperation()
edit.stopEditing(True)