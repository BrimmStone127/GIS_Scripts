# -*- coding: utf-8 -*-

# Import arcpy module
import arcpy
import sys
from datetime import datetime
global start_time
global new_time
start_time = datetime.now()

# Local variables:
newTable = "ORTPS_Assessment"
Path = "C:\Users\cbrimm\Desktop\TEST_gisdata" # Edit this variable to the correct path (The folder that holds the raw RG_16.csv or equivalent)
newGDB = "\ORTPS_Assessment.gdb"
newGDBname = "ORTPS_Assessment.gdb"
tableName = "ORTPS_Assessment"
tablePath = "\ORTPS_Assessment"
primeTable = "\RG_16.csv"


def main():
    global input_var1
    global input_var2
    global input_var3
    global input_var4
    global input_var5
    global input_var6
    global input_var7
    global input_var8
    global input_var9
    newGDBname = "ORTPS_Assessment.gdb"
    newGDB = "\ORTPS_Assessment.gdb"
    input_var = raw_input("The current name for the new .gdb is " + newGDBname + ". Would you like to change this? (Y/N): ")
    input_var = input_var.upper()
    if input_var == "Y" or input_var == "YES":
        condition = True
        while condition == True:
            input_var = raw_input("Please enter the new name for the .gdb (Example: ORTPS_Assessment_2017): ")
            tableName = input_var
            tablePath = r"/" + tableName
            newGDBname = input_var + ".gdb"
            newGDB = r"/" + newGDBname
            print ("The new gdb, path, and table names are: " + newGDBname + ", " + newGDB + ", " + tableName)
            input_var =  raw_input("Are these values correct? (Y/N): ")
            input_var = input_var.upper()
            if input_var in ("N", "NO"):
                condition = True
            if input_var in ("Y", "YES"):
                condition = False
    elif input_var == "N" or input_var == "NO":
        print "Creating gdb..."
    else:
        "Input not recognized.."

    time1 = (datetime.now() - start_time)
    createGDB()
    new_time = (datetime.now() - start_time) - time1
    print new_time

    arcpy.env.workspace = Path + newGDB
    time1 = (datetime.now() - start_time)
    table2Table()
    new_time = (datetime.now() - start_time) - time1
    print new_time

    time1 = (datetime.now() - start_time)
    addFields()
    new_time = (datetime.now() - start_time) - time1
    print new_time

    step = True
    while step:
        input_var = raw_input("Are there any new fields that you would like to add? (Y/N): ")
        input_var = input_var.upper()
        if input_var == "Y" or input_var == "YES":
            input_var1 = raw_input("Enter the name of the field you would like to add: ")
            input_var2 = raw_input("Enter the field type: (TEXT, FLOAT, DOUBLE, SHORT, LONG, DATE, BLOB, RASTER, GUID): ")
            input_var2 = input_var2.upper()
            input_var3 = raw_input("Enter the field precision, OPTIONAL ENTER NOTHING FOR DEFAULT (LONG): ")
            input_var4 = raw_input("Enter the field scale, OPTIONAL ENTER NOTHING FOR DEFAULT (LONG): ")
            input_var5 = raw_input("Enter the field length, OPTIONAL ENTER NOTHING FOR DEFAULT (LONG): ")
            input_var6 = raw_input("Enter the field alias, OPTIONAL ENTER NOTHING FOR DEFAULT (STRING): ")
            input_var7 = raw_input("Enter if the field is nullable, OPTIONAL ENTER NON_NULLABLE or NULLABLE (Boolean): ")
            input_var7 = input_var7.upper()
            input_var8 = raw_input("Enter if the field is required, OPTIONAL ENTER NON_REQUIRED or REQUIRED (Boolean): ")
            input_var8 = input_var8.upper()
            input_var9 = raw_input("Enter the field domain, OPTIONAL ENTER NOTHING FOR DEFAULT (String): ")
            newField = "arcpy.AddField_management(" + newTable + " , " + input_var1 + ", " + input_var2 + ", " + input_var3 + ", " + input_var4 + ", " + input_var5 + ", " + input_var6 + ", " + input_var7 + ", " + input_var8 + ", " + input_var9 + ") "
            print "You have created this add field command: " + newField
            input_var = raw_input("Is this correct? (Y/N): ")
            if input_var == "Y" or input_var == "YES":
                step = False
            else:
                step = True
        if input_var == "N" or input_var == "NO":
            step = False

    time1 = (datetime.now() - start_time)
    calculateFields()
    new_time = (datetime.now() - start_time) - time1
    print new_time

    time1 = (datetime.now() - start_time)
    countyTables()
    new_time = (datetime.now() - start_time) - time1
    print new_time


