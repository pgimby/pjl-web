#!/usr/bin/python3
#
# Script to add Equipment Manual PDFs to the equipmentDB.xml

# This script get all of the manuals in staffresources/equipment/equipman folder.
# Each manual is named with the pattern ####man[i].jpg where #### is the equipment ID #,
# [i] is an integer used for cases where more that one manual may exist.
# The path of each manual present will over write the existing path listed in the
# equipmentDB.xml file. There can be multiple manuals per equipment ID #

import xml.etree.ElementTree as ET
import os
from pjlDB import *

'''Defines important files and directories'''
inputDir = "/usr/local/master/labs/equipman"
slugRoot = "/home/pgimby/pjl-web"
equipDir = "/staffresources/equipment/equipman"
db = EquipDB("../equipmentDB.xml")



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





'''Checks to make sure that this script is being run on the right computer'''
host="slug"
myhost = os.uname()[1]
if host != myhost:
	print("This script is designed to be run on " + host + " only")
	print("Exiting")
	exit()


'''Main Body of Script'''
listOfIDs = equipWithMan(inputDir)
for i in listOfIDs:
	equipManuals,eqID = manInfo(i,inputDir,equipDir)
	equip = db.getItem(idnum=eqID)
	equip.documents = equipManuals
	db.addItem(equip)
db.save("../updatedequipmentDB.xml", ignore_validation=False, error_log=True)

print("...and then there will be cake")