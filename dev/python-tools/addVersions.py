#!/usr/bin/python3

'''This Fails and im not sure why'''

from pjlDB import *
import csv


new_versions = [[0102, '/data/repository/0102-AC-Circuits-and-Voltage-Dividers/0102-PHYS497WI2018/AC-Circuits-and-Voltage-Dividers-WI2018.pdf ', 'Winter', '2018', 'PHYS 497']]

db = LabDB("../../data/labDB.xml")

for version in new_versions:

	#print(version)
	lab = db.getLab(idnum=version[0])
	print(version[0])
	new_version = {"path": version[1],"semester": version[2],"year": version[3],"course": version[4],"directory": "/".join(version[1].split("/")[:-1])}
	print(new_version)
	#for i in new_version:
	#	print(i)

	#print(new_version)
	lab.addVersion(new_version)
	#db.addLab(lab)

#db.save("/dev/updatedlabDB.xml", ignore_validation=False, error_log=True)

