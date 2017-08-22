#! /usr/bin/python3
import xml.etree.ElementTree as ET
import pjlDB as p

tree = ET.parse("../labDB.xml")
db = p.labDB(tree)

#newlab = db.newLab(db.new_id)

newlab = db.newLab(db.new_id)
newlab.name = "Nuclear Pulse Height Analysis"
newlab.lab_tyoe = "Lab"

versions = [{"path": "/data/repository/0181-Nuclear-Pulse-Height-Analysis/0181-LEGACY", "semester": "", "year": "", "course": ""}]

newlab.versions = versions

equipment = [{"id": "0010", "name": "Oscilloscope", "amount": "1"},
             {"id": "0000", "name": "Nucleus Series 2/286 computer analyer", "amount": "1"},
             {"id": "0000", "name": "Berkeley nucleaon cs GL-3 pulse generator", "amount": "1"}]
newlab.equipment = equipment
db.addLab(newlab)
db.save("../../dev/updated_lab_database.xml", ignore_validation=True)
#lab.name = "Test Lab"
#lab.equipment = [{"id": "0055", "name": "thingamajig", "amount": "2"}]

#db.addLab(lab)
db.validateFull()