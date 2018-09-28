#!/usr/bin/python3

'''This script is designed to add edit the equipment inventory. It can be used to add new equipment or to remove an existing piece of equipment'''

# Version 1.1 added image update function, manual update function
# Version 1.2 added ability to edit equipment information of existing items

#Future Version
#Add logging system to track changes

import pjlDB 
import os, argparse, unicodedata, re
import xml.etree.ElementTree as ET



#Fucntion that preform safety checks

def testHost(host):
	'''
	Test what computer this being run on. As of now it is machinne specific
	
	Args:
		host (str) name of host script was designed for
	
	Return:
		none
	'''
	thishost = os.uname()[1]
	if thishost not in host:
		print("This script is designed to be run on " + thishost + " only. Exiting...")
		exit()


def checkTimeStamp(dev,data):
	'''
	Checks that the source files for the databases referenced are the latest. This protects against overwritting changes by mistake

	Args:
		dev (str) location of a file
		data (str) location of a file

	Return:
		(bool) True if file at data is newer than the one at dev
	'''
	if os.path.getmtime(data) <= os.path.getmtime(dev):
		return True
	else:
		return False


# Function used for deleting equipment

'''Functions used for deleting equipiment items'''
def deleteEquipItem(eqdb,labdb):
	valid = False
	while not valid:
		itemID = input("Please enter the id number of the equipment item you wish to remove? ")
		if len(itemID) == 4 and itemID.isdigit() == True:
			try:
				item = eqdb.getItem(idnum=itemID)
				if input("Do you want to delete - " + item.name + "? (y/N) ") == "y":
					eqdb.deleteItem(labdb, itemID)
			except pjlDB.EQIDDoesNotExist as e:
				print(e)
			valid = True
		else:
			print("Invalid equipment id number entered. Needs to be a 4 digit number")
			return False


#Functions for collecting information for a new or existing equipment item

'''Gets an existing equipment item from xml'''
def getItemToEdit(eqdb):
	valid = False
	while not valid:
		eqID = input("Enter the id number of the equipment item you wish to edit. ")
		if len(eqID) == 4 and eqID.isdigit() == True:
			try: 
				eqItem = eqdb.getItem(idnum=eqID)
				valid = True
				return eqItem
			except pjlDB.EQIDDoesNotExist as e:
				print(e)
				if input("Would you like to try again? (y/N)") == "y":
					valid = False
				else:
					exit()
		else:
			print(eqID + " is not a valid equipment id number. Must be a four digit number.")

'''Collects information of kit status and/or contents'''
def getKit(oldItem):
	kit = []
	kitString = ""
	name = ""
	print(oldItem.kit)
	kitStatus = input("Is this item a kit? (y/N) [" + str(oldItem.is_kit) + "] ").lower()
	if kitStatus == "y":
		iskit = True
	elif kitStatus == "n":
		iskit = False
	else:
		iskit = oldItem.is_kit
	if iskit:
		name = input("Name of kit: [" + oldItem.name + "]")
		if name == "":
			name = oldItem.name
		if input("Would you like to edit the kit contents? y/N ").lower() == "y":
			lastItem = False
			kit = editKitList(oldItem)
			if not input("Would you like to add another item? Y/n ").lower() == "n":
				kit = addNewKitItem(kit)
			kitString = ", ".join(kit )
		else:
			kitString = oldItem.kit
	return iskit, name, kitString

def editKitList(oldItem):
	kit = []
	origKitList = oldItem.kit.split(",")
	for i in origKitList:
		name = i.split("(")[0].strip()
		try:
			amount = i.split("(")[1].strip()
			amount = str(amount.split(")")[0])
		except:
			amount = str(1)
		newName = input("Enter new name [" + name + "] , or enter \'delete\' to remove ")
		if newName == "delete":
			continue
		elif not newName == "":
			name = newName
		print(name)
		newAmount = input("Enter amount of " + name + "(s) [" + amount + "]: ")
		if newAmount.isdigit():
			amount = str(newAmount)
		if amount == "1":
			item = name
		else:
			item = name + " (" + amount +")"
		kit.append(item)
	return kit

def addNewKitItem(kit):
	lastItem = False
	while not lastItem:
		kitItemName = input("Kit Item : ")
		if kitItemName == "":
			print("Name is blank. Please try again, or enter \'pass\' to continue.")
			continue
		if kitItemName.lower() == "pass":
			lastItem = True
			continue
		kitItemAmount = input("How many " + kitItemName + "(s) are there? ")
		if kitItemAmount == "1":
			kit.append(kitItemName)
		elif kitItemAmount == "":
			kit.append(kitItemName)
		elif kitItemAmount.isdigit():
			kit.append(kitItemName + " (" + str(kitItemAmount) + ")")
		if input("Would you like to add another item? (Y/n) ").lower() == "n":
			lastItem = True
	return kit

	print("add extra item")

