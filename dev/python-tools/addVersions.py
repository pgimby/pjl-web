#!/usr/bin/python3

'''This Fails and im not sure why'''

from pjlDB import *
import csv


with open("lst.csv", 'r') as o:
	reader = csv.reader(o)
	new_versions = list(reader)
#new_versions = [['0102', '/data/repository/0102-AC-Circuits-and-Voltage-Dividers/0102-PHYS497WI2018/AC-Circuits-and-Voltage-Dividers-WI2018.pdf ', 'Winter', '2018', 'PHYS 497']]

	db = LabDB("../../data/labDB.xml")

	for version in new_versions:
		lab = db.getLab(idnum=version[0])
		new_version = {"path": version[1],"semester": version[2],"year": version[3],"course": version[4],"directory": "/".join(version[1].split("/")[:-1])}
		lab.addVersion(new_version)
		db.addLab(lab)


#db.save("../updatedlabDB.xml", ignore_validation=False, error_log=False)
db.save("../labDB.xml", ignore_validation=False, error_log=False)