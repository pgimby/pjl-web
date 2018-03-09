#!/usr/bin/python3

from pjlDB import *
import csv
import argparse

db = EquipDB("/usr/local/master/pjl-web/data/equipmentDB.xml")

parser = argparse.ArgumentParser()
parser.add_argument('source', help='enter path of lab folder(s) to add.  Ex addNewLab /path/to/folder1 ~/path/to/folder2')
args = parser.parse_args()
equFile = args.source

def parseEquInfo(equipInfo,catagory):
	lst = []
	for i in equipInfo:
		infoParts = i.split(";")
		if infoParts[0].split()[0] == catagory:
			for j in range(1,len(infoParts)):
				lst.append(" ".join(infoParts[j].split()))
	return lst



with open(equFile, "r") as o:
	equipItems = csv.reader(o)
	for i in equipItems:
		newitem = db.newItem(db.new_id)
		newitem.name = parseEquInfo(i,"name")[0]
		print(newitem.id_num)
		if "is_kit; True" in ",".join(map(str,i)):
			newitem.is_kit = True
			kit = parseEquInfo(i,"kit")
			newitem.kit = ", ".join(map(str, kit))
			print(newitem.kit)
		db.addItem(newitem)

		#namei[0])


#newitem = db.newItem(db.new_id)


#newitem.name = "8 inch front serface mirror"
#newitem.manufacturer = "PJL"
#newitem.model = ""
#newitem.is_kit = True
#newitem.locations = [{"room": "ST032", "storage": "C3"}]
#newitem.quantity = {"total": "8", "service": "8","repair": "0"}
#newitem.kit = "steel rod (1), knife edge support (1), knife edge (1), knife edge (1), small cylindrical plastic mass (1), small cylindrical metal mass (1)"
#newitem.documents = [{"name": "warrantee", "location": "/path/to/document.pdf"}]

#print(db.new_id)
#db.addItem(newitem)



db.save("/home/pgimby/pjl-web/dev/equipmentDB.xml", ignore_validation=False, error_log=True)