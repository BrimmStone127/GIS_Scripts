# coding: utf-8
import arcpy
from datetime import datetime
global start_time
global new_time
start_time = datetime.now()


def main():
    setup()
    calculateBlockageMask()
    calculatePretype()
    calculateStreetname()
    createNYSTA()
    print "SCRIPT COMPLETE - TOTAL TIME: " + str((datetime.now() - start_time))


def setup():
    # Define the workspace and the path to the streetsegment.gdb
    global edit
    global PATH
    PATH = "C:\Users\cbrimm\Desktop\TEST_gisdata"  # EDIT THIS PATH TO FIT YOUR DIRECTORY
    print("Path: "+PATH)
    print("Using workspace: "+PATH + "\streetsegment.gdb")


def calculateBlockageMask():
    time1 = (datetime.now() - start_time)
    change_count = 0
    null_count = 0
    print"CALCULATING BLOCKAGE_MASK..........",
    tempPath = PATH + "\streetsegment.gdb\streetsegment"
    field = "OneWay"
    cursor = arcpy.UpdateCursor(tempPath)
    for row in cursor:
        val = row.getValue(field)
        if val == "FT":
            row.setValue("BLOCKAGE_MASK", 256)
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "TF":
            row.setValue("BLOCKAGE_MASK", 1)
            cursor.updateRow(row)
            change_count = change_count + 1
        else:
            row.setValue("BLOCKAGE_MASK", 0)
            cursor.updateRow(row)
            change_count = change_count + 1
    print "DONE PROCESS TIME:",
    new_time = (datetime.now() - start_time) - time1
    print new_time,
    print "(ROWS FOUND NULL - " + str(null_count) + ") (ROWS CHANGED - " + str(change_count) + ")"
    del cursor



def calculatePretype():
    time1 = (datetime.now() - start_time)
    null_count = 0
    change_count = 0
    print "CALCULATING PRETYPE2...............",
    tempPath = PATH + "\streetsegment.gdb\streetsegment"
    field = "Shield"
    cursor = arcpy.UpdateCursor(tempPath)
    for row in cursor:
        val = row.getValue(field)
        if val == "I" or val == "IC":
            row.setValue("PRETYPE2", "I")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "S" or val == "SC" or val == "SH":
            row.setValue("PRETYPE2", "SR")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "C" or val == "CT":
            row.setValue("PRETYPE2", "CR")
            cursor.updateRow(row)
            change_count = change_count + 1
        elif val == "U" or val == "UB" or val == "UC":
            row.setValue("PRETYPE2", "US")
            cursor.updateRow(row)
            change_count = change_count + 1
        else:
            null_count = null_count + 1
    print "DONE PROCESS TIME:",
    new_time = (datetime.now() - start_time) - time1
    print new_time,
    print "(ROWS FOUND NULL - "+str(null_count)+") (ROWS CHANGED - "+str(change_count)+")"


def calculateStreetname():
    # Calculate STREETNAME1
    time1 = (datetime.now() - start_time)
    change_count = 0
    null_count = 0
    print "CALCULATING STREETNAME1............",
    tempPath = PATH + "\streetsegment.gdb\streetsegment"
    field = "FCC"
    cursor = arcpy.UpdateCursor(tempPath)
    for row in cursor:
        val = row.getValue(field)
        if val == "A15":
            pre = row.getValue("PRETYPE2")
            high = row.getValue("HighwayNumber")
            nav = row.getValue("NAVIGATIONDIRECTION9")
            if nav != "None":
                name = str(pre) + " - " + str(high) + " " + str(nav)
            else:
                name = str(pre) + " - " + str(high)
            row.setValue("STREETNAME1", name)
            cursor.updateRow(row)
            change_count = change_count + 1
        else:
            null_count = null_count + 1
    print "DONE PROCESS TIME:",
    new_time = (datetime.now() - start_time) - time1
    print new_time,
    print "(ROWS FOUND NULL - " + str(null_count) + ") (ROWS CHANGED - " + str(change_count) + ")"

def createNYSTA():
    # Checks and sees if nysta.gdb exist, if it does it removes it and reinstalls it
    print("Creating streetsegment_NYSTA.gdb")
    if arcpy.Exists(PATH + "\streetsegment_NYSTA.gdb"):
        print("streetsegment_NYSTA already exist...reinstalling gdb")
        arcpy.Delete_management(PATH+"\streetsegment_NYSTA.gdb\streetsegment_NYSTA.shp")
        arcpy.Delete_management(PATH+"\streetsegment_NYSTA.gdb")
    arcpy.CreateFileGDB_management(PATH, "streetsegment_NYSTA.gdb")
    # Copies from streetsegment into nysta where the jurisdiction is 06 - Thruway and Berkshire Spur
    print("Copying from streetsegment to streetsegment_NYSTA")
    arcpy.FeatureClassToFeatureClass_conversion(PATH + "\streetsegment.gdb\streetsegment", PATH + "\streetsegment_NYSTA.gdb", "StreetSegment_NYSTA", "JURISDICTION LIKE '06%'")

if __name__ == '__main__':
    main()
