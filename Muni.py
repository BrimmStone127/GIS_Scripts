# -*- coding: utf-8 -*-

# Import arcpy module
import arcpy
from datetime import datetime
global start_time
global new_time
start_time = datetime.now()


def main():
    print "Creating Cities_Towns2"
    time1 = (datetime.now() - start_time)
    erase()
    new_time = (datetime.now() - start_time) - time1
    print new_time

    print "Creating Villages2"
    time1 = (datetime.now() - start_time)
    intersect()
    new_time = (datetime.now() - start_time) - time1
    print new_time

    print "Joining SWIS from 'SWIS_Muni_Codes' to Cities_Towns2"
    time1 = (datetime.now() - start_time)
    join()
    new_time = (datetime.now() - start_time) - time1
    print new_time

def erase():
    arcpy.env.workspace = "C:\Users\cbrimm\Desktop\TEST_gisdata\SWIS_Fill_Work.gdb"
    arcpy.Erase_analysis("Cities_Towns", "Villages", "Cities_Towns2")


def intersect():
    arcpy.env.workspace = "C:\Users\cbrimm\Desktop\TEST_gisdata\SWIS_Fill_Work.gdb"
    arcpy.Intersect_analysis(["Villages", "Cities_Towns"], "Villages2")


def join():
    arcpy.env.workspace = "C:\Users\cbrimm\Desktop\TEST_gisdata\SWIS_Fill_Work.gdb"
    inData = "Cities_Towns2"
    inField = "SWIS"
    joinTable = "SWIS_Muni_Codes"
    joinField = "CITYTOWN_SWIS"
    fields = ["SWIS"]
    arcpy.JoinField_management(inData, inField, joinTable, joinField, fields)

if __name__ == '__main__':
    main()