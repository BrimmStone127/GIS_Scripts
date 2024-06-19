import os
import zipfile
from datetime import datetime
global start_time
start_time = datetime.now()

count = 0

mypath="W:/gisdata/orthos/spcs_east/nysdop/2016/06in"
os.chdir(mypath)
list = []

search_list = os.listdir(mypath)

f = open("C:\Users\cbrimm\Desktop\list.txt",'r') # LIST OF FILES NEEDED FOR ZIPPING (STORED IN TXT)
while True:
    text = f.readline()
    if not text:
        break
    try:
        int(text[2:10])
        list.append(text)
    except ValueError:
        print "not a num"

string = search_list[0]
print string[2:10]

def binarySearch(alist, item):
    first = 0
    last = len(alist)-1
    found = False
    while first<=last and not found:
        midpoint = (first + last)//2
        midpoint_temp = alist[midpoint]
        midpoint_num = int(midpoint_temp[2:10])
        print "MIDPOINT_NUM=" + str(midpoint_num),
        print "ITEM=" + str(item),
        if midpoint_num == item:
            print "MATCH!!!!!!!!!!!!!!!"
            zout.write(search_list[midpoint])
            found = True
        else:
            if item < midpoint_num:
                print "MIDPOINT IS TOO HIGH"
                last = midpoint-1
            else:
                print "MIDPOINT IS TOO LOW"
                first = midpoint + 1
    return found

zout = zipfile.ZipFile('Zipped.zip', 'w', zipfile.ZIP_DEFLATED)
for item in list:
    item = int(item[2:10])
    binarySearch(search_list, item)

print "SCRIPT COMPLETE - TOTAL TIME: " + str((datetime.now() - start_time))