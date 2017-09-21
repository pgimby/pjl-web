#!/usr/bin/python3

import pjlDB as pd
import xml.etree.ElementTree as ET




#opening up a file holding new versions to add in rows with accompanying labIDs

new = []
with open("../data.txt", "r") as f:
    for line in f.readlines():
        l = line.split(",")
        new.append({"id":l[0],"path":l[1],"sem":l[2],"yr":l[3],"crs":l[4],"dir":l[5]})

#store the database and update the version list for each associated lab

tree = ET.parse("../labDB.xml")
db = pd.labDB(tree)

for n in new:
    lab = db.getLab(idnum=n["id"])
    versions = lab.versions
    new_version = {"path": n["path"],
                   "course": n["crs"],
                   "year": n["yr"],
                   "semester": n["sem"],
                   "directory": n["dir"]}
    versions.append(new_version)
    lab.versions = versions

    db.addLab(lab)


db.save("../labDB.xml", ignore_validation=True)
