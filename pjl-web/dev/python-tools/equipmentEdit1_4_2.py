#!/usr/bin/python3

'''This script is designed to add edit the equipment inventory. It can be used to add new equipment or to remove an existing piece of equipment'''

# Version 1.1 added image update function, manual update function
# Version 1.2 added ability to edit equipment information of existing items

#Future Version
#Add logging system to track changes

import pjlDB 
import os, argparse, unicodedata, re
import colorama
from colorama import Fore, Style
from pprint import pprint
import xml.etree.ElementTree as ET


version = "1.4.2"

'''List of valid rooms and semesters '''
validRooms = ["ST009","ST017","ST020","ST025","ST029","ST030","ST032","ST034","ST036","ST037","ST038","ST039","ST042","ST046","ST048","ST050","ST068","ES002", "SB08", "SB03", "Chem Store", "SA 2nd Floor", "unknown"]


'''Functions for general appearance'''

def printG(txt):
	'''For debug messages. [Debug - FUNCTION] MESSAGE'''
	print(Fore.GREEN + txt + Style.RESET_ALL)

def printR(txt):
	'''For Errors. [Error] MESSAGE'''
	print(Fore.RED + txt + Style.RESET_ALL)

def printB(txt):
	'''For Information Messages'''
	print(Fore.BLUE + txt + Style.RESET_ALL)

def printY(txt):
	'''For messages/questions that request user input. Does not accept input'''
	print(Fore.YELLOW + txt + Style.RESET_ALL)

def printC(txt):
	'''For printing information requiring review'''
	print(Fore.CYAN + txt + Style.RESET_ALL)

def inputY(txt):
	'''For messages that input data from user. Requires input.'''
	return input(Fore.YELLOW + txt + Style.RESET_ALL)


'''Fucntion that preform safety checks'''

def testHost(host):
	'''
	Test what computer this being run on. As of now it is machine specific
	
	Args:
		host (str) name of host script was designed for
	
	Return:
		none
	'''
	thishost = os.uname()[1]
	if thishost not in host:
		printR("This script is not designed to be run on " + str(thishost) + ". Exiting...")
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
				printR(str(e))
			valid = True
		else:
			printR("Invalid equipment id number entered. Needs to be a 4 digit number")
			return False




'''Functions for collecting information for a new or existing equipment item'''

'''Gets an existing equipment item from xml'''
def getItemToEdit(eqdb):
	valid = False
	while not valid:
		eqID = inputY("Enter the id number of the equipment item you wish to edit. ")
		if len(eqID) == 4 and eqID.isdigit() == True:
			try: 
				eqItem = eqdb.getItem(idnum=eqID)
				valid = True
				return eqItem
			except pjlDB.EQIDDoesNotExist as e:
				printR(str(e))
				if input("Would you like to try again? (y/N)") == "y":
					valid = False
				else:
					exit()
		else:
			printR(str(eqID) + " is not a valid equipment id number. Must be a four digit number.")


'''Collects information of kit status and contents'''
def getKit(oldItem):
	kit = []
	kitString = ""
	name = ""
	kitStatus = inputY("Is this item a kit? (y/n) [" + str(oldItem.is_kit) + "] ").lower()
	if kitStatus == "y":
		iskit = True
	elif kitStatus == "n":
		iskit = False
	else:
		iskit = oldItem.is_kit
	
	if iskit:
		name = inputY("Name of kit: [" + str(oldItem.name) + "] ")
		try:
			name = specialChar(name)
		except Exception as e:
			raise e
		if name == "":
			name = oldItem.name
		if inputY("Would you like to edit the kit contents? y/N ").lower() == "y":
			lastItem = False
			kit = editKitList(oldItem)
			if not inputY("Would you like to add another item? Y/n ").lower() == "n":
				kit = addNewKitItem(kit)
			kitString = ", ".join(kit )
		else:
			kitString = oldItem.kit
	return iskit, name, kitString


