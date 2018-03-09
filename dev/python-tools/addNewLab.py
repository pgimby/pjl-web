#!/usr/bin/python3

'''Adds version from a csv file and adds them to the repository'''

from pjlDB import *
import csv, argparse, os
import xml.etree.ElementTree as ET

'''Folders and file used.'''
root = "/usr/local/master"
eqdb = EquipDB(root + "/pjl-web/data/equipmentDB.xml")
labdb = LabDB(root + "/pjl-web/data/labDB.xml")
infoFile = "info.csv"
semesterDict = {"Winter": "WI", "Spring": "SP", "Summer": "SU", "Fall": "FA" }


'''Collects information on the lab to add, and formats it to be used by pjlDB.py'''
class NewLabInfo():


	def __init__(self,labSource,newLabObj):
		self.id_num = newLabObj.id_num
		self.labFolder = self.id_num + "-" + labSource.split("/")[-2]
		self.rawInfo = self._collectInfo(labSource,infoFile)
		self.name = " ".join(self.rawInfo["name"][0].split("-"))
		self.name = " ".join(self.name.split())
		self.lab_type = self.rawInfo["type"][0].capitalize()
		self.equipment = self.equipInfo()
		self.software = self.rawInfo.get("software","")
		self.semester = self.rawInfo["semester"][0].capitalize()
		self.semester = " ".join(self.semester.split())
		self.year = self.rawInfo["year"][0]
		self.year = " ".join(self.year.split())
		self.course = self.rawInfo["course"][0]
		self.versionDr = self.id_num + "-PHYS" + self.course + semesterDict[self.semester] + self.year
		self.versions = self.makeVersionDict()
		self.topics = self.optionalTag("topics")
		self.disciplines = self.optionalTag("disciplines")


	def optionalTag(self,typ):
		checkForNone = self.rawInfo.get(typ)
		if checkForNone != None:
			if not len(checkForNone) == 0:
				if not checkForNone[0] == '':
					checkForNone = [i.strip(' ') for i in checkForNone]
					for i in checkForNone:
						if i == '':
							checkForNone.remove(i)
					return checkForNone
				else:
					return []
			else:
				return []
		else:
			return []

	
	'''Checks to see if info.csv file exists'''
	def _collectInfo(self,dr,filename):
		self.infoPath = dr + filename
		if os.path.isfile(self.infoPath):
			csvContents = self._convertCSVtoDic()
		else:
			print(i + " is missing the configuration file info.csv")
			print("exiting...")
			exit()
		return csvContents


	'''Turns data in info.csv into dictionary'''
	def _convertCSVtoDic(self):
		labInfoDict = {}
		with open(self.infoPath, "r") as o:
			labInfo = csv.reader(o)
			for i in labInfo:
				category = i[0].lower()
				contents = i[1:]
				labInfoDict[category] = contents
		return labInfoDict


	'''Makes a dictionary of version to feed into pjlDB.py'''
	def makeVersionDict(self):
		versions = []
		version = {}
		version["path"] = "/data/repository/" + self.labFolder + "/" + self.versionDr \
		+ "/" + self.rawInfo["pdf"][0]
		version["semester"] = self.semester
		version["course"] = "PHYS " + self.course
		version["year"] = self.year
		directory = "/data/repository/" + self.labFolder + "/" + self.versionDr
		version["directory"] = directory
		versions.append(version)
		return versions


	'''Finds the name of equipment from inventory, and returns list'''
	def equipInfo(self):
		equipItems = []
		equipRawInfo = self.rawInfo["equipment"]
		for i in equipRawInfo:
			itemDict = {}
			eqid = i.split("-")[0].strip()
			if eqdb._idExistsAlready(eqid) == True:
				itemDict["id"] = eqid
				itemDict["name"] = eqdb.getItem(eqid).name
				itemDict["amount"] = i.split("(")[1].split(")")[0]
				if "[" in i:
					altid = (i.split("[")[1].split("]")[0])
					itemDict["alt-name"] = eqdb.getItem(altid).name
					itemDict["alt-id"] = altid
				else:
					itemDict["alt-name"] = ""
					itemDict["alt-id"] = ""
			equipItems.append(itemDict)
		return equipItems


def emptyList(tagInfo):
	for i in tagInfo:
		if i == "":
			tagInfo.remove(i)
	if len(tagInfo) == 0:
		return True
	else:
		return False


'''Adds information to new xml entry'''
def addLabToXML(labInfo,newlab,labdb):
	newlab.name = labInfo.name
	newlab.lab_type = labInfo.lab_type
	#if not emptyList(labInfo.disciplines):
	newlab.disciplines = labInfo.disciplines
	#if not emptyList(labInfo.topics):
	newlab.topics = labInfo.topics
	newlab.equipment = labInfo.equipment
	newlab.software = labInfo.software
	newlab.versions = labInfo.versions
	if testing == True:
		print(newlab.name)
		print(newlab.lab_type)
		print(newlab.disciplines)
		print(newlab.topics)
		print(newlab.equipment)
		print(newlab.software)
		print(newlab.versions)

	labdb.addLab(newlab)
'''Collects info on the source and destination directories of new lab'''
def getDrMoveInfo(labInfo,repository):
	drInfo = {}
	drInfo["originDr"] = i
	drInfo["labDr"] = root + "/labs/repository/" + labInfo.labFolder
	drInfo["versionDr"] = drInfo["labDr"] +"/" + labInfo.versionDr#[0]["directory"]
	return drInfo

def makeDr(newDr):
	print("newDr is " + newDr)
	if not os.path.isdir(newDr):
		os.system("mkdir " + newDr)
	else: 
		print("Lab folder " + newDr + " Already Exists.")
		print("If this is a new version of an existing lab try running addVersions.py")
		print("Exiting...")
		exit()

def checkForDr(existingDr):
	if not os.path.isdir(existingDr):
		print("Source folder " + existingDr + " Does Not Exists. Exiting ...")
		exit()
	else:
		return True

def moveDr(origin,destination):
	if checkForDr(origin) and checkForDr("/".join(destination.split("/")[:-1])):
		os.system("mv " + origin + " " + destination)


'''Reads in location of folder for lab to add'''
parser = argparse.ArgumentParser()
parser.add_argument('source', nargs='+', help='enter path of lab folder(s) to add. \
	Ex addNewLab /path/to/folder1 ~/path/to/folder2')
parser.add_argument('-t', '--test', help='test adding to xml without moving folders', action='store_true')
args = parser.parse_args()
labDr = args.source
testing = args.test

'''Adds new lab to labDB.xml'''
newDrInfo = []
for i in labDr:
	newLab = labdb.newLab(labdb.new_id)
	labInfo = NewLabInfo(i,newLab)
	addLabToXML(labInfo,newLab,labdb)
	newDrInfo.append(getDrMoveInfo(labInfo,root))
labdb.save(root + "/pjl-web/dev/labDB.xml", ignore_validation=False)
valid = labdb.validateFull()

if testing != True:
	if valid == True:
		for i in range(0,len(labDr)):
			makeDr(newDrInfo[i]["labDr"])
			moveDr(newDrInfo[i]["originDr"],newDrInfo[i]["versionDr"])
			origin = newDrInfo[i]["versionDr"] + "/" + "Support_Docs"
			destination = newDrInfo[i]["labDr"]
			moveDr(origin,destination)
	else:
		print("something went wrong. Exiting...")
		exit()

print("...and then there will be cake")