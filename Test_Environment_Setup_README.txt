Muni Script
Author: Clayton Brimm
8/18/17
FOR ARCPY REFERENCE: http://pro.arcgis.com/en/pro-app/arcpy/main/arcgis-pro-arcpy-reference.html


OVERVIEW

This small script creates an easier to use testing environment for shapefiles that are large and difficult to test scripts on. To use it you must run the check field
function using the name of the fields you want to check. The script will then test those fields and see how long it will take to find a row that is not null. This will make
sure that every field will have at least one row that is not null.