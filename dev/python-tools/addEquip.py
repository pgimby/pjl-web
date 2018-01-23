#!/usr/bin/python3

from pjlDB import *

db = EquipDB("/home/pgimby/pjl-web/dev/equipmentDB.xml")
newitem = db.newItem(db.new_id)


newitem.name = "8 inch front serface mirror"
newitem.manufacturer = "PJL"
newitem.model = ""
newitem.is_kit = True
newitem.locations = [{"room": "ST032", "storage": "C3"}]
newitem.quantity = {"total": "8", "service": "8","repair": "0"}
#newitem.kit = "steel rod (1), knife edge support (1), knife edge (1), knife edge (1), small cylindrical plastic mass (1), small cylindrical metal mass (1)"
#newitem.documents = [{"name": "warrantee", "location": "/path/to/document.pdf"}]

print(db.new_id)
db.addItem(newitem)
db.save("/home/pgimby/pjl-web/dev/updatedEquipmentDB.xml", ignore_validation=False, error_log=True)