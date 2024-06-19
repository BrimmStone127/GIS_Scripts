ParcelZipper2 Script
Author: Clayton Brimm
8/9/17
FOR ARCPY REFERENCE: http://pro.arcgis.com/en/pro-app/arcpy/main/arcgis-pro-arcpy-reference.htm 


OVERVIEW

This script automates the creation of a zipped file containing county data. 


SETUP

To run this script right click on the python file and select EDIT WITH IDLE or use your preferred python IDE (Interactive Development Environment). Once the IDE loads edit 
the Path variable to reflect the pathway needed to access the setup files. Once the variable is edited you should be able to run the module/file from the 
IDE. 


METHOD BREAKDOWN

main()
This method is the main control of the script. There are a number of while statements and user input sections here that help define what methods are called and when. This 
method is used to execute other methods and then print out diagnostics of these methods. 


getCounty()
Loops over each county folder and takes out each file that is not a .zip or a .gdb and puts it in its own new folder that is compressed. It does the same with each .gdb file. 
