#!/usr/bin/python3
#
# Script is a tool for finding information about initial status of inventory
#
# Written by Peter Gimby, Apr 10, 2018

import argparse, os
from xml.etree import ElementTree as ET
# import os, subprocess, argparse, filecmp, time

# '''define folder locations'''
root = "/usr/local/master/"
xml_file = root + "pjl-web/data/equipmentDB.xml"


def ifNone(entry):
    if entry == "":
        return ("None")
    else:
        return entry

def printLocations(locations):
    output = ""
    for i in locations:
        output = output + str(i["room"]) + "," + str(i["storage"]) + ","
    return output
    #return locations





'''Main Script'''

'''User input to allow for a test mode during development'''
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', help='test adding to xml without moving folders', action='store_true')
parser.add_argument('-a', '--all', help='display all categories', action='store_true')
parser.add_argument('-l', '--location', help='display location(s)', action='store_true')
parser.add_argument('-c', '--count', help='display amount in inventory', action='store_true')
parser.add_argument('-w', '--working', help='display amount in working condition', action='store_true')
parser.add_argument('-r', '--repair', help='display amount out of service', action='store_true')
args = parser.parse_args()
testMode = args.test



#outputwidth = 100

#open XML file
tree = ET.parse(xml_file)
root = tree.getroot()


count = 0
print ("id,Name,Total,In Service,Under Repair,Picture,Location")

for lab in root:
    idNum = lab.attrib["id"]
    name = lab.findtext("InventoryName")
    #print(name)
    for quantity in lab.findall(".//Quantity"):
        underRepair = str(ifNone(quantity.findtext("UnderRepair")))
        totalAmount = str(ifNone(quantity.findtext("Total")))
        inService = str(ifNone(quantity.findtext("InService")))
#        print(totalAmount)
        #print("Total " + totalAmount + " In Service " + inService + " Under Repair " + underRepair)
    locations = []
    for location in lab.findall(".//Location"):
        spot = {}
        spot["room"] = location.findtext("Room")
        spot["storage"] = location.findtext("Storage")
        locations.append(spot)

    for picture in lab.findall(".//Identification"):
        if picture.findtext("Thumbnail") == "/img/img-placeholder.png":
            hasPicture = "None"
        else:
            hasPicture = " "
    print (idNum + "," + name + "," + totalAmount + "," + inService + "," + underRepair + "," + hasPicture + "," + str(printLocations(locations)))
        #print(str(room) + " " + str(storage))

    #location = lab.findtext("UnderRepair")
    #print(location)
    #print(lab.Item)
    #for item in lab.findall(".//Item"):
    #    print("eh")
#        if item.attrib["id"] == i:

print("...and then there will be cake")
