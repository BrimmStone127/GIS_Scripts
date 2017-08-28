# coding: utf-8
# NYS ITS GPO
# AUTHOR: CLAYTON BRIMM 7/10/17

# IMPORTS
import arcpy
from datetime import datetime
global start_time
global new_time
start_time = datetime.now()

# The main initiation method for the script
def main():
    setup()
    addFields()
    calculateNavDirection()
    calculatePostType()
    calculatePostDirect()
    calculatePreDirect()
  # createNYSTA()
    print "SCRIPT COMPLETE - TOTAL TIME: " + str((datetime.now() - start_time))

# Method sets up the work environment and defines the necessary paths to correctly run the script
def setup():
    # Define the workspace and the path to the streetsegment.gdb
    global edit
    global PATH
    PATH = "C:\Users\cbrimm\Desktop\TEST_gisdata"  # EDIT THIS PATH TO FIT YOUR DIRECTORY
    print("Path: "+PATH)
    arcpy.env.workspace = PATH + "\streetsegment.gdb"
    print("Using workspace: "+PATH + "\streetsegment.gdb")

# Adds the new fields that will be needed to the streetsegment shapefile
def addFields():
    # Add a fields to streetsegment
    print "ADDING FIELDS"
    # This is a array of the needed fields for streetsegment
    to_add = ["BLOCKAGE_MASK", "PREDIRECTIONAL2", "POSTDIRECTIONAL2", "POSTTYPE4", "NAVIGATIONDIRECTION9", "STREETNAME1", "PRETYPE2"]
    fieldList = arcpy.ListFields("streetsegment")
    fieldName = [f.name for f in fieldList]
    # This iterates across the attribute table and checks if the new field names exist, if they do then nothing happens, if not they are then created
    for field in to_add:
        if field in fieldName:
            print(field+" field already exists.")
        elif field == "BLOCKAGE_MASK":
            arcpy.AddField_management("streetsegment", "BLOCKAGE_MASK", "LONG")
            print("ADDED "+field+" FIELD.")
        elif field == "PREDIRECTIONAL2":
            arcpy.AddField_management("streetsegment", "PREDIRECTIONAL2", "TEXT", field_length=2)
            print("ADDED " + field + " FIELD.")
        elif field == "POSTDIRECTIONAL2":
            arcpy.AddField_management("streetsegment", "POSTDIRECTIONAL2", "TEXT", field_length=2)
            print("ADDED " + field + " FIELD.")
        elif field == "POSTTYPE4":
            arcpy.AddField_management("streetsegment", "POSTTYPE4", "TEXT", field_length=4)
            print("ADDED " + field + " FIELD.")
        elif field == "NAVIGATIONDIRECTION9":
            arcpy.AddField_management("streetsegment", "NAVIGATIONDIRECTION9", "TEXT", field_length=9)
            print("ADDED " + field + " FIELD.")
        elif field == "STREETNAME1":
            arcpy.AddField_management("streetsegment", "STREETNAME1", "TEXT", field_length=100)
            print("ADDED " + field + " FIELD.")
        elif field == "PRETYPE2":
            arcpy.AddField_management("streetsegment", "PRETYPE2", "TEXT", field_length=2)
            print("ADDED " + field + " FIELD.")

# Calculates the NAVIGATIONDIRECTION9 field
def calculateNavDirection():
    # edit.startEditing(True, False)
    global change_count
    global null_count
    time1 = (datetime.now() - start_time)
    change_count = 0
    null_count = 0
    # edit.startOperation()
    print "CALCULATING NAVIGATIONDIRECTION9...",
    tempPath = PATH + "\streetsegment.gdb\streetsegment" #make sure to change gdb name
    field = "NavigationDirection"
    cursor = arcpy.UpdateCursor(tempPath)
    for row in cursor:
        val = row.getValue(field)
        if val == "E":
            row.setValue("NAVIGATIONDIRECTION9", "East")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "S":
            row.setValue("NAVIGATIONDIRECTION9", "South")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "N":
            row.setValue("NAVIGATIONDIRECTION9", "North")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "W":
            row.setValue("NAVIGATIONDIRECTION9", "West")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "NW":
            row.setValue("NAVIGATIONDIRECTION9", "Northwest")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "NE":
            row.setValue("NAVIGATIONDIRECTION9", "Northeast")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "SE":
            row.setValue("NAVIGATIONDIRECTION9", "Southeast")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "SW":
            row.setValue("NAVIGATIONDIRECTION9", "Southwest")
            cursor.updateRow(row)
            change_count = change_count + 1
        else:
            null_count = null_count + 1
    # edit.stopOperation()
    print "DONE PROCESS TIME:",
    new_time = (datetime.now() - start_time) - time1
    print new_time,
    print "(ROWS FOUND NULL - " + str(null_count) + ") (ROWS CHANGED - " + str(change_count) + ")"

