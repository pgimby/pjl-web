#!/usr/bin/python3

#import packages
import argparse
import os
from xml.etree import ElementTree as ET

#params
xml_file = "../labDB.xml"
outputwidth = 100



#command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("idnum")
args = parser.parse_args()
i = args.idnum


#open XML file
tree = ET.parse(xml_file)
root = tree.getroot()

count = 0
for lab in root:
    for item in lab.findall(".//Item"):
        if item.attrib["id"] == i:
            s = str("Lab: " + lab.findtext("Name") + " (" + lab.attrib["labId"] + ")").ljust(60)
            s += str("Item: " + item.findtext("Name") + " (" + item.attrib["id"] + ")").ljust(40)
            count += 1
            print(s)


print("\nFound " + str(count) + " equipment records in " + str(os.path.abspath(xml_file)) + "\n\n")