'''Edits an existing kit'''
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

		newName = specialChar(inputY("Enter new name [" + str(name) + "] , or enter \'delete\' to remove "))

		if newName == "delete":
			continue
		elif not newName == "":
			name = newName
			#name = specialChar(newName)
		printB(name)
		newAmount = inputY("Enter amount of " + str(name) + "(s) [" + str(amount) + "]: ")
		if newAmount.isdigit():
			amount = str(newAmount)
		if amount == "1":
			item = name
		else:
			item = name + " (" + amount +")"
		kit.append(item)
	return kit


'''Adds contents of new kit'''
def addNewKitItem(kit):
	lastItem = False
	while not lastItem:
		kitItemName = specialChar(inputY("Kit Item : "))
		if kitItemName == "":
			printY("Name is blank. Please try again, or enter \'pass\' to continue.")
			continue
		if kitItemName.lower() == "pass":
			lastItem = True
			continue
		kitItemAmount = inputY("How many " + str(kitItemName) + "(s) are there? ")
		if kitItemAmount == "1":
			kit.append(kitItemName)
		elif kitItemAmount == "":
			kit.append(kitItemName)
		elif kitItemAmount.isdigit():
			kit.append(kitItemName + " (" + str(kitItemAmount) + ")")
		if inputY("Would you like to add another item? (Y/n) ").lower() == "n":
			lastItem = True
	return kit

	print("add extra item")


'''gets name of item'''
def getName(oldItem):
	printG("[Debug - getName] entering")
	name = specialChar(inputY("Name: [" + str(oldItem.name) + "] "))
	return name


'''replaces special characters with unicode'''
def specialChar(name):
	printG("[Debug - specialChar] entering")
	Greek = re.findall(r"{([.\s\S]*?)}",name)
	for i in Greek:
		printG("[Debug - specialChar] fixing " + i)
		if i.istitle():
			lookup = 'greek capital letter '
		else:
			lookup = 'greek small letter '
		try:
			new = unicodedata.lookup(lookup + i)
			old = ("{" + i + "}")
			name = name.replace(old,new)
		except Exception as e:
			printR("{ } brackets are reserved for inputing special characters i.e. greek letters.")
			printR('\"' + i + '\"' + " does not appear to be a defined special character and will be left as is.")
			#raise e
	printG("[Debug - specialChar] leaving and returning " + str(name))
	return name


'''gets quantities of item'''
def getQuantity(oldItem,kit):
	if kit:
		kitText = "kit"
	else:
		kitText = ""
	validAmount = False
	while not validAmount:
		tempTotal = inputY("Total Amount: [" + str(oldItem.quantity["total"]) + "] ")
		if not tempTotal == "":
			newTotal = tempTotal
		else:
			newTotal = oldItem.quantity["total"]
			if newTotal == "":
				newTotal = str(0)
		tempService = inputY("Total in Service: [" + str(oldItem.quantity["service"]) + "] ")
		if not tempService == "":
			newService = tempService
		else:
			newService = oldItem.quantity["service"]
			if newService == "":
				newService = str(0)
		tempRepair = inputY("Total under Repair: [" + (oldItem.quantity["repair"]) + "] ")
		if not tempRepair == "":
			newRepair = tempRepair
		else:
			newRepair = oldItem.quantity["repair"]
			if newRepair == "":
				newRepair = str(0)
		if int(newService) + int(newRepair) == int(newTotal):
			validAmount = True
		else:
			printR("Totals do not add up. Please try again.")
		quantity = {}
		quantity["total"] = newTotal
		quantity["service"] = newService
		quantity["repair"] = newRepair
	return quantity

'''gets manufacturer of item'''
def getManufacturer(oldItem):
	tempMan = inputY("Manufacturer: [" + str(oldItem.manufacturer) + "] ")
	if not tempMan == "":
		newMan = tempMan
	else:
		newMan = oldItem.manufacturer
	return newMan

'''gets model of item'''
def getModel(oldItem):
	tempModel = inputY("Model: [" + str(oldItem.model) + "] ")
	if not tempModel == "":
		newModel = tempModel
	else:
		newModel = oldItem.model
	return newModel

'''gets location of item'''
def getLocations(oldItem,validRooms):
	printB("To remove an existing location complete designate room as 'removed' ")
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
		if inputY("Is there another location (y/N) ") == "y":
			location = {}
			location["room"] = validRoom("",validRooms)
			location["storage"] = validStorage("")
			if not location["room"] == "" and not location["storage"] == "":
				newLocations.append(location)
			else:
				printR("Location is invalid. Not adding location")
		else:
			allLocations = True
	return newLocations

