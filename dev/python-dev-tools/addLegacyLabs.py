#!/usr/bin/python3

#import packages
import xml.etree.ElementTree as ET


inputxml = "../labDB.xml"
outputxml = "../deletemeDB.xml"



#..........FUNCTIONS.............
def data(filename):
    newlabs = []
    labinfo = {}
    with open(filename, "r") as f:
        f.readline()
        for line in f.readlines():
            labinfo = {}
            row = line.split("\t")
            labinfo["labid"] = row[0]
            labinfo["labname"] = row[1]
            equip = ",".join(list(filter(filterFunction, row[2].split(","))))
            labinfo["equipment"] = equip
            newlabs.append(labinfo)
    return newlabs


def filterFunction(item):
    if item and item != "\n":
        return True


def getNumber(s):
    for i in range(1,20):
        if "(" + str(i) + ")" in s:
            return str(i)
    return "1"






    

tree = ET.parse("../labDB.xml")
root = tree.getroot()



newlabs = data("labs-to-add.dat")


for datum in newlabs:
    lab = ET.Element("Lab", {"labId": datum["labid"]})
    name = ET.SubElement(lab, "Name")
    name.text = datum["labname"]
    disciplines = ET.SubElement(lab, "Disciplines")
    topics = ET.SubElement(lab, "Topics")
    versions = ET.SubElement(lab, "Versions")
    equipment = ET.SubElement(lab, "Equipment")
    for item in datum["equipment"].split(","):
        eqitem = ET.SubElement(equipment, "Item", {"id" : "0000"})
        eqname = ET.SubElement(eqitem, "Name")
        eqname.text = item
        eqnum = ET.SubElement(eqitem, "Number")
        if "(2)" in item:
            eqnum.text = "2"
        elif "(3)" in item:
            eqnum.text = "3"
        elif "(4)" in item:
            eqnum.text = "4"
        elif "(5)" in item:
            eqnum.text = "5"
        elif "(6)" in item:
            eqnum.text = "6"
        elif "(7)" in item:
            eqnum.text = "7"
        else:
            eqnum.text = "1"

    typ = ET.SubElement(lab, "Type")
    typ.text = "Lab"
    docs = ET.SubElement(lab, "SupportDocs")
    software = ET.SubElement(lab, "Software")
    root.append(lab)


tree.write(outputxml, encoding="unicode")
