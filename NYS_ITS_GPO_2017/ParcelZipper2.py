import zipfile
import os
from datetime import datetime


def getCounty():
    directory = r'W:\GIS\Statewide_Parcel_Map_Program\SPM_Published\to_SharePoint_or_FTP\1706\Counties_Share' # Path to the location of the counties repository
    print directory
    os.chdir(directory) # Change the directory the script is working in
    counties = os.listdir(directory) # Create an array of all the county files
    for county in counties: # loop over all counties in the county array
        string = r"W:\GIS\Statewide_Parcel_Map_Program\SPM_Published\to_SharePoint_or_FTP\1706\Counties_Share" + "\\"
        string2 = string + county # Create the string that represents the path to a particular counties folder
        if string2 == r"W:\GIS\Statewide_Parcel_Map_Program\SPM_Published\to_SharePoint_or_FTP\1706\Counties_Share\_NO_SHARE": # ensure that the folder is an actual county
            break
        else:
            county_name = os.path.basename(os.path.normpath(string2)) # Cut the pathname down to just the name of the county
            os.chdir(string2)  # Change the directory the script is working in to the particular county folder
            zip_name1 = county_name + "_2016_Tax_Parcels_SHP_1706.zip" # string correctly forms the file name of the zip folder
            zip_name2 = county_name + "_2016_Tax_Parcels_GDB_1706.zip" # string correctly forms the file name of the zip folder
            county_files = os.listdir(string2) # create an array of the files in the county folder
            zout = zipfile.ZipFile(zip_name1, 'w', zipfile.ZIP_DEFLATED) # setup the zip process
            zout2= zipfile.ZipFile(zip_name2, 'w', zipfile.ZIP_DEFLATED)
            for cf in county_files: # loop over all the files in the array
                os.chdir(string2)
                zip_check = cf[-4:]
                if os.path.isdir(cf) or zip_check == ".zip": # makes sure that the program does not add any already zipped files to the new zip file
                    if os.path.isdir(cf):
                        gdb_check = cf[-4:]
                        if gdb_check == ".gdb":
                            for dirpath, dirs, files in os.walk(cf):
                                for f in files:
                                    fn = os.path.join(dirpath, f)
                                    zout2.write(fn)
                                    print "Added " + fn + " to " + zip_name2

                elif not os.path.isdir(cf):
                    zout.write(cf) # writes the file to the zipped folder
                    print "Added " + cf + " to " + zip_name1


def main():
    startTime = datetime.now()
    getCounty()
    print("Time to complete: " + str(datetime.now() - startTime))


if __name__ == "__main__":
    main()
