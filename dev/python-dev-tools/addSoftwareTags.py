#!/usr/bin/python3

#import packages
import xml.etree.ElementTree as ET





tree = ET.parse("../labDB.xml")
root = tree.getroot()

for child in root:
    newtag = ET.SubElement(child, "Software")


tree.write("../labDB-tmp.xml", encoding="unicode")