'''gets name of item'''
def getName(oldItem,greek):
	tempName = input("Name: [" + oldItem.name + "] ")
	if not tempName == "":
		newName = tempName
		Greek = re.findall(r"{([.\s\S]*?)}",newName)
		for i in Greek:
			if i.istitle():
				lookup = 'greek capital letter '
			else:
				lookup = 'greek small letter '
			new = unicodedata.lookup(lookup + i)
			old = ("{" + i + "}")
			newName = newName.replace(old,new)
	else:
		newName = oldItem.name
	return newName

'''gets quantities of item'''
def getQuantity(oldItem,kit):
	if kit:
		kitText = "kit"
	else:
		kitText = ""
	validAmount = False
	while not validAmount:
		tempTotal = input("Total Amount: [" + oldItem.quantity["total"] + "] ")
		if not tempTotal == "":
			newTotal = tempTotal
		else:
			newTotal = oldItem.quantity["total"]
			if newTotal == "":
				newTotal = str(0)
		tempService = input("Total in Service: [" + oldItem.quantity["service"] + "] ")
		if not tempService == "":
			newService = tempService
		else:
			newService = oldItem.quantity["service"]
			if newService == "":
				newService = str(0)
		tempRepair = input("Total under Repair: [" + oldItem.quantity["repair"] + "] ")
		if not tempRepair == "":
			newRepair = tempRepair
		else:
			newRepair = oldItem.quantity["repair"]
			if newRepair == "":
				newRepair = str(0)
		if int(newService) + int(newRepair) == int(newTotal):
			validAmount = True
		else:
			print("Totals do not add up. Please try again.")
		quantity = {}
		quantity["total"] = newTotal
		quantity["service"] = newService
		quantity["repair"] = newRepair
	return quantity

'''gets manufacturer of item'''
def getManufacturer(oldItem):
	tempMan = input("Manufacturer: [" + oldItem.manufacturer + "] ")
	if not tempMan == "":
		newMan = tempMan
	else:
		newMan = oldItem.manufacturer
	return newMan

'''gets model of item'''
def getModel(oldItem):
	tempModel = input("Model: [" + oldItem.model + "] ")
	if not tempModel == "":
		newModel = tempModel
	else:
		newModel = oldItem.model
	return newModel

'''gets location of item'''
def getLocations(oldItem,validRooms):
	print("To remove an existing location complete designate room as 'removed' ")
	newLocations = []
	for i in oldItem.locations:
		location = {}
		newRoom = validRoom(i["room"],validRooms)
		if newRoom:
			newStorage = validStorage(i["storage"])
			if not newRoom == "" and not newStorage == "":
				location["room"] = newRoom
				location["storage"] = newStorage
				newLocations.append(location)
	allLocations = False
	while not allLocations:
		if input("Is there another location (y/N) ") == "y":
			location = {}
			location["room"] = validRoom("",validRooms)
			location["storage"] = validStorage("")
			if not location["room"] == "" and not location["storage"] == "":
				newLocations.append(location)
			else:
				print("Location is invalid. Not adding location")
		else:
			allLocations = True
	return newLocations

'''validats room entry'''
def validRoom(oldRoom,validRooms):
	valid = False
	while not valid:
		tempRoom = input("Room: ["+ oldRoom +"] ")
		if tempRoom == "removed":
			return False
		if not tempRoom == "":
			if tempRoom in validRooms:
				newRoom = tempRoom
				valid = True
			else:
				print(tempRoom + " is not a valid room. Please try again.")
		else:
			newRoom = oldRoom
			valid = True
	return newRoom

'''gets storage room'''
def validStorage(oldStorage):
	tempStorage = input("Storage: [" + oldStorage + "] ")
	if not tempStorage == ""	:
		newStorage = tempStorage
	else:
		newStorage = oldStorage
	return newStorage	


