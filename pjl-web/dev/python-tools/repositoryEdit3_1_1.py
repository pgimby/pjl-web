#!/usr/bin/python3

'''
Can be called from the command line to make a wide range of changes to the lab repository xml file.
Change include

Adding versions of labs from a new semester
Adding a brand new lab to repository

color scheme
	red ERROR - FATAL
	green DEBUG
	blue Information 
	cyan Information - alternate
	yellow INPUT

'''

'''Verison History

1.4 added the ability to customize the name give to a kit when only part of the kit is used.
2.1.1 accept idnum for new lab from user
2.1.2 replace color package with colorama
2.1.3 cleaned up function to get rid of repetitive functions
3.0	rewrote several function and fixed known bugs
3.0.1 replace dev version of labDB with data version after updating data version.
3.1.1 fixed an issue with unwanted characters in lab names being improperly replaced.

'''
import pjlDB
import os, argparse, re
import colorama
from colorama import Fore, Style
from pprint import pprint

version = "3.1.1 - Last Update Aug 2, 2022"

# Functions for general appearance

def printG(txt):
    print(Fore.GREEN + txt + Style.RESET_ALL)

def printR(txt):
    print(Fore.RED + txt + Style.RESET_ALL)

def printB(txt):
    print(Fore.BLUE + txt + Style.RESET_ALL)

def printY(txt):
    print(Fore.YELLOW + txt + Style.RESET_ALL)

def printC(txt):
    print(Fore.CYAN + txt + Style.RESET_ALL)

def inputY(txt):
	return input(Fore.YELLOW + txt + Style.RESET_ALL)


#Fucntion that preform validity checks

def testHost(host):
	'''
	Test what computer this being run on. As of now it is machine specific
	
	Args:
		host (lst) name of host script was designed for
	
	Return:
		none
	'''
	thishost = os.uname()[1]
	if thishost not in host:
		printR("[ERROR] " + "This script is designed to be run on " + host + " only. Exiting...")
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

def validCourse():
	'''
	#Asks user to enter the course the lab was used in, and checks it against a global list of valid courses

	Args:
		none

	Return:
		course (str) valid course number
	'''
	validCourse = False
	while not validCourse:
		courseNum = str(inputY("Enter course number: "))
		for i in validCourses:
			if courseNum == i:
				course = "PHYS " + courseNum
				validCourse = True
		if not validCourse:
			printR("Invalid Course number")
			printB("Valid courses are...")
			for i in validCourses:
				print(i)
	return course

def validSemester():
	'''
	Asks user to enter the semester the lab was used in, and checks it against a list of valid semesters

	Args:
		validSemesters (list) list of valid courses

	Return:
		semesterName (str) valid semester name
	'''
	validSemester = False
	while not validSemester:
		semesterName = str(inputY("Enter semester: ")).capitalize()
		for i in validSemesters:
			if semesterName == i:
				validSemester = True
		if not validSemester:
			printR("Invalid semester")
			printB("Valid semesters are...")
			for i in validSemesters:
				printB(i)
	return semesterName

def validYear():
	'''
	Asks user to enter the year the lab was used in, and checks that it is a valid year

	Args:
		none

	Return:
		year (str) valid 4 digit year
	'''
	validYear = False
	while not validYear:
		year = inputY("Enter year: ")
		if len(year) == 4 and year.isdigit() == True:
			validYear = True
		else:
			printR("Year is invalid.")
	return year


#Functions used to add a new version entry to the repositorsy xml

def getLabObject():
	'''
	Used to generate a pjl lab object from the labDB.xml database

	Args:
		labdb (pjlDB.labDB) entire lab database object generated by pjlDB

	Return:
		lab (pjlDB._LabItem) individual lab item generated by pjlDB
	'''
	if debug: printG("[Debug - getLabObject] entering")
	validID = False
	while not validID:
		idnum = inputY("Enter lab ID number: ")
		if len(idnum) == 4 and idnum.isdigit() == True:
			try:
				lab = labdb.getLab(idnum)
				validID = True
			except pjlDB.IDDoesNotExist: ### not working properly
				printR("Error: lab " + str(idnum) + " does not exist. Please try again.")
		else:
			printR("[ERROR] " + "ID formate in not valid. Valid IDs are of the form ####. Please try again")
			validID = False
	if debug: printG("[Debug - getLabObject] leaving")
	return lab

def getOriginalDir():
	'''
	Asks user for location of folder containing new lab, and check that it exists

	Args:
		none

	Return:
		originalDir (str) location of folder containing all files for new lab
	'''
	validDir = False
	while not validDir:
		originalDir = inputY("Enter absolute path for directory containing lab version: ")
		if not originalDir.split("/")[-1] == "":
			originalDir = originalDir + "/"
		if os.path.isdir(originalDir):
			validDir = True
		else:
			printR("Directory " + str(originalDir) + " does not exist. Please try again.")
	return originalDir

