Muni Script
Author: Clayton Brimm
8/9/17
FOR ARCPY REFERENCE: http://pro.arcgis.com/en/pro-app/arcpy/main/arcgis-pro-arcpy-reference.htm 


OVERVIEW

This script automates the creation of new shapefiles and corrects the SWIS code of some villages and cities. This script runs mainly off of 


SETUP

To run this script right click on the python file and select EDIT WITH IDLE or use your preferred python IDE (Interactive Development Environment). Once the IDE loads edit 
the Path variable to reflect the pathway needed to access the setup files. Once the variable is edited you should be able to run the module/file from the 
IDE. 


METHOD BREAKDOWN

main()
This method is the main control of the script. There are a number of while statements and user input sections here that help define what methods are called and when. This 
method is used to execute other methods and then print out diagnostics of these methods. 

erase()
This method works exactly like the arcmap equivalent. It removes the village spatial data from the cities shapefile and creates a new shapefile.

intersect()
This method works exactly like the arcmap equivalent. It separates any village shape that is part of two or more city/town boundaries. 

join()
This method takes the SWIS Code from the muni table and correctly applies them to the city shapefile