'''validats room entry'''
def validRoom(oldRoom,validRooms):
	valid = False
	while not valid:
		tempRoom = inputY("Room: ["+ str(oldRoom) +"] ")
		if tempRoom == "removed":
			return False
		if not tempRoom == "":
			if tempRoom in validRooms:
				newRoom = tempRoom
				valid = True
			else:
				printR(str(tempRoom) + " is not a valid room. Please try again.")
		else:
			newRoom = oldRoom
			valid = True
	return newRoom

'''gets storage room'''
def validStorage(oldStorage):
	tempStorage = inputY("Storage: [" + str(oldStorage) + "] ")
	if not tempStorage == ""	:
		newStorage = tempStorage
	else:
		newStorage = oldStorage
	return newStorage	


'''Collects input from user on the new piece of equipment'''
def getEquipInfo(oldItem,validRooms):
	if debug: printG("[Debug - getEquipInfo] entering")
	info = {}
	infoIsKit,infoName,infoKit = getKit(oldItem)
	info["idnum"] = oldItem.id_num
	info["is_kit"] = infoIsKit
	info["name"] = infoName
	info["kit"] = infoKit
	if not infoIsKit:
		info["name"] = getName(oldItem)
	infoQuantity = getQuantity(oldItem,infoIsKit)
	info["quantity"] = infoQuantity
	infoManufacturer = getManufacturer(oldItem)
	info["manufacturer"] = infoManufacturer
	infoModel = getModel(oldItem)	
	info["model"] = infoModel
	infoLocations = getLocations(oldItem,validRooms)
	info["locations"] = infoLocations
	if debug: printG("[Debug - getEquipInfo] leaving with return " + str(info))
	return info

'''displays collected information for comfirmations'''
def checkEquipInfo(info):
	print("")
	printC("---------------------------------------------------")
	print("")
	printC("ID Number: " + str(info["idnum"]))
	printC("Name: " + str(info["name"]))
	printC("Is Kit: " + str(info["is_kit"]))
	if info["is_kit"]:
	 	print("Kit Contents:")
	 	printC(str(info["kit"]))
	printC("Total amount: " + info["quantity"]["total"])
	printC("Amount in service: " + info["quantity"]["service"])
	printC("Amount under repair: " + info["quantity"]["repair"])
	printC("Manufacturer: " + info["manufacturer"])
	printC("Model: " + info["model"])
	locations = info["locations"]
	count = 0
	for i in locations:
		count = count + 1
		printC("Location-" +str(count) + ": " + i["room"] + i["storage"])
	if inputY("Is the displayed information is correct. (y/N) ") == "y":
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
	images = os.listdir(imageDir)
	imageInfo = []
	ids = []
	for i in images:
		try:
			int(i[:4])
			ids.append(i[:4])
			image = {}
			image["id"] = (i[:4])
			image["name"] = i
			imageInfo.append(image)
		except Exception as e:
			printY(str(i + " is not an image in the proper format."))
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


'''Generates a list of rooms with storage units'''
def makeRoomList(eqTree):
	validRooms=[]
	validUnits = []
	for i in eqTree.findall("./Item/Locations/Location"):
		room = i.findtext("Room")
		storage = i.findtext("Storage")
		unit = {"room": room, "unit": storage}
		if not room in validRooms:
			validRooms.append(room)
		if not unit in validUnits:
			validUnits.append(unit)
	validRooms.sort()
	return validRooms, validUnits

'''Get a stortage unit from user'''
def getUnit(rooms,units):

	'''Get room from list of rooms in database'''
	
	validRoom = False
	while not validRoom:
		for (i, item) in enumerate(rooms, start=0):
			printB("["+str(i) +"] " + str(item))	
		roomIndex = inputY("Choose Room Index: ")
		#roomIndex = 13
		try:
			room = rooms[int(roomIndex)]
			validRoom=True
		except Exception as e:
			printR("[Error] - " + str(e) +". Please try again.")

	'''Gets storage unit from units in selected room'''
	validUnit = False
	validUnits = []

	for i in units:
		if i['room'] == room:
			validUnits.append(i['unit'])
	validUnits.sort()

	while not validUnit:
		for (i, item) in enumerate(validUnits, start=0):
			printB(("[" + str(i) + "] " + str(item)))
		unitIndex = inputY("Choose a storage unit. ")
		#unitIndex = 3
		try:
			unit = validUnits[int(unitIndex)]
			validUnit = True
		except Exception as e:
			printR("[Error] - " + str(e) +". Please try again.")
	return room, unit