def getOriginalPdf(dir):
	'''
	Asks user for name of lab pdf file, and check that it exists

	Args:
		dir (str) pathname of the folder that the pdf should be in originally

	Return:
		pdfName (str) location of pdf file for new lab
	'''
	validPath = False
	while not validPath:
		pdfName = inputY("Enter the name of the student version pdf: ")
		if os.path.isfile(dir + pdfName):
			validPath = True	
		else:
			printR("PDF does not exist. Please try again.")
	return pdfName


# Functions used to edit equipment lists

def getEquipList(eqdb,originalItem):
	'''
	Generates a list of equipment currently assigned to a lab. 

	Args:
		eqdb (pjlDB.EquipDB) entire equipment inventory database object generated by pjlDB
		originalItem (pjlDB._LabItem) individual lab item generated by pjlDB

	Return:
		equipItems (list of dictionaries)
	'''
	if debug: printG("[Debug - getEquipList]  entering")
	print("")
	
	# print out equipment assigned to a lab
	if inputY("Would you like to edit the equipment list for this lab? y/N ").lower() == "y":
		print("")
		printB("Current Equipment List")
		printB("----------------------")
		for i in originalItem.equipment:
			printB(i['id'] + " " + i['name'] + " [" + i['alt-id'] + " " + i['alt-name'] + "] " + " (" + i['amount'] + ")")
		print("")
		
		# generate the new list of equipment
		equipItems = []

		# confirm/edit existing lab equipment
		equipItems = equipInfoReview(eqdb,originalItem)
		allItems = False

		# add new equipment items to lab
		while not allItems:
			print("")
			if inputY("Would you like to add a new piece of equipment for this lab? y/N ").lower() == "y":
				newItem = getNewEquip(eqdb,originalItem)
				if not newItem == False:
					if not any(d['id'] == newItem['id'] for d in equipItems):
						equipItems.append(newItem)
					else:
						printR(str(newItem['name']) + " Already exists in equipment list.")
			else:
				allItems = True
	else:
		equipItems = originalItem.equipment
	if debug: printG("[Debug - getEquipList]  leaving")
	return equipItems

def equipInfoReview(eqdb,originalItem):
	'''
	Controls the review and editing of equipment list. Asks user to input id numbers and 
	quantity of equipment needed for the new lab. User also can input an alternate/secondary 
	equipment item for each primary item
	
	Input id numbers are check for correctness

	Args:
		eqdb (pjlDB.EquipDB) entire equipment inventory database object generated by pjlDB
		originalItem (pjlDB._LabItem) individual lab item generated by pjlDB
	
	Return:
		equipItems (list of dictionaries)
	'''
	if debug: printG("[Debug - equipInfoReview]  entering")
	equipItems = []
	if originalItem.equipment:
		for i in originalItem.equipment:
			printC("ID Number ["  + i['id'] + "]: Name [" + i['name'] + "]: Alternate Name: [" + i['alt-name'] + "]: Amount [" + i['amount'] + "]" )
			userInput = inputY("To edit press \"y\", To delete enter \"delete\", to continue to next item press \"enter\". [enter]: ")
			if userInput.lower() == "y":
				item = getNewEquip(eqdb,originalItem)
				if item == False:
					equipItems.append(i)
				elif not any(d['id'] == item['id'] for d in equipItems):
					equipItems.append(item)
				else:
					printR(str(item['name']) + " Already exists in equipment list.")
			elif userInput.lower() == "delete":
				printB("deleting " + i['id'] + " " + i['name'] + "\n")
			elif userInput.lower() == "":
				equipItems.append(i)
	if debug: printG("[Debug - equipInfoReview]  leaving")
	return equipItems

def getNewEquip(eqdb,origianlItem):
	'''
	Gets information about new equipment to add to lab equipment list
	
	Input id numbers are check for correctness,

	Args:
		eqdb (pjlDB.EquipDB) entire equipment inventory database object generated by pjlDB
		originalItem (pjlDB._LabItem) individual lab item generated by pjlDB
	
	Return:
		newItem (dict)
	'''
	
	if debug: printG("[Debug - getNewEquip] entering")
	validOutput = False
	while not validOutput:
		itemId = ""
		newItem = {}
		
		# Get id number from user and check that it is in the database
		itemId = inputY("Enter the new equipment id number, or hit \"enter\" to continue. ")

		# Lets user it enter to continue
		if itemId == "":
			return False

		# Gets info from user and check that entries are valid
		try:
			newEquip = eqdb.getItem(idnum=itemId)
			newItem['id'] = newEquip.id_num
			newItem['name'] = getEquipName(newEquip)
			if not newItem['name'] == "":
				validOutput = True
					# return False
			newItem['alt-id'],newItem['alt-name'] = getAltEquip(eqdb)
			newItem['amount'] = getEquipAmount(newItem['name'])
			return newItem
		except pjlDB.EQIDDoesNotExist as e:
			printR(itemId + " is an invalid entry.")
		except Exception as e:
			printR("Something strange happened")
			printR(e.__class__)
			exit()

	if debug: printG("[Debug - getNewEquip] leaving")
	return newItem

