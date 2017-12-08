#!/usr/bin/python3

#import packages
from pjlDB import *


db = equipDB("../../data/equipmentDB.xml")

db.validateFull(error_log=False)
