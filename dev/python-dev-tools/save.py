#!/usr/bin/python3

#import packages
import xml.etree.ElementTree as ET
tree = ET.parse('../newlabDB.xml')
root = tree.getroot()
tmp = ET.tostring(root, encoding="unicode")
with open("tmp.xml", 'w') as f:
	f.write(tmp)
#tree.write('../newlabDB.xml', methode="xml", short_)