def getEquipName(eqItem):
	'''
	Gets information about name for the equipment. If the item is a kit the name can be either
	the name of the kit, or the name of an item in the kit
	
	Args:
		eqItem (pjlDB._EquipmentItem) entire equipment inventory database object generated by pjlDB
	
	Return:
		eqItem.name (str) name chosen for the equipment item
	'''
	if debug: printG("[Debug - getEquipName] entering")
	if eqItem.is_kit:
		return equipNameOptions(eqItem)
	else:
		return eqItem.name

def getAltEquip(eqdb):
	'''
	Gets informaition for alternate equipment item name and id
	
	Args:
		eqdb (pjlDB.EquipDB) entire equipment inventory database object generated by pjlDB

	Return:
		newAltId (str) 		id number of alternate item
		newAltName (str) 	name of alternate item
	'''
	if debug: printG("[Debug - getAltEquip] entering ")
	validOutput = False
	while not validOutput:
		newAltItem = {}
		altId = inputY("Enter id number of an alternate for this item. If none hit Enter. ")

		# Lets user not include an alternate item
		if altId == "":
			newAltID = ""
			newAltName = ""
			return newAltID,newAltName 

		# Gets information about alternate item and check for validity
		try:
			altEq = eqdb.getItem(idnum=altId)
			newAltID = altEq.id_num
			newAltName = getEquipName(altEq)
			if not newAltName == "":
				return newAltID,newAltName
		except pjlDB.EQIDDoesNotExist as e:
			printR("Alternate item is not valid")

def getEquipAmount(itemName):
	'''
	Get information about amount of an item that is required

	Args:
		itemName (str) name used for displaying in the text output to user

	Return:
		amount (str) number 
	'''
	if debug: printG("[Debug - getEquipAmount]  entering")
	validNum = False
	while not validNum:
		amount = inputY("Please enter how many " + itemName + "(s) are needed? ")
		if amount.isdigit():
			return amount
		else:
			printR(amount + " is not a valid number.")
			if inputY("Do you wish to try again? Y/n: ").lower() == "n":
				return ""
	if debug: printG("[Debug - addEquipItem]  entering")

def equipNameOptions(item):
	'''
	Sometimes a piece of a equipment is a piece of the kit. In these cases it can be useful for the name
	in the equipment list to appear as the part, but keep the equipment id number of the kit. This function
	allows the user to choose a name from the list of components in a kit.

	Args:
		item (pjlDB.EquipDB) entire equipment inventory database object generated by pjlDB

	Return:
		name (str) Name of equipment item
	'''
	if debug: printG("[Debug - equipNameOptions]  entering")
	print()
	printY("What name you would like displayed for this item? Pick a number [default = 0].")
	print()

	# Displays the list if items in a kit for easy viewing and selection by user
	kitItems = item.kit.split(",")
	kitItems[:0] = [item.name]
	for i in range(0, len(kitItems)):
		index = str(i)
		print("[" + index + "] " + kitItems[i].strip())
	
	# Request input from user 
	validName = False
	while not validName:
		name = ""
		selection = inputY("Please Choose a Name for This Item? [0] ")
		if selection == "":
			selection = 0
		try:
			itemNum = int(selection)
		except ValueError:
			printR(selection + " Is not an integer.")
			if not inputY("Would you like to try again? Y/n: ").lower() =="n":
				continue
			else:
				return ""

		try:
			name = kitItems[itemNum].strip()
		except IndexError:
			printR(selection + " Is not in the rage of items.") 
			if not inputY("Would you like to try again? Y/n: ").lower() =="n":
				continue
			else:
				return ""

		validName = True
	return name


# Funtions used to edit list of software, disciplines, and topics