'''Collects input from user on the new piece of equipment'''
def getEquipInfo(oldItem,validRooms,greek):
	info = {}
	infoIsKit,infoName,infoKit = getKit(oldItem)
	info["idnum"] = oldItem.id_num
	info["is_kit"] = infoIsKit
	info["name"] = infoName
	info["kit"] = infoKit
	if not infoIsKit:
		info["name"] = getName(oldItem,greek)
	infoQuantity = getQuantity(oldItem,infoIsKit)
	info["quantity"] = infoQuantity
	infoManufacturer = getManufacturer(oldItem)
	info["manufacturer"] = infoManufacturer
	infoModel = getModel(oldItem)	
	info["model"] = infoModel
	infoLocations = getLocations(oldItem,validRooms)
	info["locations"] = infoLocations
	return info

'''displays collected information for comfirmations'''
def checkEquipInfo(info):
	print("")
	print("---------------------------------------------------")
	print("")
	print("ID Number: " + info["idnum"])
	print("Name: " + info["name"])
	print("Is Kit: " + str(info["is_kit"]))
	if info["is_kit"]:
	 	print("Kit Contents:")
	 	print(info["kit"])
	print("Total amount: " + info["quantity"]["total"])
	print("Amount in service: " + info["quantity"]["service"])
	print("Amount under repair: " + info["quantity"]["repair"])
	print("Manufacturer: " + info["manufacturer"])
	print("Model: " + info["model"])
	locations = info["locations"]
	count = 0
	for i in locations:
		count = count + 1
		print("Location-" +str(count) + ": " + i["room"] + i["storage"])
	if input("Is the displayed information is correct. (y/N) ") == "y":
	 	return True
	else:
	 	return False


'''Modifies equimpnet object and adds them to new equipmentDB xml'''
def addEquip(item,info,eqdb):
	item.is_kit = info["is_kit"]
	if item.is_kit:
		item.kit = info["kit"]
	item.name = info["name"]
	item.quantity["total"] = info["quantity"]["total"]
	item.quantity["service"] = info["quantity"]["service"]
	item.quantity["repair"] = info["quantity"]["repair"]
	item.manufacturer = info["manufacturer"]
	item.model = info["model"]
	item.locations = info["locations"]
	eqdb.addItem(item)


#Functions for updating equipment images

def imgInfo(imageDir):
	images =  os.listdir(imageDir)
	imageInfo = []
	ids = []
	for i in images:
		ids.append(i[:4])
		image = {}
		image["id"] = (i[:4])
		image["name"] = i
		imageInfo.append(image)
	print(ids)
	return imageInfo,ids

def outInfo(name, equipRoot):
	eqID = str(name)[:4]
	webPath = equipRoot + "/" + name

	print("????????????????????????????")
	print(webPath)
	return eqID,webPath




#Functions for updating manuals

'''Generates list of ID numbers for all equipment with a manual'''
def equipWithMan(inputDir):
	listofID = []
	for root, dirs, files in os.walk(inputDir):
		for i in files:
			equipID = str(i)[:4]
			listofID.append(equipID)
	return list(set(listofID))

'''Gathers info on each of the manuals for indiviudal pieces of equipment'''
def manInfo(ID,inputDir,equipDir):
	manInfos = []
	for root, dirs, files in os.walk(inputDir):
		for i in files:
			if ID in i:
				dictName = {}
				docPath = "/".join([equipDir, i])
				dictName["location"] = str(docPath)
				ID = str(i)[:4]
				dictName["name"] = nameGenerator(ID,manInfos)
				manInfos.append(dictName)
	return manInfos, ID

'''Determines the number of manuals available for each item'''
def numOfManuals(ID,currentList):
	num = 1
	for i in currentList:
		if ID in i["location"]:
			num = num + 1
	return num

'''Generates names for manuals based on number of manuals available for each item'''
def nameGenerator(ID,currentLst):
	manualNum = numOfManuals(ID,currentLst)
	if manualNum == 1: 
		name = ID + "-manual.pdf"
	else:
		name = ID + "-manual" + str(manualNum) + ".pdf"
	return name


### Main Script

version = "1.3"


'''List of valid rooms and semesters '''
validRooms = ["ST009","ST017","ST020","ST025","ST029","ST030","ST032","ST034","ST036","ST037","ST038","ST039","ST042","ST046","ST048","ST050","ST068","ES002", "Chem Store", "SA 2nd Floor"]

'''dictionary of greek characters with matching unicode '''
greek = {"alpha": "\u03B1", "micro": "\u03BC"}

