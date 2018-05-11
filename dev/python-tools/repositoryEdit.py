#!/usr/bin/python3

'''Adds version from a csv file and adds them to the repository'''

import pjlDB
import csv, os, argparse
version = "1.0"


'''Paths for xml files'''
root = "/usr/local/master/pjl-web"
#labdbDev = root + "/dev/testlabDB.xml"
eqdbDev = root + "/dev/equipmentDB.xml"
labdbDev = root + "/dev/labDB.xml"
eqdbData = root + "/data/equipmentDB.xml"
labdbData = root + "/data/labDB.xml"
#destXML = "/dev/testlabDB.xml"


def testHost(host):
    thishost = os.uname()[1]
    if not host == thishost:
        print("This script is designed to be run on " + thishost + " only. Exiting...")
        gracefullExit(mountInfo)


'''Checks that the development version of the db is as new or newer that the live one'''
def checkTimeStamp(dev,data):
	if os.path.getmtime(data) <= os.path.getmtime(dev):
		return True
	else:
		return False


#Functions used to add a new version entry to the repository xml


'''creats a new empty lab object'''
def getLabObject(labdb):
	print("Adding new version of existing lab.")
	validID = False
	while not validID:
		idnum = input("Enter lab ID number for new version: ")
		if len(idnum) == 4 and idnum.isdigit() == True:
			try:
				lab = labdb.getLab(idnum)
				validID = True
			except pjlDB.IDDoesNotExist: ### not working properly
				print("Message")
		else:
			print("ID formate in not valid. Valid IDs are of the form ####. Please try again")
			validID = False
	return lab


'''collects information about new version of an existing lab'''
def getVersionInfo(lab,validCourses,validSemesters,semesterKeys, testMode):
	new_version = {}
	new_version["originalDir"] = originalDir()
	new_version["course"] = validCourse(validCourses)
	new_version["semester"] = validSemester(validSemesters) 
	new_version["year"] = validYear()
	new_version["directory"] = validDirectory(new_version,lab,semesterKeys)
	new_version["path"] = validPath(new_version)
	return new_version


'''get path of lab documents to add, and confirm they exist and are in the right format'''
def originalDir():
		validDir = False
		while not validDir:
			originalDir = input("Enter absolute path for directory containing new version: ")
			if not originalDir.split("/")[-1] == "":
				originalDir = originalDir + "/"
			print(originalDir)
			if os.path.isdir(originalDir):
				validDir = True
			else:
				print("Directory " + originalDir + " does not exist. Please try again.")
		return originalDir


'''gets course number, and makes sure it is a valid course'''
def validCourse(validCourses):
	validCourse = False
	while not validCourse:
		courseNum = str(input("Enter course number: "))
		for i in validCourses:
			if courseNum == i:
				course = "PHYS " + courseNum
				validCourse = True
		if not validCourse:
			print("Invalid Course number")
			print("Valid courses are...")
			for i in validCourses:
				print(i)
	return course


'''gets semester, and makes sure it is a valid semester'''
def validSemester(validSemesters):
	validSemester = False
	while not validSemester:
		semesterName = str(input("Enter Semester: ")).capitalize()
		for i in validSemesters:
			if semesterName == i:
				validSemester = True
		if not validSemester:
			print("Invalid semester")
			print("Valid semesters are...")
			for i in validSemesters:
				print(i)
	return semesterName


'''gets year, and makes sure it is a valid year'''
def validYear():
	validYear = False
	while not validYear:
		year = input("Enter year: ")
		if len(year) == 4 and year.isdigit() == True:
			validYear = True
		else:
			print("Year is invalid.")
	return year


'''determinds the name of the new directory for the new version'''
def validDirectory(new_version,lab,semesterKeys):
	samplePath = lab.versions[0]["directory"]
	path = "/".join(samplePath.split("/")[:-1])
	semester = semesterKeys[new_version["semester"]]
	courseNum = new_version["course"].split(" ")[-1]
	year = new_version["year"]
	directory = path + "/" + lab.id_num + "-PHYS" + courseNum + semester + year + "/"
	return directory


'''get name of pdf file to display, and check that it exists in source directory'''
def validPath(new_version):
	validPath = False
	while not validPath:
		pdfName = input("Enter the name of the lab pdf: ")
		if os.path.isfile(new_version["originalDir"] + pdfName):
			validPath = True	
			path = new_version["directory"] + pdfName
		else:
			print("PDF does not exist. Please try again.")
	return path


'''ask user to confirm that the information given is correct'''
def confirmEntry(new_version):
	print("")
	print("Please confirm that the information entered is correct")
	print("original Directory: " + new_version["originalDir"])
	print("course: " + new_version["course"])
	print("semester: " + new_version["semester"])
	print("year: " + new_version["year"])
	print("directory: " + new_version["directory"])
	print("path: " + new_version["path"])
	if not input("Is this information correct? N/y: ") == "y":
		print("exiting...")
		exit()