def getRestrictedList(originalItem,originalList,listSource,listName):
	'''
	generates a list of restricted items. In order to be include in the xml a list item must be in the master list

	Args:
		originalItem (pjlDB._LabItem) individual lab item generated by pjlDB
		originalList (list) current list of items included
		listSource (string) path to file containing list of available items
		listName (string) name of list being edited

	Return:
		restrictedItems (list) valid updated list
	'''
	if debug: printG("editing a restricted list (" + listName + ").")
	restrictedItems = []
	
	# print out current items in list
	if inputY("Would you like to edit the " + listName + " list for this lab? y/N ").lower() == "y":
		print("")
		printB("Current "+ listName)
		printB("-------------------")
		for i in originalList:
			printB(i)
		print("")

		# Gives user the option to remove each item currently in list
		restrictedItems = restrictedRemove(originalItem,originalList,listName)

		# Gathers information from user on any new items to be added to list
		allItems = False
		while not allItems:
			if inputY("Would you like to add a new " + listName + " for this lab? y/N ").lower() == "y":
				print("")
				masterList = getValidList(listSource)
				#print("")
				printB("Valid " + listName)
				printList(masterList)
				restrictedItem = getNewRestricted(masterList,listName)
				if not restrictedItem == False:
					restrictedItems.append(restrictedItem)
				else:
					printR("Invalid " + listName + " entered.")
			else:
				allItems = True
		restrictedItems = list(set(restrictedItems))
	else:
		restrictedItems = originalList
	return restrictedItems

def restrictedRemove(originalItem,originalList,listName):
	'''
	Removes unwanted item from list

	Args:
		originalList (list) current list of items included
		listName (string) name of list being edited
		originalItem (pjlDB._LabItem) individual lab item generated by pjlDB
	
	Return:
		restrictedItems (list) wanted to remain in list
	'''
	restrictedItems = []
	if originalList:
		for i in originalList:
	 		if not inputY("Would you like to remove \"" + i + "\" as needed " + listName + " software? If so enter 'delete': ").lower() == "delete":
		 		restrictedItems.append(i)	 			
	return restrictedItems

def getNewRestricted(masterList,listName):
	'''
	Get list of software from user and check if they are valid

	Args: 
		masterList (list) complete pool of valid topics

	Return:
		software (str) single valid software for new lab
	'''
	valid = False
	while not valid:
		item = inputY("Enter new " + listName + ": ")
		for i in masterList:
			if i.lower() == item.lower():
		 		valid = True
		 		item = i
		 		printB("Adding " + i + " to " + listName)
		 		print("")
		if not valid:
			printR(item + " is invalid " + listName +".")
			if not inputY("Would you like to try again? Y/n ").lower() == "n":
	 			continue
			else:
				return False
	return item

def getValidList(listSource):
	'''
	Generates list of valid selections from file

	Args:
		listSource (string) path to file containing valid list entries

	Return:
		validList (list) list of valid selections

	'''
	validList = open(listSource).readlines()
	for i in range (0,len(validList)):
		validList[i] =  validList[i].replace('\n','').strip()
	validList = list(filter(None, validList))
	return validList


# Functions for printing and confirming lists and entries

def printList(lst):
	'''
	Prints a list of strings line by line for easy readability

	Args:
		lst (list) list of strings to be printed

	Return:
		none
	'''
	printB("-------------------")
	for i in lst:
		printB(i)
	print("")

def confirmEntry(newLabInfo):
	'''
	print out what information entered by usee, and asks for confirmation

	Args:
		new_version (dict) dictionary containing all data in for that pjlDB can enter into database

	Return:
		(bool) True if information has been confirmed by user
	'''
	print("")
	printY("-------------------------------------------------------")
	print("")

	printB("Please confirm that the information entered is correct")
	displayLabItem(newLabInfo)
	if not inputY("Is this information correct? N/y: ").lower() == "y":
		print("exiting...")
		exit()
	else:
		return True

def displayLabItem(lab):
	if debug: printG("[Debug - displayLabItem] entering")
	print("")
	printB("ID: " + lab.id_num)
	print("")
	printB("Name: " + lab.name)
	print("")
	printB("Type: " + lab.lab_type)
	print("")
	printVersions(lab.versions)
	print("")
	printB("Equipment: ")
	printB("----------")
	printEquipList(lab.equipment)
	print("")
	printB("Disciplines: ")
	printList(lab.disciplines)
	printB("Topics: ")
	printList(lab.topics)
	printB("Software: ")
	printList(lab.software)
	if debug: printG("[Debug - displayLabItem] leaving")

def printEquipList(equipList):
	for i in equipList:
		printB(i["id"] +": " + i["name"] + " (" + i["amount"] + "), " + i["alt-id"] + ": " +  i["alt-name"])

def printVersions(labVersions):
	if debug: printG("[Debug - printVersions] entering")

	versions = []
	if args.new or args.add:
		print("Version to Add:")
		print("--------------------")
		versions.append(labVersions[-1])
	elif args.edit:
		return
	else:
		print("Versions in databas:")
		print("--------------------")
		versions=labVersions
	for i in versions:
		print(i["course"] + " " + i["semester"] + " " + i["year"] )


