#! /usr/bin/python3
import xml.etree.ElementTree as ET
import pjlDB as p

tree = ET.parse("../labDB.xml")
db = p.labDB(tree)

#newlab = db.newLab(db.new_id)

newlab = db.newLab("0180")
newlab.name = "Axial and non Axial Magnetic Fields of a Helmholtz Coil"
newlab.lab_tyoe = "Lab"

versions = [{"path": "/data/repository/No-Year/0180-Axial-and-non-Axial-Magnetic-Fields-of-a-Helmholtz-Coil/0180-LEGACY/Axial-Magnetic-Flux-Density-of-a-Helmholtz-Coil.pdf", "semester": "", "year": "", "course": ""}]

newlab.versions = versions

equipment = [{"id": "0000", "name": "Fluke multimeter", "amount": "3"},
             {"id": "0000", "name": "Anatek power supply", "amount": "1"},
             {"id": "0000", "name": "mounted helmholtz coil-pair", "amount": "1"},
             {"id": "0000", "name": "female BNC to male banana adapter", "amount": "1"},
             {"id": "0000", "name": "high current power supply", "amount": "1"},
             {"id": "0000", "name": "lab jack", "amount": "1"},
             {"id": "0000", "name": "fork clamp", "amount": "1"},
             {"id": "0000", "name": "lab stand", "amount": "1"},
             {"id": "0000", "name": "right angle clamp", "amount": "1"},
			 {"id": "0000", "name": "cross-bar switch", "amount": "1"},
 	  		 {"id": "0000", "name": "plastic ruler", "amount": "6"},
			 {"id": "0000", "name": "set of connecting leads", "amount": "1"},
     		 {"id": "0000", "name": "3 ft coax cable", "amount": "1"},
			 {"id": "0000", "name": "standard magnet", "amount": "1"},
			 {"id": "0000", "name": "calipers", "amount": "1"},
			 {"id": "0000", "name": "micrometer", "amount": "1"},
			 {"id": "0000", "name": "wire gauge chart", "amount": "1"},
			 {"id": "0000", "name": "tape measure", "amount": "1"},
			 {"id": "0000", "name": "masking tape", "amount": "1"},
			 {"id": "0000", "name": "metric graph paper", "amount": "1"}]
newlab.equipment = equipment
db.addLab(newlab)
db.save("../../dev/updated_lab_database.xml", ignore_validation=True)
#lab.name = "Test Lab"
#lab.equipment = [{"id": "0055", "name": "thingamajig", "amount": "2"}]

#db.addLab(lab)
db.validateFull()