'''adds updated xml entry to labdb.xml and saves it'''
def validDB(info,lab,labdb):
	lab.addVersion(info)
	valid = labdb.validateFull()
	if valid:
		return valid
	else:
		return False


#Functions for moving directory into repository

'''Checks if the directory already exists'''
def validDir(info,root):
	versionDir = root + info["directory"]
	if not os.path.isdir(versionDir):
		return True
	else: 
		print("Lab folder " + versionDir + " Already Exists.")
		print("Exiting...")
		return False

'''Moves source directory to repository'''
def moveVersionDir(info,root):
	versionDir = root + info["directory"]
	if not os.path.isdir(versionDir):
		#os.system("echo cp -a " + info["originalDir"] + " " + versionDir)
		os.system("mkdir " + versionDir)
		os.system("rsync -avz --exclude Support_Docs " + info["originalDir"] + " " + versionDir)
	else: 
		print("Lab folder " + versionDir + " Already Exists.")
		print("Exiting...")
		exit()


#Functions for updating Support_Docs

'''Create a Support_Doc folder if one does not exist''' 
def addSupportFolder(info):
	versionDir = root + info["directory"]
	labFolder = "/".join(versionDir.split("/")[:-2])
	supportFolder = labFolder + "/Support_Docs"
	if not os.path.isdir(supportFolder):
		print("Support_Docs Folder does not exist. Adding new folder " + supportFolder)
		os.system("mkdir " + supportFolder)
	if os.path.isdir(labFolder):
		updateSupportFolder(info,supportFolder,labFolder)
	else:
		print("Something when wrong. Exiting...")
		exit()

'''syncs any files in Support_Docs with those in repository support_docs folder'''
def updateSupportFolder(info,supportFolder,labFolder):
	supportOrigin = info["originalDir"] + "Support_Docs"
	if os.path.isdir(supportOrigin):
		os.system("rsync -avz " + supportOrigin + "/ " + supportFolder)


#Functions for adding a new lab




#Main Script


'''Create pjlDB object of each of the relevent xml files'''
eqdb = pjlDB.EquipDB(eqdbDev)
labdb = pjlDB.LabDB(labdbDev)




'''Define user options'''
parser = argparse.ArgumentParser()
parser.add_argument('-n', '--new', help='Used this option to add a new lab. Information regarding the new lab will be requested by the script.".', action='store_true')
parser.add_argument('-a', '--add', help='Used this option to add a new version to an existing lab. Information regarding the new version will be requested by the script.".', action='store_true')
#parser.add_argument('-d', '--delete', help='enter id number of the piece of equipment to delete. Ex 0001')
#parser.add_argument('-m', '--nomove', help='Used this option to add a new lab without moving the folder to the repository.".', action='store_true')
parser.add_argument('-t', '--test', help='debug mode', action='store_true')
parser.add_argument('-v', '--version', help='Print current verion of script', action='store_true')
args = parser.parse_args()
testMode = args.test


'''List of valid courses'''
validCourses = ["211", "223", "227", "255", "259", "323", "325", "341", "365", "369", "375", "397", "497"]
validSemesters = ["Winter", "Spring", "Summer", "Fall"]
semesterKeys = {"Winter": "WI", "Spring": "SP", "Summer": "SU", "Fall": "FA"}

'''Confirm that this script won't accidently run on the wrong machine'''
testHost(devhost)


'''prints version'''
if args.version:
	print("Version " + version)
	exit()


'''set a test mode for script'''
if args.test:
	print("Running in test mode.")


'''Checks that the development version of both key DBs are new or as new as the live versions.'''
if not checkTimeStamp(eqdbDev,eqdbData) or not checkTimeStamp(labdbDev,labdbData):
	if not checkTimeStamp(eqdbDev,eqdbData):
		print("Equipment development database is out of synce with the live version. Please update the development version before continuing.")
	if not checkTimeStamp(labdbDev,labdbData):
		print("Repository development database is out of synce with the live version. Please update the development version before continuing.")
	print("Exiting...")
	exit()


'''add a new version of an existing lab'''
if args.add:
	lab = getLabObject(labdb)
	versionInfo = getVersionInfo(lab,validCourses,validSemesters,semesterKeys,testMode)
	confirmEntry(versionInfo)
	if validDB(versionInfo,lab,labdb) and validDir(versionInfo,root):
		labdb.save("/usr/local/master/pjl-web/dev/labDB.xml", ignore_validation=False, error_log=True)
		moveVersionDir(versionInfo,root)
		addSupportFolder(versionInfo)
	else:
		print("something when wrong")
		exit()

'''add a new lab'''
if args.new:
	lab = labdb.newLab(labdb.new_id)
	print(lab.id_num)
	print("Adding a brand new lab")

'''confirms that the script has ended properly'''
print("...and then there will be cake")