#Functions for moving directory into repository

def emptyDir(version):
	'''
	checks that the verison has not already been added to repository file structure

	Args:
		info (dict) information about new lab object
		root (str) root path of lab repository

	Return:
		(bool) True is lab has not already been added to repository file structure
	'''
	versionDir = root + version["directory"]
	if not os.path.isdir(versionDir):
		return True
	else: 
		printR("Lab folder " + versionDir + " Already Exists.")
		print("Exiting...")
		return False

def moveVersionDir(info,root):
	'''
	adds source file to lab repository.
		Makes new directory
		rsyncs files except for contents of Support_Docs folder

	Args:
		info (dict) information about new lab object
		root (str) root path of lab repository

	Return:
		none
	'''
	if debug: printG("[Debug - moveVersionDir] entering")
	versionDir = root + info["directory"]
	if not os.path.isdir(versionDir):
		os.system("mkdir " + versionDir)
		os.system("sudo rsync -avz --exclude Support_Docs " + info["originalDir"] + " " + versionDir)
	else:
		print("") 
		printB("Lab folder " + versionDir + " Already Exists.")
		print("")
		if inputY("Do you want to update the folder contents? N/y: ").lower() == "y":
			print("")
			os.system("rsync -avz --exclude Support_Docs " + info["originalDir"] + " " + versionDir)
		else:
			printB("Exiting...")
			exit()
	if debug: printG("[Debug - moveVersionDir] leaving")

def addSupportFolder(info,root):
	'''
	adds contents of Support_Docs folder to repository

	Args:
		info (dict) information about new lab object

	Return:
		none
	'''
	originDir = info["originalDir"] + "Support_Docs"
	destinationDir = root + info["labFolder"] + "/Support_Docs"
	if os.path.isdir(originDir):
		if not os.path.isdir(destinationDir):
			printB("Support_Docs Folder does not exist. Adding new folder " + str(destinationDir))
			os.system("mkdir " + destinationDir)
		if os.path.isdir(destinationDir):
			os.system("rsync -avz " + originDir + "/ " + destinationDir)
		else:
			printR("[ERROR] " + "Something when wrong. Exiting...")
			exit()


# Functions for adding a new lab or lab version

def getNewId(idTry):
	'''
	Checks that a user specified new id number is valid

	Args:
		info (dict) information about new lab object

	Return:
		none
	'''
	validID=False
	while not validID:
		try:
			labdb.newLab(idTry)
			return idTry
		except Exception as e:
			printR(str(idTry) + " is not a valid lab id number or already is in use.")
			idTry = inputY("Please enter a 4 digit number for the new lab ID, or hit \"enter\" to select the next available one.")
			print("")
			if idTry == "":
				idTry = str(labdb.new_id)
				return idTry
			else:
				continue
			#idEntered = inputY("s")
			#print(e.__class__)
		
		#raise

def editingLab(newLab,testMode):
	'''
	Main function that collects information for new lab entry

	Args:
		originalItem (pjlDB._LabItem) individual lab item generated by pjlDB
		validCourses (list) list of valid courses
		validSemesters (list) list of valid semesters
		semesterKeys (dict) dictionary that matches semesters with their abreviations
		eqdb (pjlDB.EquipDB) entire equipment inventory database object generated by pjlDB
		disiplineSource (str) path of file that contains all valid disciplines
		topicSource (str) path of file that contains all valid topics
		testMode (bool) allows script to be run in testing mode. No output written.
	
	Return:
		new_lab (dict) dictionary that contains information needed for pjlDB package to create new lab object
		labFolder (str) path of parent folder to create for new lab
	'''
	if debug: printG("[Debug - editingLab] entering")
		
	# if this is a new lab the user can add a name and lab type, else the existing one is used.
	if not newLab.name:
		#newLab.name = "Test Lab" # getName(newLab) # Name of lab
		newLab.name = getName(newLab) # Name of lab
	printB("Making changes to " + newLab.name)
	if not newLab.lab_type:
		#newLab.lab_type = "Home" # getType() # Type of lab
		newLab.lab_type = getType() # Type of lab
	
	if not args.edit:
		newVersion = getVersionInfoNew(newLab)
		newLab.addVersion(newVersion)
		newLab.version = newVersion

	
	#newLab.equipment = [{'id': '0001', 'name': 'Fluke multimeter', 'alt-name': 'Anatek power supply', 'alt-id': '0002', 'amount': '3'}]
	newLab.equipment = getEquipList(eqdb,newLab)
	#newLab.software = ['Canon'] #getRestrictedList(newLab,newLab.software,softwareSource,"software")
	newLab.software = getRestrictedList(newLab,newLab.software,softwareSource,"software")
	#newLab.disciplines = ['Math'] #getRestrictedList(newLab,newLab.disciplines,disciplineSource,"discipline")
	newLab.disciplines = getRestrictedList(newLab,newLab.disciplines,disciplineSource,"discipline")
	#newLab.topics = ['ODE'] #getRestrictedList(newLab,newLab.topics,topicSource,"topic")
	newLab.topics = getRestrictedList(newLab,newLab.topics,topicSource,"topic")
	
	if debug: printG("[Debug - editing] leaving")
	#return newLab


