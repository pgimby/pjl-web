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


inputDir = "/usr/local/master/labs/equipimg"
slugRoot = "/home/pgimby/pjl-web"
equipDir = "/staffresources/equipment/equipimg"
db = EquipDB("../../data/equipmentDB.xml")

# def imgInfo(inputDir):
#   	equipInfos = {}
#   	for root, dirs, files in os.walk(inputDir):
#   		for i in files:
#   			imgPath = "/".join([root, i])
#   			equID = i
#   			equipInfos[equID] = imgPath
# 	#return equipInfos

# def outInfo(name, equipRoot):
# 	eqID = str(name)[:4]
# 	webPath = equipRoot + "/" + name
# 	return eqID,webPath


host="slug"
myhost = os.uname()[1]
if host != myhost:
	print("This script is designed to be run on " + host + " only")
	print("Exiting")
	exit()


#equipInfos = imgInfo(inputDir)
 #for i in equipInfos:
 #	eqID,webPath = outInfo(i,equipDir)
 #	equip = db.getItem(idnum=eqID)
 #	equip.thumbnail = webPath
 #	db.addItem(equip)




#db.save("../updatedequipmentDB.xml", ignore_validation=False, error_log=True)

	#print(eqID + " " + webPath)
	#print(i + " " +equipInfos[i])

#	ID = getEquipID(i)

