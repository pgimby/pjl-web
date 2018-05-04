#!/usr/bin/python3

'''This script is designed to add new equipment to the equipment DB. It can be run in two ways'''

from pjlDB import *
import csv, os, argparse

eqdbLive = "/usr/local/master/pjl-web/dev/equipmentDB.xml"
labdbLive = "/usr/local/master/pjl-web/dev/labDB.xml"
eqSource = "/usr/local/master/pjl-web/data/equipmentDB.xml"
labdbSource = "/usr/local/master/pjl-web/data/labDB.xml"

eqdb = EquipDB("/usr/local/master/pjl-web/dev/equipmentDB.xml")
labdb = LabDB("/usr/local/master/pjl-web/dev/labDB.xml")



parser = argparse.ArgumentParser()
#parser.add_argument('-i', '--input', help='enter path of csv file to import information about the new equipment. Ex ./equipmentEdit -i newEquipment.csv')
parser.add_argument('-a', '--add', help='Used this option to add a single piece of equipment with name only. Ex "name of new equipment".', action='store_true')
parser.add_argument('-d', '--delete', help='enter id number of the piece of equipment to delete. Ex 0001')
parser.add_argument('-t', '--test', help='debug mode', action='store_true')

args = parser.parse_args()
testMode = args.test
#equFile = args.input
#deleteNum = parser.delete

'''Checks that the development version of the db is as new or newer that the live one'''

def checkTimeStamp(live,dev):
	if os.path.getctime(live) <= os.path.getctime(dev):
		return True
	else:
		return False


# Functions used for deleting equipiment items
def deleteEquipItem(idnum,eqdb,labdb):
	if len(idnum) == 4 and idnum.isdigit() == True:
		eqdb.deleteItem(labdb, idnum)
		if testMode: 
			print("checkValidID True")
		return True
	else:
		print("Invalid equipment id number entered. Needs to be a 4 digit number")
		if testMode:
			print("checkValidID False")
		return False
# Functions for adding new equipment

class EquipmentItem():


	def __init__(self):
		self.equipItem = self.getIdNum()
		print(self.equipItem.id_num)
		print(self.equipItem.name)
		
	def getIdNum(self):
		validID = False
		while not validID:
			self.idnum = input("Enter id number of equipment to edit. For new item hit ENTER ")
			if len(self.idnum) == 4 and self.idnum.isdigit() == True:
				equipItem = eqdb.getItem(self.idnum)
				if equipItem.name:
					validID = True
				except:
					print("not a valid equipment id number")
			elif not self.idnum:
				equipItem = eqdb.newItem(eqdb.new_id)
				validID = True
			else:
				if not input("Invalid equipment id number. Would you like to try again? y/N ") == "y":
					exit()
		return equipItem




		# print(args.add)
		# print(type(eqdb))
		# self.infoOK = False
		# self.lastItem = False
		# self.allLocations = False




# 	while infoOK == False:
# 		info = {}
# 		print("Please enter information about new equipment")
# 		if input("Is this item a kit? y/N ") == "y":
# 			kitText = " of kits"
# 			info["is_kit"] = True
# 			info["name"] = input("Name of kit: ")

# 			kit = []
# 			while lastItem == False:
# 				lastItem = True
# 				kitItemName = input("Kit Item : ")
# 				kitItemAmount = input("How many " + kitItemName + "(s) are there? ")
# 				if not kitItemAmount == "1":
# 					kit.append(kitItemName + "(" + kitItemAmount + ")")
# 				else:
# 					kit.append(kitItemName)
# 				if input("Is this the last item in the kit? Y/n ") == "n":
# 					lastItem = False
# 			info["kit"] = kit
# 		else:
# 			kitText = ""
# 			info["is_kit"] = False
# 			info["name"] = input("Name: ")
# 		quantity = {}
# 		quantity["total"] = input("Total amount" + kitText + ": " )
# 		quantity["service"] = input("Amount in service: ")
# 		quantity["repair"]	= input("Amount under repair: ")
# 		info["quantity"] = quantity
# 		info["manufacturer"] = input("Manufacturer: ")
# 		info["model"] = input("Model: ")
# 		print("Please add some information about the storage location of this equipment")
# 		locations = []
	
# 		while allLocations == False:
# 			allLocations = True
# 			location = {}
# 			location["room"] = input("Room: ")
# 			location["storage"] = input("Storage Container: ")
# 			locations.append(location)
# 			if input("Is there another location y/N ") == "y":
# 				allLocations = False
# 		info["locations"] = locations
# 		print(locations)
# 		confirmed = checkInfo(info)
# 		if confirmed:
# 			infoOK = True
# 		else:
# 			if input("Would you like to try again. y/N ") == "y":
# 				infoOK = False
# 			else:
# 				exit()
# 	return info

# def checkInfo(info):
# 	print("Name: " + info["name"])
# 	if info["is_kit"] == "True":
# 		print("Kit Contents: " + info["kit"])
# 	print("Total amount: " + info["quantity"]["total"])
# 	print("Amount in service: " + info["quantity"]["service"])
# 	print("Amount under repair: " + info["quantity"]["repair"])
# 	print("Manufacturer: " + info["manufacturer"])
# 	print("A")
# 	print("Model: " + info["model"])
# 	loc = info["locations"]
# 	for i in range(0,len(loc)):
# 		print(loc[i-1])
# 		print(i)
# 	if input("Is the displayed information is correct. y/N ") == "y":
# 		return True
# 	else:
# 		return False

# def addEquip(info,eqdb):
# 	print("adding new equipment item")
# 	newitem = eqdb.newItem(eqdb.new_id)
# 	newitem.name = info["name"]
# 	newitem.quantity["total"] = info["quantity"]["total"]
# 	newitem.quantity["service"] = info["quantity"]["service"]
# 	newitem.quantity["repair"] = info["quantity"]["repair"]
# 	newitem.manufacturer = info["manufacturer"]
# 	newitem.model = info["model"]
# 	newitem.locations = info["locations"]
# 	eqdb.addItem(newitem)

# Main Script


'''Checks that the development version of both key DBs are new or as new as the live versions.'''
if not checkTimeStamp(eqSource,eqdbLive) or not checkTimeStamp(labdbSource,labdbLive):
	if not checkTimeStamp(eqSource,eqdbLive):
		print("Equipment development database is out of synce with the live version. Please update the development version before continuing.")
	if not checkTimeStamp(labdbSource,labdbLive):
		print("Repository development database is out of synce with the live version. Please update the development version before continuing.")
	print("Exiting...")
	exit()

if not args.delete == None:
	deleteEquipItem(args.delete,eqdb,labdb)

if not args.add == None:
	equipInfo = EquipmentItem()
	#addEquip(equipInfo,eqdb)


eqdb.save("/home/pgimby/pjl-web/dev/tmp.xml", ignore_validation=False, error_log=True)
#db.save("/home/pgimby/pjl-web/dev/equipmentDB.xml", ignore_validation=False, error_log=True)

print("...and then there will be cake")