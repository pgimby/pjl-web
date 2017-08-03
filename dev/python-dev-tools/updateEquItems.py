#!/usr/bin/python3

#import packages
import xml.etree.ElementTree as ET





xml_path = "../../data/labDB.xml"



def getNumber(s):

    for i in range(1,20):
        if "(" + str(i) + ")" in s:
            return str(i)
    return "1"





tree = ET.parse(xml_path)
root = tree.getroot()
for equip in root.findall(".//Equipment"): #XPath syntax for getting all descendants
    for item in equip.findall("Item"):
        num_children = len(item.getchildren())
        if num_children == 0:
            equipname = item.text
            num = getNumber(equipname)
            item.clear()
            item.attrib = {"id":"0000"}
            name = ET.SubElement(item, "Name")
            name.text = equipname
            number = ET.SubElement(item, "Number")
            number.text = num

tree.write("../../data/labDB.xml", encoding="unicode")