'''generates list of items in a storage unit'''

def itemsInUnit(room,unit,eqTree):
	items = []
	for i in eqTree:
		#print(i.attrib)
		locations=i.findall(".//Locations/Location")
		quantity = i.findtext(".//Total")
		#printR(str(quantity))
		for loc in locations:
			itemRoom = loc.findtext("Room")
			itemUnit = loc.findtext("Storage")
			if itemRoom == room and itemUnit == unit:
				items.append(addItem(i,quantity))

	return items
				#print(i[0].text, "is in", itemRoom,itemUnit)

def addItem(unit,quantity):
	unitInfo = {}
	unitInfo['id'] = unit.attrib['id']
	unitInfo['name'] = unit.findtext("./InventoryName")
	thumbnail= unit.findtext(".//Thumbnail")
	unitInfo['quantity'] = quantity
	if not thumbnail == "/img/img-placeholder.png":
		unitInfo["thumbnail"] = thumbnail
	else:
		unitInfo["thumbnail"] = "None"
	return unitInfo

def printUnitList(room,unit,lst):
	printC("Storage Unit " + str(room) + str(unit)+ " Contents." )
	for i in lst:
		name = i['name'] + " "
		name = name.ljust(35, '-')
		quantity = str(i['quantity']).rjust(3, " ")
		if i['thumbnail'] == "None":
			picMessage = " NEEDS PICTURE"
		else:
			picMessage = ""
		printB(i['id'] + " " + name + " " + str(quantity) + picMessage)

def menuSelection(menu):
	validEntry = False
	while not validEntry:
		for (i, item) in enumerate(menu, start=0):
			printB("[" + str(i) + "] " + item['name'])
		selection = inputY("Please Choose an Option: ")
		try:
			option = menu[int(selection)]["option"]
			validEntry = True
			return option
		except Exception as e:
			printR("[Error] " + selection + " is not a valid entry. Please try again.")


### Main Script


'''Define user options'''
parser = argparse.ArgumentParser()
parser.add_argument('-r', '--remove', help='Delete a piece of equipment from db.', action='store_true')
parser.add_argument('-d', '--debug', help='Debug Mode.', action='store_true')
parser.add_argument('-u', '--unitPrint', help='Print equipment in a specified unit.', action='store_true')
parser.add_argument('-e', '--edit', help='Edit details of a piece of equipment.', action='store_true')
parser.add_argument('-i', '--images', help='Add all images in ~/staffresources/equipment/equipimg to the equipment database.', action='store_true')
parser.add_argument('-m', '--manuals', help='Add all manuals in ~/staffresources/equipment/equipman to the equipment database.', action='store_true')
parser.add_argument('-n', '--new', help='Add new piece of equipment.".', action='store_true')
parser.add_argument('-t', '--test', help='Debug mode.', action='store_true')
parser.add_argument('-x', '--validate', help='Disable validation for xml.', action='store_true')
parser.add_argument('-v', '--version', help='Print current verion of script.', action='store_true')
args = parser.parse_args()

debug=args.debug
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


'''Menu Items'''
menu=[
	{"option": "edit", "name": "Edit Item"},
	{"option": "new", "name": "Add New Item"},
	{"option": "delete", "name": "Delete Item"},
	{"option": "printUnit", "name": "Print Storage Unit Contents"},
	{"option": "images", "name": "Update thumbnails"},
	{"option": "manuals", "name": "Update manuals"},
	{"option": "quit", "name":"Quit"}
	]

'''Changes the output to a temporary file if script is run in test mode'''
if testMode:
	destXML = root + "/dev/test_equipmentDB.xml"
	printC("----------Running in test mode.----------")	
else:
	destXML= eqdbDev

