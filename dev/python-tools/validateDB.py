#!/usr/bin/python3

#import packages
from pjlDB import *


db = EquipDB("../../data/equipmentDB.xml")

db.validateFull(error_log=False)


db = LabDB("../../data/labDB.xml")

db.validateFull(error_log=False)

