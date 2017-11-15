#!/usr/bin/python3

#import packages
import xml.etree.ElementTree as ET


root = ET.Element("Equipment")
tree = ET.ElementTree(root)

item = ET.SubElement(root, "Item", {"id": "0001"})
name = ET.SubElement(item, "InventoryName")
name.text = "Fluke multimeter"
identification = ET.SubElement(item, "Identification")
manufacturer = ET.SubElement(identification, "Manufacturer")
manufacturer.text = "Fluke"
model = ET.SubElement(identification, "Model")
model.text = "PM2535"
location = ET.SubElement(item, "Location")
room = ET.SubElement(location, "Room")
room.text = "ST037"
storage = ET.SubElement(location, "Storage")
storage.text = "C1"
amount = ET.SubElement(item, "Quantity")
total = ET.SubElement(amount, "Total")
total.text = "48"
inservice = ET.SubElement(amount, "InService")
inservice.text = "46"
underrepair = ET.SubElement(amount, "UnderRepair")
underrepair.text = "2"
documents = ET.SubElement(item, "Documents")
document = ET.SubElement(documents, "Document")
docname = ET.SubElement(document, "Name")
docname.text = "user manual"
location = ET.SubElement(document, "location")
online = ET.SubElement(location, "Online")
online.text = "/equipment/docs/0001/manual.pdf"
offline = ET.SubElement(location, "Offline")
offline.text = "ST050"

tree.write("../equipmentDB.xml", encoding="UTF-8")