def getName(originalItem):
	'''
	Asks user to enter name of new lab, and check that the name is not already used

	Args:
		originalItem (pjlDB._LabItem) individual lab item generated by pjlDB

	Return: 
		labName (str) name of new lab
	'''
	labName = originalItem.name
	if originalItem.name == "":
		validName = False
		while not validName:
			labName = str(inputY("Enter name of the new lab. Please use conventional titlecase (ie. This is a Title of a New Lab): "))
			if inputY("Is this name entered correctly? N/y: ").lower() == "y":
				validName = True
			elif inputY("Would you like to try again? Y/n ").lower() == "n":
				print("Exiting.")
				exit()
	return labName

def getType():
	'''
	asks user what type of experiment this is. There are only two options lab or labatorial

	Args:
		none

	Return (str) type experiment. lab or labatorial
	'''
	validType = False
	while not validType:
		labType = inputY("Is this a lab, labatorial, home, or remote? ").lower()
		if labType == "lab" or labType == "labatorial" or labType == "home" or labType == "remote":
			validType = True
		else:
			if inputY("Would you like to try again? Y/n: ").lower() == "n":
				exit()
	return labType.capitalize()

def newLabFolder(labName,idNumber):
	'''
	determine name of folder for a new lab

	Args:
		info (dict) information about new lab object
	'''
	name = "-".join(labName.split(" "))
	for i in replaceCharList:
		name = name.replace(i,'-')
	for i in removeCharList:
		name = name.replace(i,'')
	labFolder = "/data/repository/" + idNumber + "-" + name
	labFolderPath = root + labFolder
	if debug: printG("[Debug - newLabFolder] labFolder and path are " + labFolder + " and " + labFolderPath)
	return labFolder,labFolderPath

def newVersionFolder(newVersion,newLab):
	'''
	determine name of folder for a new lab. This is different than the function
	(validExistingDirectory) which uses knowledge of existing version folders.

	Args:
		info (dict) information about new lab object
		labFolder (str) path of the new lab parent folder in repository
		semesterKeys (dict) matches full name semesters with abreviation

	Return:
		directory (str) path of version directory for a new lab
	'''
	if debug: printG("[Debug - newVersionFolder] entering")
	semester = semesterKeys[newVersion["semester"]]
	courseNum = newVersion["course"].split(" ")[-1]
	directory = newVersion["labFolder"] + "/" + newLab.id_num + "-PHYS" + courseNum + semester + newVersion["year"]
	if debug: printG("[Debug - newVersionFolder] directory is " + directory)
	return directory


def getVersionInfoNew(newLab):
	if debug: printG("[Debug - getVersionIfoNew] entering")
	newVersion = {}
	#newVersion["originalDir"] = "/home/pgimby/labs/under-construction/tmp/" #getOriginalDir() # location that lab documents reside outside of repository
	newVersion["originalDir"] = getOriginalDir() # location that lab documents reside outside of repository
	#newLab.pdf = "tmp2.pdf" # getOriginalPdf(new_version["originalDir"]) # name of pdf to be displayed on website
	newLab.pdf = getOriginalPdf(newVersion["originalDir"]) # name of pdf to be displayed on website
	
	#newVersion["course"] = "323" # validCourse() # get the course number
	newVersion["course"] = validCourse() # get the course number
	#newVersion["semester"] = "Fall" # validSemester()  # get the semsester
	newVersion["semester"] = validSemester()  # get the semsester
	#newVersion["year"] = "2022" #validYear() # get the year
	newVersion["year"] = validYear() # get the year
	
	newVersion["labFolder"],newVersion["labFolderPath"] = newLabFolder(newLab.name,newLab.id_num) # newLabFolder is for displaying on the website newFolderPath is for syning documents into repository
	newVersion["directory"] = newVersionFolder(newVersion,newLab)
	printR(str(newVersion["directory"]))
	#new_version["path"] = validPdfPath(newLab.pdf, new_version)
	newVersion["path"] = newVersion["directory"] + "/" + newLab.pdf
	return newVersion


# Functions for updating an existing version of a lab. 

