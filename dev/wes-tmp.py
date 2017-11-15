#!/usr/bin/python3

#import packages
import xml.etree.ElementTree as ET


tree = ET.parse("labDB.xml")
root = tree.getroot()

for v in root.findall(".//Version"):
    dirnode = v.find("Directory")
    pathnode = v.find("Path")
    path = pathnode.text.split("/")[:-1]
    if dirnode.text != "/".join(path):
        print(dirnode.text, "/".join(path))
        dirnode.text = "/".join(path)



tree.write("labDB.xml")
