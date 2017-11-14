#!/usr/bin/python3

#import packages
import xml.etree.ElementTree as ET
from pjlDB import *



tree1 = ET.parse("../labDB.xml")
root1 = tree1.getroot()
tree2 = ET.parse("../equipmentDB.xml")
root2 = tree2.getroot()

db = equipDB(tree2)
db.validateFull()

'''
eqids = []
for item in root1.findall(".//Item"):
    eqids.append(item.attrib["id"])

eqids = list(set(eqids))
kits = []
with open("../wes-tmp.txt", "r") as f:
    for line in f.readlines():
        l = line.split("\t")
        eid = l[0]
        name = l[1]
        kit = l[2]
        kits.append([eid, name, kit])

for i in eqids:
    eid = i
    typ = "item"
    components = ""
    name = ""
    for kit in kits:
        if eid == kit[0]:
            typ = "kit"
            components = kit[2]
            name = kit[1]
    
    for lab in root1:
        for item in lab.findall(".//Item"):
            if item.attrib["id"] == str(eid):
                if name == "":
                    name = item.findtext("Name")


    itemnode = ET.SubElement(root2, "Item")
    itemnode.attrib = {"id": str(eid)}
    itemname = ET.SubElement(itemnode, "InventoryName")
    itemname.text = name
    ident = ET.SubElement(itemnode, "Identification")
    manu = ET.SubElement(ident, "Manufacturer")
    if "Pasco" in name:
        manu.text = "Pasco"
    if "Fluke" in name:
        manu.text = "Fluke"
    if "Korad" in name:
        manu.text = "Korad"
    if "HP" in name:
        manu.text = "HP"
    if "Philips" in name:
        manu.text = "Philips"
    if "Berkeley Nucleonics" in name:
        manu.text = "Berkeley Nucleonics"
    if "Phywe" in name:
        manu.text = "Phywe"
    if "B&K" in name:
        manu.text = "B&K"
    if "Neva" in name:
        manu.text = "Neva"
    if "Vernier" in name:
        manu.text = "Vernier"
    if "Jarrell Ash" in name:
        manu.text = "Jarrell Ash"
    if "Ortec" in name:
        manu.text = "Ortec"
    if "Protec" in name:
        manu.text = "Protec"
    if "Cenco" in name:
        manu.text = "Cenco"
    if "Osram" in name:
        manu.text = "Osram"
    if "Leeds and Northrop" in name:
        manu.text = "Leeds and Northrop"
    if "Tel-Atomic" in name:
        manu.text = "Tel-Atomic"
    if "Tel-X-ometer" in name:
        manu.text = "Tel-X-ometer"
    if "Firestone" in name:
        manu.text = "Firestone"
    if "Teachspin" in name:
        manu.text = "Teachspin"
    if "Cary" in name:
        manu.text = "Cary"
    if "Newport Instruments" in name:
        manu.text = "Newport Instruments"
    if "RCA" in name:
        manu.text = "RCA"
    if "Hammond" in name:
        manu.text = "Hammond"
    if "Rex" in name:
        manu.text = "Rex"
    if "Topward" in name:
        manu.text = "Topward"
    if "Tracerlab" in name:
        manu.text = "Tracerlab"
    if "Nucleus" in name:
        manu.text = "Nucleus"
    if "Mettler" in name:
        manu.text = "Mettler"
    if "GE" in name:
        manu.text = "GE"
    if "Kepco" in name:
        manu.text = "Kepco"
    if "Nalgene" in name:
        manu.text = "Nalgene"
    if "Nuclear Data" in name:
        manu.text = "Nuclear Data"
    model = ET.SubElement(ident, "Model")
    kitnode = ET.SubElement(itemnode, "Kit")
    if typ == "kit":
        kitnode.attrib = {"isKit": "true"}
    else:
        kitnode.attrib = {"isKit": "false"}
    kitnode.text = components
    loc = ET.SubElement(itemnode, "Locations")
    quant = ET.SubElement(itemnode, "Quantity")
    tot = ET.SubElement(quant, "Total")
    ins = ET.SubElement(quant, "InService")
    under = ET.SubElement(quant, "UnderRepair")
    docs = ET.SubElement(itemnode, "Documents")


print("number of items in inventory: ",len(root2))
names = []
ids = []
for item in root2.findall(".//Item"):
    names.append(item.findtext("InventoryName"))
    ids.append(item.attrib["id"])

print(len(set(names)), len(set(ids)))
import collections
print([item for item, count in collections.Counter(names).items() if count > 1])

        
tree2.write("../equipmentDB.xml")
'''