def createGDB():
    if arcpy.Exists(Path + newGDB):
        print(newGDB + " already exist...reinstalling gdb")
        arcpy.Delete_management(Path + newGDB + tablePath)
        arcpy.Delete_management(Path + newGDB)
    print "creating "+ newGDBname
    arcpy.CreateFileGDB_management(Path, newGDBname)
    print("GDB Created..")


def table2Table():
    print "Transferring from " + primeTable + " to " + newGDB
    arcpy.env.workspace = Path
    arcpy.TableToTable_conversion(Path + primeTable, newGDB, tableName)


def addFields():
    print "Adding fields..."
    arcpy.env.workspace = Path + newGDB
    arcpy.AddField_management(newTable , "PARCEL_ADDR", "TEXT", "", "", "255", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(newTable , "LOC_STREET", "TEXT", "", "", "255", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(newTable , "LOC_UNIT", "TEXT", "", "", "25", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(newTable , "ADD_OWNER", "TEXT", "", "", "255", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(newTable , "MAIL_ADDR", "TEXT", "", "", "255", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(newTable , "ADD_MAIL_ADDR", "TEXT", "", "", "255", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(newTable , "CITYTOWN_NAME", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(newTable , "CITYTOWN_CODE", "TEXT", "", "", "25", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(newTable , "COUNTY_ITERATE", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")
    arcpy.AddField_management(newTable , "SBL", "TEXT", "", "", "50", "", "NULLABLE", "NON_REQUIRED", "")


def calculateFields():
    print "Calculating fields..."
    print "LOC_STREET"
    arcpy.CalculateField_management(newTable, "LOC_STREET", "[LOC_ST_PREFIX] & \" \" & [LOC_ST_NAME] & \" \" & [LOC_ST_SUFFIX] & \" \" & [LOC_POST_DIR]", "VB", "")
    arcpy.CalculateField_management(newTable, "LOC_STREET", "!LOC_STREET!.strip()", "PYTHON_9.3", "")
    arcpy.CalculateField_management(newTable, "LOC_STREET", "!LOC_STREET!.replace('   ', ' ')", "PYTHON_9.3", "")
    arcpy.CalculateField_management(newTable, "LOC_STREET", "!LOC_STREET!.replace('  ', ' ')", "PYTHON_9.3", "")
    print "LOC_UNIT"
    arcpy.CalculateField_management(newTable, "LOC_UNIT", "[LOC_UNIT_NAME] & \" \" & [LOC_UNIT_NBR]", "VB", "")
    arcpy.CalculateField_management(newTable, "LOC_UNIT", "!LOC_UNIT!.strip()", "PYTHON_9.3", "")
    arcpy.CalculateField_management(newTable, "LOC_UNIT", "!LOC_UNIT!.replace('  ', ' ')", "PYTHON_9.3", "")
    print "PARCEL_ADDR"
    arcpy.CalculateField_management(newTable, "PARCEL_ADDR", "[LOC_ST_NBR] & \" \" & [LOC_STREET] & \" \" & [LOC_UNIT]", "VB", "")
    arcpy.CalculateField_management(newTable, "PARCEL_ADDR", "!PARCEL_ADDR!.strip()", "PYTHON_9.3", "")
    arcpy.CalculateField_management(newTable, "PARCEL_ADDR", "!PARCEL_ADDR!.replace('  ', ' ')", "PYTHON_9.3", "")
    print "ADD_OWNER"
    arcpy.CalculateField_management(newTable, "ADD_OWNER", "[ADD_OWNER_FNAME] & \" \" & [ADD_OWNER_MI] & \" \" & [ADD_OWNER_LNAME] & \" \" & [ADD_OWNER_SUFFIX]", "VB", "")
    arcpy.CalculateField_management(newTable, "ADD_OWNER", "!ADD_OWNER!.strip()", "PYTHON_9.3", "")
    arcpy.CalculateField_management(newTable, "ADD_OWNER", "!ADD_OWNER!.replace('    ', ' ')", "PYTHON_9.3", "")
    arcpy.CalculateField_management(newTable, "ADD_OWNER", "!ADD_OWNER!.replace('    ', ' ')", "PYTHON_9.3", "")
    arcpy.CalculateField_management(newTable, "ADD_OWNER", "!ADD_OWNER!.replace('   ', ' ')", "PYTHON_9.3", "")
    arcpy.CalculateField_management(newTable, "ADD_OWNER", "!ADD_OWNER!.replace('  ', ' ')", "PYTHON_9.3", "")
    print "MAIL_ADDR"
    arcpy.CalculateField_management(newTable, "MAIL_ADDR", "[MAIL_ST_NBR] & \" \" & [MAIL_ST_PREFIX] & \" \" & [MAIL_ST_RTE] & \" \" & [MAIL_ST_SUFFIX] & \" \" & [POST_DIR] & \" \" & [OWNER_UNIT_NAME] & \" \" & [OWNER_UNIT_NBR]", "VB", "")
    arcpy.CalculateField_management(newTable, "MAIL_ADDR", "!MAIL_ADDR!.strip()", "PYTHON_9.3", "")
    arcpy.CalculateField_management(newTable, "MAIL_ADDR", "!MAIL_ADDR!.replace('      ', ' ')", "PYTHON_9.3", "")
    arcpy.CalculateField_management(newTable, "MAIL_ADDR", "!MAIL_ADDR!.replace('     ', ' ')", "PYTHON_9.3", "")
    arcpy.CalculateField_management(newTable, "MAIL_ADDR", "!MAIL_ADDR!.replace('    ', ' ')", "PYTHON_9.3", "")
    arcpy.CalculateField_management(newTable, "MAIL_ADDR", "!MAIL_ADDR!.replace('   ', ' ')", "PYTHON_9.3", "")
    arcpy.CalculateField_management(newTable, "MAIL_ADDR", "!MAIL_ADDR!.replace('  ', ' ')", "PYTHON_9.3", "")
    arcpy.CalculateField_management(newTable, "ADD_MAIL_ADDR", "[ADD_MAIL_ST_NBR] & \" \" & [ADD_ST_PREFIX] & \" \" & [ADD_MAIL_ST_RTE] & \" \" & [ADD_ST_SUFFIX]& \" \" & [ADD_POST_DIR]& \" \" & [ADD_OWNER_UNITNM] & \" \" & [ADD_OWNER_UNITNBR]", "VB", "")
    arcpy.CalculateField_management(newTable, "ADD_MAIL_ADDR", "!ADD_MAIL_ADDR!.strip()", "PYTHON_9.3", "")
    arcpy.CalculateField_management(newTable, "ADD_MAIL_ADDR", "!ADD_MAIL_ADDR!.replace('      ', ' ')", "PYTHON_9.3", "")
    arcpy.CalculateField_management(newTable, "ADD_MAIL_ADDR", "!ADD_MAIL_ADDR!.replace('     ', ' ')", "PYTHON_9.3", "")
    arcpy.CalculateField_management(newTable, "ADD_MAIL_ADDR", "!ADD_MAIL_ADDR!.replace('    ', ' ')", "PYTHON_9.3", "")
    arcpy.CalculateField_management(newTable, "ADD_MAIL_ADDR", "!ADD_MAIL_ADDR!.replace('   ', ' ')", "PYTHON_9.3", "")
    arcpy.CalculateField_management(newTable, "ADD_MAIL_ADDR", "!ADD_MAIL_ADDR!.replace('  ', ' ')", "PYTHON_9.3", "")
    print "CITYTOWN_NAME"
    arcpy.CalculateField_management(newTable, "CITYTOWN_NAME", "[MUNI_NAME]", "VB", "")
    print "CITYTOWN_CODE"
    arcpy.CalculateField_management(newTable, "CITYTOWN_CODE", "[MUNI_CODE]", "VB", "")
    print "COUNTY_ITERATE"
    arcpy.CalculateField_management(newTable, "COUNTY_ITERATE", "!COUNTY_NAME!.replace(' ','')", "PYTHON_9.3", "")
    print "SBL"
    arcpy.CalculateField_management(newTable, "SBL", "[SECTION]& [SUB_SEC]& [BLOCK]& [LOT]& [SUB_LOT]& [SUFFIX]", "VB", "")


def countyTables():
    print "Creating county tables..."
    arcpy.env.workspace = Path
    countyArray = ["Albany", "Allegany", "Broome", "Cattaraugus", "Cayuga", "Chautauqua", "Chemung", "Chenango", "Clinton", "Columbia", "Cortland", "Delaware", "Dutchess", "Erie", "Essex",
                   "Franklin", "Fulton", "Genesee", "Greene", "Hamilton", "Herkimer", "Jefferson", "Kings", "Lewis", "Livingston", "Madison", "Monroe", "Montgomery", "Nassau",
                   "Niagara", "Oneida", "Onondaga", "Ontario", "Orange", "Orleans", "Oswego", "Otsego", "Putnam", "Queens", "Rensselaer", "Richmond", "Rockland", "St Lawrence", "Saratoga",
                   "Schenectady", "Schoharie", "Schuyler", "Seneca", "Steuben", "Suffolk", "Sullivan", "Tioga", "Tompkins", "Ulster", "Warren", "Washington", "Wayne", "Westchester", "Wyoming",
                   "Yates"]
    for county in countyArray:
        print "Creating "+county+" table."
        if county == "St Lawrence":
            county1 = "StLawrence"
        else:
            county1 = county
        expression = arcpy.AddFieldDelimiters(arcpy.env.workspace, "COUNTY_NAME") + " = '" + county + "'"
        arcpy.TableToTable_conversion(Path + newGDB + tablePath, Path + newGDB, county1, expression)


if __name__ == '__main__':
    main()