'''Define user options'''
parser = argparse.ArgumentParser()
parser.add_argument('-d', '--delete', help='Delete a piece of equipment from db.', action='store_true')
parser.add_argument('-e', '--edit', help='Edit details of a piece of equipment.', action='store_true')
parser.add_argument('-i', '--images', help='Add all images in ~/staffresources/equipment/equipimg to the equipment database.', action='store_true')
parser.add_argument('-m', '--manuals', help='Add all manuals in ~/staffresources/equipment/equipman to the equipment database.', action='store_true')
parser.add_argument('-n', '--new', help='Add new piece of equipment.".', action='store_true')
parser.add_argument('-t', '--test', help='Debug mode.', action='store_true')
parser.add_argument('-x', '--validate', help='Disable validation for xml.', action='store_true')
parser.add_argument('-v', '--version', help='Print current verion of script.', action='store_true')
args = parser.parse_args()
testMode = args.test
validate = args.validate

'''Paths for files'''
root = "/usr/local/master/pjl-web"
eqdbDev = root + "/dev/equipmentDB.xml"
labdbDev = root + "/dev/labDB.xml"
eqdbData = root + "/data/equipmentDB.xml"
labdbData = root + "/data/labDB.xml"
imageLocal = "/staffresources/equipment/equipimg"
imageDir = root + imageLocal
manualLocal = "/staffresources/equipment/equipman"
manualDir = root + manualLocal


'''Changes the output to a temporary file if script is run in test mode'''
if testMode:
	destXML = root + "/dev/test_equipmentDB.xml"
	print("----------Running in test mode.----------")	
else:
	destXML= eqdbDev

'''validation disabled warning'''
if validate:
	print("validation of output file has been disabled. Be Very Careful!")

'''name of host machine this scipt was written for'''
devHost=["slug","fry"]


'''Confirm that this script won't accidently run on the wrong machine'''
testHost(devHost)


'''Create pjlDB object of each of the relevent xml files'''
eqdb = pjlDB.EquipDB("/usr/local/master/pjl-web/dev/equipmentDB.xml")
labdb = pjlDB.LabDB("/usr/local/master/pjl-web/dev/labDB.xml")


'''prints version'''
if args.version:
	print("Version " + version)
	exit()


'''Checks that the development version of both key DBs are new or as new as the live versions.'''
if not checkTimeStamp(eqdbDev,eqdbData) or not checkTimeStamp(labdbDev,labdbData):
	if not checkTimeStamp(eqdbDev,eqdbData):
		print("Equipment development database is out of synce with the live version. Please update the development version before continuing.")
	if not checkTimeStamp(labdbDev,labdbData):
		print("Repository development database is out of synce with the live version. Please update the development version before continuing.")
	print("Exiting...")
	exit()


######################################################################################################

















'''calls functions for deleting equipment item'''
if args.delete:
	deleteEquipItem(eqdb,labdb)


'''calls functions for editing an existing equipment entry'''
if args.edit or args.new:
	if args.new:
		equipItem = eqdb.newItem(eqdb.new_id)
	if args.edit:
		equipItem = getItemToEdit(eqdb)
	confirmed = False
	while not confirmed:
		equipInfo = getEquipInfo(equipItem,validRooms,greek)
		if checkEquipInfo(equipInfo):
			confirmed = True
			addEquip(equipItem,equipInfo,eqdb)


'''calls functions for updateing images for equipment'''
if args.images:
	images,ids = imgInfo(imageDir)
	tree = eqdb.tree
	eqTreeRoot = tree.getroot()
	for item in eqTreeRoot:
		itemID = item.attrib["id"]
		equip = eqdb.getItem(idnum=itemID)
		if itemID in ids:
			for i in images:
				if i["id"] == itemID:
					name = i["name"]
			#equip.thumbnail = "/" + imageLocal + "/" + name
			equip.thumbnail = imageLocal + "/" + name
			print(equip.thumbnail)
		else:
			equip.thumbnail = "/img/img-placeholder.png"
			print(equip.thumbnail)
		eqdb.addItem(equip)

if args.manuals:
	print("adding manuals")
	listOfIDs = equipWithMan(manualDir)
	print(listOfIDs)
	for i in listOfIDs:
		equipManuals,eqID = manInfo(i,manualDir,"/" + manualLocal)
		equip = eqdb.getItem(idnum=eqID)
		equip.documents = equipManuals
		print(equip.documents)
		#eqdb.addItem(equip)
# db.save("../updatedequipmentDB.xml", ignore_validation=False, error_log=True)

'''saves new xml file'''
if args.test:
	print("writing to " + destXML)
	print(type(destXML))
	eqdb.save(destXML, ignore_validation=validate, error_log=True)
else:
	print("saving to " + destXML)
	eqdb.save(destXML, ignore_validation=validate, error_log=True)

'''confirms that the script has ended properly'''
print("...and then there will be cake")
