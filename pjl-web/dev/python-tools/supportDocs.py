#!/usr/bin/python3
#
# Script to add Support Documents to the labDB.xml

# This script searches through the repository for any folder called Support_Docs. 
# It the grabs any file in those folder and posts it in the labDB.xml file that is 
# associated with that file. The name given to the file is based on the name of the
# original file, but it is truncated to avoid posting files with exeptionally long
# file names.

import xml.etree.ElementTree as ET
import os
from pjlDB import *

db = LabDB("../labDB.xml")
rootDir = "/usr/local/master/labs/repository"
webRoot = "/data/repository/"
nameDir = "Support_Docs"


'''Returns the path name of any support document folder'''
def findSupportDirs(rootDir,nameDir):
	supportDirs = []
	for root, dirs, files in os.walk(rootDir):
		for i in dirs:
			if nameDir in i:
				supportDir = '/'.join([root, i])
				supportDirs.append(supportDir)
	return supportDirs

'''Returns lab ID'''
def findID(lab):
	labID = lab.split("/")[6].split("-")[0]
	return labID

'''Returns a list of paths to support docs'''
def findSupportPaths(lab):
	supportPaths = []
	for root, dirs, files in os.walk(lab):
		for i in files:
			supportPath = "/".join([root, i])
			supportPaths.append(supportPath)
	return supportPaths

'''Constructs a dictionary of lists all the {name: paths:} of support docs '''
def makeDict(supportPaths,webRoot):
	supportDicts = []
	for i in supportPaths:
		dictName = {}
		docName = makeDocName(i)
		docPath = makeDocWebPath(i,webRoot)
		dictName["path"] = docPath
		dictName["name"] = docName
		supportDicts.append(dictName)
	return supportDicts

'''Gets path of doc for web xml'''
def makeDocWebPath(path,webRoot):
	path = "/".join(path.split("/")[6:])
	path = webRoot + path
	return path

'''Makes a name for each doc that is less then x characters'''
def makeDocName(supportPath):
	fullPathName = supportPath.split("/")[-1]
	ext = fullPathName.split(".")[-1]
	fullName = fullPathName.split(".")[:-1]
	maxLength = 20
	if len(fullName[0]) > maxLength:
		name = str(fullName)[2:maxLength] + "..." + ext
	elif len(fullName[0]) == maxLength:
		name = str(fullName[0]) + "." + ext
	elif len(fullName[0]) < maxLength:
		name = str(fullName[0]) + "." + ext
	return name


supportDirs = findSupportDirs(rootDir,nameDir)
for i in supportDirs:
	labID = findID(i)
	supportPaths = findSupportPaths(i)
	supportDicts = makeDict(supportPaths,webRoot)
	lab = db.getLab(labID)
	lab.support_docs = supportDicts
	db.addLab(lab)
db.save("../../dev/updatedlabDB.xml", ignore_validation=False)
print("...and then there will be cake")