def getDeploymentID(version):
	'''
	Takes a dictionaries containing version of a lab, and pulls out a unique 
	identifier based on when a version was deployed, and in what course.
	The result is in the form 227FA2019.

	Args:
		version (dict)

	Return:
		deploymentId (string) unique identifer for when and where lab was used.
	'''
	if debug: printG("[Debug - get DeploymentID] entering")
	course = version["course"]#[5:]
	year = version["year"]
	semester = version["semester"]
	key = semesterKeys[semester]
	deploymentId = course + key + year
	return deploymentId

def updateVersion(originalItem,updatedVersionInfo):
	'''
	Takes a dictionaries containing versions of a lab, and replaces the pdf
	with the a new version as per user input

	Args:
		originalItem (pjlDB._LabItem) original lab object
		updatedVersionInfo (dict) updated information on the lab version

	Return:
		lab.versions (list) of dictionaries, one entry for each version.
	'''
	if debug: printG("[Debug - updateVersion] entering")
	newDeployId = getDeploymentID(updatedVersionInfo)
	for i in lab.versions:
		if getDeploymentID(i) == newDeployId:
			print("Replacing " + i["path"] + " with " + updatedVersionInfo["path"])
			if inputY("Would you like to procced with this change? N/y: ").lower() == "y":
				printY("Replacing " + i["path"] + " with " + updatedVersionInfo["path"])
				i["path"] = updatedVersionInfo["path"]
				return
			else:
				printB("Exiting...")
				exit()
	printR("Error: The lab to be updated does not exist in the database. Exiting...")
	exit()


# Functions for rotating lab database in preperation for updating live website

def get_db_files():
    all_files = os.listdir(db_storage)
    db_files = []
    for f in all_files:
        if f.startswith("labDB") and f.split(".")[0][-1] in ['0','1','2','3','4','5','6','7']:
            db_files.append(f)
    return sorted(db_files)

def increment_files(files):
    for i,f in enumerate(files):
        name = f.split(".")[0]
        index = int(name[-1])
        index += 1
        f = name[:-1] + str(index) + ".xml"
        os.rename(db_storage + files[i], db_storage + f)
    os.rename(db_storage + "labDB.xml", db_storage + "labDB-0.xml")
    os.system("cp " + new_xml + " " + db_storage + "labDB.xml")
    os.system("chmod 644 " + db_storage + "labDB.xml")
    os.system(" cp " + db_storage + "labDB.xml " + new_xml )


#Main Script

'''List of valid courses and semesters'''
validCourses = ["211", "223", "229", "227", "255", "259", "323", "325", "341", "355", "365", "369", "375", "397", "497", "597"]
validSemesters = ["Winter", "Spring", "Summer", "Fall"]
semesterKeys = {"Winter": "WI", "Spring": "SP", "Summer": "SU", "Fall": "FA"}

'''list of charachers that often appear in names that cause problmes. Replaces with a - '''
replaceCharList = [",","(",")","---","--"]

'''list of charachers that often appear in names that cause problmes. Remove charater all together'''
removeCharList = ["'"]

'''Paths for  files'''
root = "/usr/local/master/pjl-web"
eqdbDev = root + "/dev/equipmentDB.xml"
labdbDev = root + "/dev/labDB.xml"
eqdbData = root + "/data/equipmentDB.xml"
labdbData = root + "/data/labDB.xml"
disciplineSource = root + "/data/validDisciplines.txt"
topicSource = root + "/data/validTopics.txt"
softwareSource = root + "/data/validSoftware.txt"
db_storage = root + "/data/"
new_xml = root+ "/dev/labDB.xml"


'''Create pjlDB object of each of the relevent xml files'''
eqdb = pjlDB.EquipDB(eqdbDev)
labdb = pjlDB.LabDB(labdbDev)

'''Define user options'''
parser = argparse.ArgumentParser(
	formatter_class=argparse.RawDescriptionHelpFormatter,
	epilog='''
Know bugs and other important information:
------------------
	A) Spaces in the names of folders does not work.
''')
parser.add_argument('-a', '--add', help='Add a new version to an existing lab.".', action='store_true')
parser.add_argument('-d', '--debug', help='debug code', action='store_true')
parser.add_argument('-e', '--edit', help='Edit the details of a lab.', action='store_true')
parser.add_argument('-p', '--print', help='Print lab metadata.', action='store_true')
parser.add_argument('-n', '--new', help='Add a brand new lab.".', type=str, nargs='?', const=labdb.new_id)
parser.add_argument('-t', '--test', help='Debug mode.', action='store_true')
parser.add_argument('-x', '--validate', help='Disable validation for xml.', action='store_true')
parser.add_argument('-w', '--repwheel', help='cycle lab database xml to newest dev version. Save last 9 previous.', action='store_true')
parser.add_argument('-v', '--version', help='Print current verion of script.', action='store_true')
args = parser.parse_args()
testMode = args.test
validate = args.validate


