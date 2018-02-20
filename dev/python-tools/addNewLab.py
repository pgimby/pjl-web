#!/usr/bin/python3

'''Adds version from a csv file and adds them to the repository'''

from pjlDB import *
import csv
import argparse
import os
import xml.etree.ElementTree as ET

eqdb = EquipDB("/home/pgimby/pjl-web/dev/equipmentDB.xml")
labdb = LabDB("/home/pgimby/pjl-web/data/labDB.xml")
rootDr = "/usr/local/master/labs"
webRoot = "/home/pgimby/pjl-web"
repository = rootDr + "/repository"
newLabDr = rootDr + "/under-construction/newlabs/"
infoFile = "info.csv"
semesterDict = {"Winter": "WI", "Spring": "SP", "Summer": "SU", "Fall": "FA" }





class NewLabInfo():

	def __init__(self,infoDr,labID):
		self.infoDr = infoDr
		self.id_num = labID.id_num
		print(self.infoDr)
		self.labFolder = self.id_num + "-" + infoDr.split("/")[-2]
		self.labtree = ET.parse(webRoot + "/data/labDB.xml")
		self.labroot = self.labtree.getroot()
		self.rawInfo = self._collectInfo(infoDr,infoFile)
		self.name = " ".join(self.rawInfo["name"][0].split("-"))
		self.name = " ".join(self.name.split())
		self.lab_type = self.rawInfo["type"][0].capitalize()
		self.disciplines = self.rawInfo.get("disciplines","")
		self.topics = self.rawInfo.get("topics")
		self.equipment = self.equipInfo()
		self.software = self.rawInfo.get("software","")
		self.semester = self.rawInfo["semester"][0].capitalize()
		self.year = self.rawInfo["year"][0]
		self.course = self.rawInfo["course"][0]
		self.versionDr = self.id_num + "-PHYS" + self.course + semesterDict[self.semester] + self.year
		self.versions = self.makeVersionDict()
	'''Turns data in info.csv into dictionary'''
	def _collectInfo(self,dr,filename):
		self.infoPath = dr + filename
		#print("A " + self.infoPath)
		if os.path.isfile(self.infoPath):
			csvContents = self._convertCSVtoDic()
		else:
			print(i + " is missing the configuration file info.csv")
			print("exiting...")
			exit()
		return csvContents

	def _convertCSVtoDic(self):
		labInfoDict = {}
		with open(self.infoPath, "r") as o:
			labInfo = csv.reader(o)
			for i in labInfo:
				category = i[0].lower()
				contents = i[1:]
				labInfoDict[category] = contents
		return labInfoDict

	def makeVersionDict(self):
		versions = []
		version = {}
		labFolderInfo = repository + "/" + self.labFolder + "/" + self.versionDr
		version["path"] = "/data/repository/" + self.labFolder + "/" + self.versionDr + "/" + self.rawInfo["pdf"][0]
		version["semester"] = self.semester
		version["course"] = "PHYS " + self.course
		version["year"] = self.year
		directory = "/data/repository/" + self.labFolder + "/" + self.versionDr
		version["directory"] = directory
		versions.append(version)
		print(versions)
		return versions


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
					#if eqdb._idExistsAlready(altid) == True:
					itemDict["alt-name"] = eqdb.getItem(altid).name
					itemDict["alt-id"] = altid
					#else:
					#	print("equipment item " + altid + " is invalid.")
					#	print("exiting...")
					#	exit()
				else:
					itemDict["alt-name"] = ""
					itemDict["alt-id"] = ""
			equipItems.append(itemDict)
		return equipItems



'''Returns absolute path names of folder(s) of labs to add'''
def getAbsDrs(parentDr):
	lst = []
	drs = os.listdir(parentDr)
	for i in drs:
			lst.append(parentDr + i)
	print(lst)
	return lst

#def getAbs()


def addLabToXML(labInfo,newlab,labdb):
	newlab.name = labInfo.name
	newlab.lab_type = labInfo.lab_type
	newlab.disciplines = labInfo.disciplines
	newlab.topics = labInfo.topics
	newlab.versions = labInfo.versions
	newlab.equipment = labInfo.equipment
	labdb.addLab(newlab)


def oneAtATime(labDr):
	print(labDr)


parser = argparse.ArgumentParser()
parser.add_argument('source', nargs='+', help='enter path of lab folder(s) to add.  Ex addNewLab /path/to/folder1 ~/path/to/folder2')
args = parser.parse_args()
labDr = args.source

for i in labDr:
	newLab = labdb.newLab(labdb.new_id)
	labInfo = NewLabInfo(i,newLab)
	addLabToXML(labInfo,newLab,labdb)

labdb.save("../../dev/test.xml", ignore_validation=False)