# Calculate POSTTYPE4 field
def calculatePostType():
    # edit.startOperation()
    time1 = (datetime.now() - start_time)
    print "CALCULATING POSTTYPE4..............",
    arcpy.CalculateField_management("streetsegment", "POSTTYPE4", "Left([PostType],4)")
    # edit.stopOperation()
    print "DONE PROCESS TIME:",
    new_time = (datetime.now() - start_time) - time1
    print new_time

# Calculates the Postdirectional2 field
def calculatePostDirect():
    # edit.startOperation()
    time1 = (datetime.now() - start_time)
    global change_count
    global null_count
    change_count = 0
    null_count = 0
    print "CALCULATING POSTDIRECTIONAL2.......",
    tempPath = PATH + "\streetsegment.gdb\streetsegment"  # make sure to change gdb name
    field = "POSTDIRECTIONAL"
    cursor = arcpy.UpdateCursor(tempPath)
    for row in cursor:
        val = row.getValue(field)
        if val == "E":
            row.setValue("POSTDIRECTIONAL2", "E")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "S":
            row.setValue("POSTDIRECTIONAL2", "S")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "N":
            row.setValue("POSTDIRECTIONAL2", "N")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "W":
            row.setValue("POSTDIRECTIONAL2", "W")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "NW":
            row.setValue("POSTDIRECTIONAL2", "NW")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "NE":
            row.setValue("POSTDIRECTIONAL2", "NE")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "SE":
            row.setValue("POSTDIRECTIONAL2", "SE")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "SW":
            row.setValue("POSTDIRECTIONAL2", "SW")
            cursor.updateRow(row)
            change_count = change_count + 1
        else:
            null_count = null_count + 1
    # edit.stopOperation()
    print "DONE PROCESS TIME:",
    new_time = (datetime.now() - start_time) - time1
    print new_time,
    print "(ROWS FOUND NULL - " + str(null_count) + ") (ROWS CHANGED - " + str(change_count) + ")"

# Calculates the PREDIRECTIONAL2 field
def calculatePreDirect():
    # Calculate PREDIRECTIONAL2
    # edit.startOperation()
    time1 = (datetime.now() - start_time)
    global change_count
    global null_count
    change_count = 0
    null_count = 0
    print "CALCULATING PREDIRECTIONAL2........",
    tempPath = PATH + "\streetsegment.gdb\streetsegment"  # make sure to change gdb name
    field = "PREDIRECTIONAL"
    cursor = arcpy.UpdateCursor(tempPath)
    for row in cursor:
        val = row.getValue(field)
        if val == "E":
            row.setValue("PREDIRECTIONAL2", "E")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "S":
            row.setValue("PREDIRECTIONAL2", "S")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "N":
            row.setValue("PREDIRECTIONAL2", "N")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "W":
            row.setValue("PREDIRECTIONAL2", "W")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "NW":
            row.setValue("PREDIRECTIONAL2", "NW")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "NE":
            row.setValue("PREDIRECTIONAL2", "NE")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "SE":
            row.setValue("PREDIRECTIONAL2", "SE")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "SW":
            row.setValue("PREDIRECTIONAL2", "SW")
            cursor.updateRow(row)
            change_count = change_count + 1
        else:
            null_count = null_count + 1
    # edit.stopOperation()
    print "DONE PROCESS TIME:",
    new_time = (datetime.now() - start_time) - time1
    print new_time,
    print "(ROWS FOUND NULL - " + str(null_count) + ") (ROWS CHANGED - " + str(change_count) + ")"

if __name__ == '__main__':
    main()