'''check if running in debug mode'''
debug = args.debug

'''Changes the output to a temporary file if script is run in test mode'''
if testMode:
	destXML = root + "/dev/test_labDB.xml"
	print("----------Running in test mode.----------")	
else:
	destXML= labdbDev

'''validation disabled warning'''
if validate:
	printB("validation of output file has been disabled. Be Very Careful!")

'''name of host machine this scipt was written for'''
devhost = ["slug","fry","scruple","lumen","maxwell"]

'''Confirm that this script won't accidently run on the wrong machine'''
testHost(devhost)

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

'''add a new version of an existing lab'''
if args.add:
	lab = getLabObject()												# Generates a lab object from an existing entry in database
	printB("Adding new lab version to lab: [" + lab.id_num + "]")
	editingLab(lab,testMode)												# Gathers information on new version and appends it to lab object
	confirmEntry(lab)
	labdb.addLab(lab)						 								# Adds new version of lab to the master labDB.xml database
	if labdb.validateFull(error_log=False) and emptyDir(lab.versions[-1]):	# Checks that the lab database is still valid and error free
		moveVersionDir(lab.versions[-1],root)									# Moves last version added to lab folder
		addSupportFolder(lab.versions[-1],root)									# Adds new support documents to a general folder for all versions of lab
		labdb.save(destXML, ignore_validation=True, error_log=False)			# Saves the updated labDB.xml database
	else:
		printR("Error: XML Object is Invalid. Check error logs for details.")
		labdb.validateFull(error_log=True)	
		exit()

'''create a new lab'''
if args.new:
	#printB("Adding new lab.")
	newID = getNewId(args.new)	
	#print(str(args.new))
	#printC(str(type(newID)))
	#newID="0224"
	#lab = labdb.newLab(args.new)										# Generates a new blank lab
	lab = labdb.newLab(newID)										# Generates a new blank lab
	printB("Adding new lab with id number: [" + lab.id_num + "]")
	editingLab(lab,testMode)											# Gathers information from user regarding new lab and adds to blank lab
	confirmEntry(lab)													# Has user confirm that information was entered properly
	labdb.addLab(lab)													# Adds new lab to the master labDB.xml database
	if labdb.validateFull(error_log=False):								# Checks that the lab database is still valid and error free
		os.system("mkdir " + lab.versions[0]["labFolderPath"])				# Makes a directory for the new lab
		moveVersionDir(lab.versions[0],root)								# Moves lab documents for first version in to lab folder
		addSupportFolder(lab.versions[0],root)								# Adds support documents to a general folder for all versions of lab
		labdb.save(destXML, ignore_validation=True, error_log=False)		# Saves the updated labDB.xml database
	else:
		printR("Error: XML Object is Invalid. Check error logs for details.")
		labdb.validateFull(error_log=True)									# Exports errors to log file if validation fails

'''edits an existing lab'''
if args.edit:
	lab = getLabObject()															# Generates a lab object from an existing entry in database
	print("")
	printB("Editing " + lab.name)
	editingLab(lab,testMode)														# Gathers information regarding edits to be made
	if inputY("Would you like to updated a version of  lab? y/N ").lower() == "y":
		updatedVersion = getVersionInfoNew(lab)										# Get information on a updated version of lab pdf
		updateVersion(lab,updatedVersion)
	else:
		updatedVersion = False
	confirmEntry(lab)																# Has user confirm that information was entered properly
	labdb.addLab(lab)																# Commites changes to the database
	if labdb.validateFull(error_log=False):											# Checks that the lab database is still valid and error free
		if not updatedVersion == False:
			moveVersionDir(updatedVersion,root)												# Adds the updated version of pdf to lab folder
			addSupportFolder(updatedVersion,root)												# Updates the pdf referenced in database
		labdb.save(destXML, ignore_validation=validate, error_log=False)				# Saves the updated labDB.xml database
	else:
		printR("Error: XML Object is Invalid. Check error logs for details.")
		labdb.validateFull(error_log=True)		

'''prints metadata for specified lab'''
if args.print:
	printB("Printing lab metadata.")
	lab = getLabObject()					# Generates a lab object from an existing entry in database
	displayLabItem(lab)							# Prints general information about lab
	printVersions(lab.versions)					# Prints information on versions currently in database

if args.repwheel:
	printB("Updating labDB.xml in data folder.")    
	files = get_db_files()
	increment_files(list(reversed(files)))

'''confirms that the script has ended properly'''
printB("...and then there will be cake!")