'''Check if it is being run by root'''
# if not os.getuid() == 0:
#     printR("[WARNING - main ] This script must be run by \"The Great and Powerful Sudo\". Exiting!")
#     exit()


'''name of host machine this scipt was written for'''
devHost=["slug","fry", "scruple", "asgard"]

'''Confirm that this script won't accidently run on the wrong machine'''
testHost(devHost)

'''validation disabled warning'''
if validate:
	printB("validation of output file has been disabled. Be Very Careful!")

'''Create pjlDB object of each of the relevent xml files'''
eqdb = pjlDB.EquipDB("/usr/local/master/pjl-web/dev/equipmentDB.xml")
labdb = pjlDB.LabDB("/usr/local/master/pjl-web/dev/labDB.xml")

'''prints version'''
if args.version:
	printB("Version " + version)
	exit()


'''Checks that the development version of both key DBs are new or as new as the live versions.'''
if not checkTimeStamp(eqdbDev,eqdbData) or not checkTimeStamp(labdbDev,labdbData):
	if not checkTimeStamp(eqdbDev,eqdbData):
		printR("Equipment development database is out of synce with the live version. Please update the development version before continuing.")
	if not checkTimeStamp(labdbDev,labdbData):
		printR("Repository development database is out of synce with the live version. Please update the development version before continuing.")
	print("Exiting...")
	exit()

'''Allows running in test mode where nothing is saved'''
if args.test:
	printY("Running in test mode. No changes will be saved")



'''Start Menu Loop'''
doneEdits = False

while not doneEdits:

	'''get menu selection from user'''
	selection = menuSelection(menu)
	if debug: printG("[Debug - main] menu option selected is " + selection)
	
	'''edits an existing equipment item'''
	if selection == "edit":
		equipItem = getItemToEdit(eqdb)
		confirmed = False
		while not confirmed:
			equipInfo = getEquipInfo(equipItem,validRooms)
			if checkEquipInfo(equipInfo):
				confirmed = True
				addEquip(equipItem,equipInfo,eqdb)

	'''adds a brand new item to next available eqid number'''
	if selection == "new":
		if debug: printG("[Debug - main] adding new item")
		equipItem = eqdb.newItem(eqdb.new_id)
		confirmed = False
		while not confirmed:
			equipInfo = getEquipInfo(equipItem,validRooms)
			if checkEquipInfo(equipInfo):
				confirmed = True
				addEquip(equipItem,equipInfo,eqdb)

	'''calls functions for deleting equipment item'''
	if selection == "delete":
		deleteEquipItem(eqdb,labdb)

	'''prints items is a storage unit'''
	if selection == "printUnit":
		printB("Printing Unit Contents")
		tree = eqdb.tree
		eqTreeRoot = tree.getroot()
		rooms, units = makeRoomList(eqTreeRoot)
		room, unit = getUnit(rooms,units)
		itemList = itemsInUnit(room,unit,eqTreeRoot)
		printUnitList(room,unit,itemList)

	'''calls functions for updateing images for equipment'''
	if selection == "images":
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
				printB(equip.thumbnail)
			else:
				equip.thumbnail = "/img/img-placeholder.png"
				printB(equip.thumbnail)
				eqdb.addItem(equip)


	'''calls functions for updateing manuals for equipment'''
	if selection == "manuals":
		listOfIDs = equipWithMan(manualDir)
		#print(listOfIDs)
		for i in listOfIDs:
			equipManuals,eqID = manInfo(i,manualDir,manualLocal)
			#print(equipManuals,eqID)
			equip = eqdb.getItem(idnum=eqID)
			equip.documents = equipManuals
			#print(equip.documents)
			eqdb.addItem(equip)


	
	if selection == "quit":
		doneEdits = True
	'''calls functions for editing an existing equipment entry'''

	'''saves new xml file'''
	if args.test:
		print(" not saving " + destXML)
		#print(type(destXML))
		#eqdb.save(destXML, ignore_validation=validate, error_log=True)
	else:
		print("saving to " + destXML)
		eqdb.save(destXML, ignore_validation=validate, error_log=True)

printG("Finished Loop")




'''confirms that the script has ended properly'''
print("...and then there will be cake")
