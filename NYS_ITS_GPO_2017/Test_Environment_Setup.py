# coding: utf-8
import arcpy
from datetime import datetime
startTime = datetime.now()

# Define the workspace and the path to the streetsegment.gdb
PATH = "c:\Users\cbrimm\Desktop\TEST_gisdata\TESTER"  # EDIT THIS PATH TO FIT YOUR DIRECTORY
print("Path: "+PATH)
arcpy.env.workspace = PATH + "\streetsegment.gdb"
max_rows = 0


def checkfield(n):
    global max_rows
    field = n
    temp_path = PATH + "\streetsegment.gdb\streetsegment"
    row_count = 0
    cursor = arcpy.UpdateCursor(temp_path)
    for row in cursor:
        if row.isNull(field):
            row_count = row_count + 1
        else:
            break
    print(row_count + 1)
    row_count = row_count + 8
    if row_count > max_rows:
        max_rows = row_count

checkfield("POSTTYPE")
checkfield("POSTDIRECTIONAL")
checkfield("PreDirectional")
checkfield("PRETYPE")
checkfield("OneWay")

print("The minimum amount of rows needed to display data is: " + str(max_rows))
print("Creating TEST1.gdb")
if arcpy.Exists(PATH + "\TEST1.gdb"):
    arcpy.Delete_management(PATH+"\TEST1.gdb\streetsegment.shp")
    arcpy.Delete_management(PATH+"\TEST1.gdb")
arcpy.CreateFileGDB_management(PATH, "TEST1.gdb")
print("Importing attributes from streetsegment")
arcpy.FeatureClassToFeatureClass_conversion("StreetSegment", PATH + "\TEST1.gdb", "streetsegment", "OBJECTID <= " + str(max_rows))
print("Time to complete: " + str(datetime.now() - startTime))