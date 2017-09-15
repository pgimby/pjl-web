#! /usr/bin/python3
import xml.etree.ElementTree as ET
import pjlDB as p

tree = ET.parse("../labDB.xml")
db = p.labDB(tree)

#newlab = db.newLab(db.new_id)
newlab = db.newLab("0182")
newlab.name = "Modelling Motion"
newlab.lab_type = "Lab"

versions = [{"path": "/data/repository/0182-Modelling-Motion/0182-PHYS227FA2016/227_2016_Lab03_Modelling_Motion.pdf", "semester": "Fall", "year": "2016", "course": "PHYS 227", "directory": "/data/repository/0182-Modelling-Motion"}]
newlab.versions = versions

equipment = [{"id": "0024", "name": "computer", "amount": "1"}]
newlab.equipment = equipment

software = ["browser","VPython"]
newlab.software = software

db.addLab(newlab)
db.save("../../dev/updated_lab_database.xml", ignore_validation=True)

#lab.name = "Test Lab"
#lab.equipment = [{"id": "0055", "name": "thingamajig", "amount": "2"}]

#db.addLab(lab)
db.validateFull()
