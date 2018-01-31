#!/usr/bin/python3
#
# Script to add Equipment Images  to the equipmentDB.xml

# This script get all of the files in staffresources/equipment/equipimg folder.
# Each image is named with the pattern ####img.jpg where #### is the equipment ID #.
# The path of each image present will over write the existing path listed in the
# equipmentDB.xml file. There should be only one image per equipment ID #

import xml.etree.ElementTree as ET
import os
from pjlDB import *


inputDir = "/usr/local/master/labs/equipimg"
slugRoot = "/home/pgimby/pjl-web"
equipDir = "/staffresources/equipment/equipimg"
db = EquipDB("../equipmentDB.xml")

def imgInfo(inputDir):
	equipInfos = {}
	for root, dirs, files in os.walk(inputDir):
		for i in files:
			imgPath = "/".join([root, i])
			equID = i
			equipInfos[equID] = imgPath
	return equipInfos

def outInfo(name, equipRoot):
	eqID = str(name)[:4]
	webPath = equipRoot + "/" + name
	return eqID,webPath


'''checks to make sure that this script is being run on the right computer'''
host="slug"
myhost = os.uname()[1]
if host != myhost:
	print("This script is designed to be run on " + host + " only")
	print("Exiting")
	exit()


equipInfos = imgInfo(inputDir)
for i in equipInfos:
	eqID,webPath = outInfo(i,equipDir)
	equip = db.getItem(idnum=eqID)
	equip.thumbnail = webPath
	db.addItem(equip)

db.save("../updatedequipmentDB.xml", ignore_validation=False, error_log=True)
print("...and then there will be cake")