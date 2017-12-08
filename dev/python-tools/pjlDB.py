#!/usr/bin/python3

#import packages
import xml.etree.ElementTree as ET
import re
import datetime







def isValidID(idnum):
    try:
        int(idnum)
    except:
        return False
    if isinstance(idnum, str) and len(idnum) == 4:
        return True
    else:
        return False



def getTopics():

    """returns a list of strings"""

    with open("../../README.md", "r") as f:
        s = f.read()
        m = re.search(r"<!---start topics-->\n([.\s\S]*)\n<!---end topics-->", s)
    lst = [i.strip() for i in m.group(0).split("\n")[1:-1]]
    return lst



def getDisciplines():

    """returns a list of strings"""

    with open("../../README.md", "r") as f:
        s = f.read()
        m = re.search(r"<!---start disciplines-->\n([.\s\S]*)\n<!---end disciplines-->", s)
    lst = [i.strip() for i in m.group(0).split("\n")[1:-1]]
    return lst











class equipDB():

    """
    For modifying and appending to the equipment database XML file
    """

    def __init__(self, pathtoXML):
        self.tree = ET.parse(pathtoXML)
        self.root = self.tree.getroot()
        self.equipment = []
        self._makeEquipment()
        self.new_id = self._getNextAvailableID()
        self.length = len(self.equipment)



    def log_file_object(self):
        date = datetime.datetime.today()
        date = str(date.year) + "-" + str(date.month) + "-" + \
               str(date.day) + "_" + str(date.hour) + "." + \
               str(date.minute) + "." + str(date.second)
        filename = "error_" + date + ".log"
        return open(filename, "w")



    def validateFull(self, error_log=False):
        if error_log:
            f = self.log_file_object()
            tests = [self.noDuplicateIDs(log_file=f),
                 self.hasValidPathRoots(log_file=f)]
            f.close()
        else:
            f = None
            tests = [self.noDuplicateIDs(log_file=f),
                 self.hasValidPathRoots(log_file=f)]
        if f:
            f.close()
        if all(tests):
            return True
        else:
            return False



    def noDuplicateIDs(self, log_file=None):
        error_log = []
        good = True
        seen = set()
        for item in self.equipment:
            if item.id_num not in seen:
                seen.add(item.id_num)
            else:
                good = False
                error_log.append("Equipment item \"" + item.id_num +
                                 "\" is a duplicate of another item in the database")
        if good == False:
            if log_file:
                [log_file.write(i + "\n") for i in error_log]
            else:
                [print(i) for i in error_log]
        return good






    def hasValidPathRoots(self, log_file=None):
        error_log = []
        good = True
        valid_path_prefix = "/equipment/docs/"
        for item in self.equipment:
            for document in item.documents:
                if not document["location"].startswith(valid_path_prefix):
                    good = False
                    error_log.append("Bad version path \"" +
                                     document["location"] + "\" in lab " +
                                     item.id_num + " (" +
                                     item.name + ")")
        if good == False:
            if log_file:
                [log_file.write(i + "\n") for i in error_log]
            else:
                [print(i) for i in error_log]
        return good



    def getItem(self, idnum=None, name=None):
        if not idnum and not name:
            return None
        if idnum:
            try:
                idnum = str(idnum).zfill(4)
                for item in self.equipment:
                    if item.id_num == idnum:
                        return item
                raise Exception("Equipment id \"" + idnum + "\" doesn't exist")
            except Exception as e:
                raise e
        else:
            try:
                name = str(name)
                for item in self.equipment:
                    if name == item.name:
                        return item
                raise Exception("Equipment name \"" + name + "\" doesn't exist")
            except Exception as e:
                raise e



    def deleteItem(self, idnum=None, name=None):
        if not idnum and not name:
            return None
        if idnum and isValidID(idnum):
            try:
                for item in self.equipment:
                    if item.id_num == idnum:
                        self.equipment.remove(item)
                        self._updateXML()
                        self.length = len(self.equipment)
                        self.new_id = self._getNextAvailableID()
                        return True
                raise Exception("Equipment id \"" + idnum + "\" doesn't exist")
            except Exception as e:
                raise e
        else:
            try:
                name = str(name)
                for item in self.equipment:
                    if name == item.name:
                        self.equipment.remove(item)
                        self._updateXML()
                        self.length = len(self.equipment)
                        self.new_id = self._getNextAvailableID()
                        return True
                raise Exception("Equipment name \"" + name + "\" doesn't exist")
            except Exception as e:
                raise e



    def newItem(self, idn):
        if isValidID(idn) and not self._idExistsAlready(idn):
            return _equipmentItem(idnum=idn)
        else:
            raise Exception("Invalid lab ID number: IDs must be number strings of length 4 and mustn't exist already in the tree")



    def addItem(self, equipitem):
        if not isinstance(equipitem, _equipmentItem):
            raise TypeError("Argument passed to equipDB.addItem was not an _equipItem object")
        if equipitem.id_num in [item.id_num for item in self.equipment]:
            tmp = [equipitem if equipitem.id_num == item.id_num else item for item in self.equipment]
            self.equipment = tmp[:]
            self._updateXML()
            self.length = len(self.root)
            self.new_id = self._getNextAvailableID()
        else:
            self.equipment.append(equipitem)
            self.root.append(self._labItemToXMLNode(equipitem))
            self._updateXML()
            self.length = len(self.root)
            self.new_id = self._getNextAvailableID()



    def save(self, filename, ignore_validation=False, error_log=False):
        if not isinstance(filename, str):
            raise TypeError("Argument of equipDB.save must be string")
        if ignore_validation:
            self.tree.write(filename, encoding="UTF-8")
            print("XML object not validated and written to " + filename)
            return True
        elif not ignore_validation and self.validateFull(error_log=error_log):
            self.tree.write(filename, encoding="UTF-8")
            print("XML object successfully validated and written to " + filename)
            return True
        else:
            print("XML object not valid\nXML not saved to " + filename)
            return False



    def _makeEquipment(self):
        for child in self.root:
            self.equipment.append(_equipmentItem(item=child))



    def _getNextAvailableID(self):
        ids = set()
        for item in self.equipment:
            ids.add(item.id_num)
        for i in range(1,10000):
            if str(i).zfill(4) not in ids:
                return str(i).zfill(4)



    def _itemExistsByName(self, name):
        for item in self.equipment:
            if name == item.name:
                return True



    def _updateXML(self):
        self.root.clear()
        for item in self.equipment:
            self.root.append(self._equipItemToXMLNode(item))



    def _idExistsAlready(self, idnum):
        for item in self.equipment:
            if item.id_num == idnum:
                return True



    def _equipItemToXMLNode(equipitem):
        if equipitem.id_num:
            item = ET.Element("Item", {"id": equipitem.id_num})
            name = ET.SubElement(item, "InventoryName")
            name.text = equipitem.name
            identification = ET.SubElement(item, "Identification")
            manufacturer = ET.SubElement(identification, "Manufacturer")
            manufacturer.text = equipitem.manufacturer
            model = ET.SubElement(identification, "Model")
            model.text = equipitem.model
            kit = ET.SubElement(item, "Kit")
            kit.attrib = {"isKit": "true" if equipitem.is_kit else "false"}
            locations = ET.SubElement(item, "Locations")
            for i in equipitem.locations:
                location = ET.SubElement(locations, "Location")
                room = ET.SubElement(location, "Room")
                room.text = i["room"]
                storage = ET.SubElement(location, "Storage")
                storage.text = i["storage"]
            quantity = ET.SubElement(lab, "Quantity")
            total = ET.SubElement(quantity, "Total")
            total.text = equipitem.quantity["total"]
            service = ET.SubElement(quantity, "InService")
            service.text = equipitem.quantity["service"]
            repair = ET.SubElement(quantity, "UnderRepair")
            repair.text = equipitem.quantity["repair"]
            documents = ET.SubElement(item, "Documents")
            for d in equipitem.documents:
                doc = ET.SubElement(documents, "Document")
                docname = ET.SubElement(doc, "Name")
                docname.text = d.name
                loc = ET.SubElement(doc, "Location")
                loc.text = d.location
            return item
        else:
            raise Exception("Any piece of equipment added to the tree must have, at minimum, an ID number")














class _equipmentItem():

    def __init__(self, item=None, idnum=None):
        if item and isinstance(item, ET.Element):
            self.id_num = item.attrib["id"]
            self.name = item.findtext("InventoryName")
            self.manufacturer = item.findtext(".//Manufacturer")
            self.model = item.findtext(".//Model")
            self.is_kit = True if item.find("Kit").attrib["isKit"] == "true" else False
            self.locations = []
            for loc in item.findall(".//Location"):
                location = {"room": loc.findtext("Room"),
                            "storage": loc.findtext("Storage")}
                self.locations.append(location)
            self.quantity = {"total": item.findtext(".//Total"),
                             "service": item.findtext(".//InService"),
                             "repair": item.findtext(".//UnderRepair")}
            self.documents = []
            for doc in item.findall(".//Document"):
                document = {"name": doc.findtext("Name"), "location": doc.findtext("Location")}
                self.documents.append(document)

        elif not item and isValidID(idnum):
            self.id_num = idnum
            self.name = ""
            self.manufacturer = ""
            self.model = ""
            self.is_kit = False
            self.locations = []
            self.quantity = {"total": "", "service": "", "repair": ""}
            self.documents = []

        else:
            raise Exception("Invalid arguments passed to _equipmentItem: either a valid Item or a valid equipment ID must be passed")





    def addDocument(self, doc):
        if isinstance(dict, doc) and "name" in doc and "location" in doc:
            self.documents.append(doc)
        else:
            raise Exception("Invalid argument passed to _equipmentItem.addDocument: argument must be dictionary with appropriate keys.")



    def addLocation(self, loc):
        if isinstance(dict, loc) and "room" in loc and "storage" in loc:
            self.locations.append(loc)
        else:
            raise Exception("Invalid argument passed to _equipmentItem.addLocation: argument must be dictionary with appropriate keys.")










class labDB():

    """
    For modifying and appending to the lab database XML file
    """

    def __init__(self, pathtoXML):
        self.tree = ET.parse(pathtoXML)
        self.root = self.tree.getroot()
        self.labs = []
        self._makelabs()
        self.new_id = self._getNextAvailableID()
        self.length = len(self.labs)
        self._valid_disciplines = getDisciplines()
        self._valid_topics = getTopics()
        self._valid_types = ["Lab", "Labatorial"]



    def log_file_object(self):
        date = datetime.datetime.today()
        date = str(date.year) + "-" + str(date.month) + "-" + \
               str(date.day) + "_" + str(date.hour) + "." + \
               str(date.minute) + "." + str(date.second)
        filename = "error_" + date + ".log"
        return open(filename, "w")



    def validateFull(self, error_log=False):
        if error_log:
            f = self.log_file_object()
            tests = [self.noDuplicateIDs(log_file=f),
                 self.hasValidPathRoots(log_file=f),
                 self.hasValidTypes(log_file=f),
                 self.hasValidDisciplines(log_file=f),
                 self.hasValidTopics(log_file=f),
                 self.hasUniqueEquipIDs(log_file=f)]
            f.close()
        else:
            f = None
            tests = [self.noDuplicateIDs(log_file=f),
                 self.hasValidPathRoots(log_file=f),
                 self.hasValidTypes(log_file=f),
                 self.hasValidDisciplines(log_file=f),
                 self.hasValidTopics(log_file=f),
                 self.hasUniqueEquipIDs(log_file=f)]
        if f:
            f.close()
        if all(tests):
            return True
        else:
            return False



    def noDuplicateIDs(self, log_file=None):
        error_log = []
        good = True
        seen = set()
        for lab in self.labs:
            if lab.id_num not in seen:
                seen.add(lab.id_num)
            else:
                good = False
                error_log.append("Lab \"" + lab.id_num +
                                 "\" is a duplicate of another lab in the database")
        if good == False:
            if log_file:
                [log_file.write(i + "\n") for i in error_log]
            else:
                [print(i) for i in error_log]
        return good



    def hasUniqueEquipIDs(self, log_file=None):
        error_log = []
        good = True
        equipment_ids = set()
        for lab in self.labs:
            for item in lab.equipment:
                equipment_ids.add(item["id"])
        for idn in equipment_ids:
            matching_items = set()
            for lab in self.labs:
                for item in lab.equipment:
                    if item["id"] == idn:
                        matching_items.add(item["name"])
            if len(matching_items) > 1:
                good = False
                error_log.append("Equipment ID \"" + idn + "\" has multiple names.")
        if good == False:
            if log_file:
                [log_file.write(i + "\n") for i in error_log]
            else:
                [print(i) for i in error_log]
        return good



    def hasValidPathRoots(self, log_file=None):
        error_log = []
        good = True
        valid_path_prefix = "/data/repository/"
        for lab in self.labs:
            for version in lab.versions:
                if not version["path"].startswith(valid_path_prefix):
                    good = False
                    error_log.append("Bad version path \"" +
                                     version["path"] + "\" in lab " +
                                     lab.id_num + " (" +
                                     lab.name + ")")
            for doc in lab.support_docs:
                if not doc["path"].startswith(valid_path_prefix):
                    good = False
                    error_log.append("Bad support document path \"" +
                                     doc["path"] + "\" in lab " +
                                     lab.id_num + " (" +
                                     lab.name + ")")
        if good == False:
            if log_file:
                [log_file.write(i + "\n") for i in error_log]
            else:
                [print(i) for i in error_log]
        return good



    def hasValidTypes(self, log_file=None):
        error_log = []
        good = True
        for lab in self.labs:
            if lab.lab_type not in self._valid_types:
                good = False
                error_log.append("Invalid type \"" +
                                 lab.lab_type + "\" in lab " +
                                 lab.id_num + " (" +
                                 lab.name + ")")
        if good == False:
            if log_file:
                [log_file.write(i + "\n") for i in error_log]
            else:
                [print(i) for i in error_log]
        return good



    def hasValidTopics(self, log_file=None):
        error_log = []
        good = True
        for lab in self.labs:
            for topic in lab.topics:
                if topic not in self._valid_topics:
                    good = False
                    error_log.append("Invalid topic \"" +
                                     topic + "\" in lab " +
                                     lab.id_num + " (" +
                                     lab.name + ")")
        if good == False:
            if log_file:
                [log_file.write(i + "\n") for i in error_log]
            else:
                [print(i) for i in error_log]
        return good



    def hasValidDisciplines(self, log_file=None):
        error_log = []
        good = True
        for lab in self.labs:
            for discipline in lab.disciplines:
                if discipline not in self._valid_disciplines:
                    good = False
                    error_log.append("Invalid discipline \"" +
                                     discipline + "\" in lab " +
                                     lab.id_num + " (" +
                                     lab.name + ")")
        if good == False:
            if log_file:
                [log_file.write(i + "\n") for i in error_log]
            else:
                [print(i) for i in error_log]
        return good



    def getLab(self, idnum=None, name=None):
        if not idnum and not name:
            return None
        if idnum:
            try:
                idnum = str(idnum).zfill(4)
                for lab in self.labs:
                    if lab.id_num == idnum:
                        return lab
                raise Exception("Lab id \"" + idnum + "\" doesn't exist")
            except Exception as e:
                raise e
        else:
            try:
                name = str(name)
                for lab in self.labs:
                    if name == lab.name:
                        return lab
                raise Exception("Lab name \"" + name + "\" doesn't exist")
            except Exception as e:
                raise e



    def deleteLab(self, idnum=None, name=None):
        if not idnum and not name:
            return None
        if idnum and isValidID(idnum):
            try:
                for lab in self.labs:
                    if lab.id_num == idnum:
                        self.labs.remove(lab)
                        self._updateXML()
                        self.length = len(self.labs)
                        self.new_id = self._getNextAvailableID()
                        return True
                raise Exception("Lab id \"" + idnum + "\" doesn't exist")
            except Exception as e:
                raise e
        else:
            try:
                name = str(name)
                for lab in self.labs:
                    if name == lab.name:
                        self.labs.remove(lab)
                        self._updateXML()
                        self.length = len(self.labs)
                        self.new_id = self._getNextAvailableID()
                        return True
                raise Exception("Lab name \"" + name + "\" doesn't exist")
            except Exception as e:
                raise e



    def newLab(self, idn):
        if isValidID(idn) and not self._idExistsAlready(idn):
            return _labItem(idnum=idn)
        else:
            raise Exception("Invalid lab ID number: IDs must be number strings of length 4 and mustn't exist already in the tree")



    def addLab(self, labitem):
        if not isinstance(labitem, _labItem):
            raise TypeError("Argument passed to labDB.addLab was not a _labItem object")
        if labitem.id_num in [lab.id_num for lab in self.labs]:
            tmp = [labitem if labitem.id_num == lab.id_num else lab for lab in self.labs]
            self.labs = tmp[:]
            self._updateXML()
            self.length = len(self.root)
            self.new_id = self._getNextAvailableID()
        else:
            self.labs.append(labitem)
            self.root.append(self._labItemToXMLNode(labitem))
            self._updateXML()
            self.length = len(self.root)
            self.new_id = self._getNextAvailableID()



    def save(self, filename, ignore_validation=False, error_log=False):
        if not isinstance(filename, str):
            raise TypeError("Argument of labDB.save must be string")
        if ignore_validation:
            self.tree.write(filename, encoding="UTF-8")
            print("XML object not validated and written to " + filename)
            return True
        elif not ignore_validation and self.validateFull(error_log=error_log):
            self.tree.write(filename, encoding="UTF-8")
            print("XML object successfully validated and written to " + filename)
            return True
        else:
            print("XML object not valid\nXML not saved to " + filename)
            return False



    def _makelabs(self):
        for child in self.root:
            self.labs.append(_labItem(lab=child))



    def _getNextAvailableID(self):
        ids = set()
        for lab in self.labs:
            ids.add(lab.id_num)
        for i in range(1,10000):
            if str(i).zfill(4) not in ids:
                return str(i).zfill(4)



    def _labExistsByName(self, name):
        for lab in self.labs:
            if name == lab.name:
                return True



    def _updateXML(self):
        self.root.clear()
        for lab in self.labs:
            self.root.append(self._labItemToXMLNode(lab))



    def _idExistsAlready(self, idnum):
        for lab in self.labs:
            if lab.id_num == idnum:
                return True



    def _labItemToXMLNode(self, labitem):
        if labitem.id_num:
            lab = ET.Element("Lab", {"labId": labitem.id_num})
            name = ET.SubElement(lab, "Name")
            name.text = labitem.name
            disciplines = ET.SubElement(lab, "Disciplines")
            for i in labitem.disciplines:
                child = ET.SubElement(disciplines, "Discipline")
                child.text = i
            topics = ET.SubElement(lab, "Topics")
            for i in labitem.topics:
                child = ET.SubElement(topics, "Topic")
                child.text = i
            versions = ET.SubElement(lab, "Versions")
            for i in labitem.versions:
                version = ET.SubElement(versions, "Version")
                path = ET.SubElement(version, "Path")
                path.text = i["path"]
                semester = ET.SubElement(version, "Semester")
                semester.text = i["semester"]
                year = ET.SubElement(version, "Year")
                year.text = i["year"]
                course = ET.SubElement(version, "Course")
                course.text = i["course"]
                directory = ET.SubElement(version, "Directory")
                directory.text = i["directory"]
            equipment = ET.SubElement(lab, "Equipment")
            for i in labitem.equipment:
                item = ET.SubElement(equipment, "Item", {"id": i["id"]})
                name = ET.SubElement(item, "Name")
                name.text = i["name"]
                amount = ET.SubElement(item, "Amount")
                amount.text = i["amount"]
            typ = ET.SubElement(lab, "Type")
            typ.text = labitem.lab_type
            supportdocs = ET.SubElement(lab, "SupportDocs")
            for i in labitem.support_docs:
                doc = ET.SubElement(supportdocs, "Doc")
                name = ET.SubElement(doc, "Name")
                name.text = i["name"]
                path = ET.SubElement(doc, "Path")
                path.text = i["path"]
            software = ET.SubElement(lab, "Software")
            for i in labitem.software:
                name = ET.SubElement(software, "Name")
                name.text = i
            return lab
        else:
            raise Exception("Any lab added to the tree must have, at minimum, a lab ID number")







class _labItem():

    def __init__(self, lab=None, idnum=None):
        if lab and isinstance(lab, ET.Element):
            self.id_num = lab.attrib["labId"]
            self.name = lab.findtext("Name")
            self.disciplines = [i.text for i in lab.find("Disciplines").findall("Discipline")]
            self.topics = [i.text for i in lab.find("Topics").findall("Topic")]
            self.versions = [{"path": i.findtext("Path"),
                              "semester": i.findtext("Semester"),
                              "year": i.findtext("Year"),
                              "course": i.findtext("Course"),
                              "directory": i.findtext("Directory")} for i in lab.find("Versions").findall("Version")]
            self.equipment = [{"id": i.attrib["id"],
                               "name": i.findtext("Name"),
                               "amount": i.findtext("Amount")} for i in lab.find("Equipment").findall("Item")]
            self.lab_type = lab.findtext("Type")
            self.support_docs = [{"name": i.findtext("Name"),
                                  "path": i.findtext("Path")} for i in lab.find("SupportDocs").findall("Doc")]
            self.software = [i.text for i in lab.find("Software").findall("Name")]
        elif not lab and isValidID(idnum):
            self.id_num = idnum
            self.name = ""
            self.disciplines = []
            self.topics = []
            self.versions = []
            self.equipment = []
            self.lab_type = ""
            self.support_docs = []
            self.software = []
        else:
            raise Exception("Invalid arguments passed to _labItem: either a valid lab or a valid lab ID must be passed")


    def addVersion(self, version):
        if isinstance(dict, version) \
           and "path" in version \
           and "semester" in version \
           and "year" in version \
           and "course" in version \
           and "directory" in version:
            self.versions.append(version)
        else:
            raise Exception("Invalid argument passed to _labItem.addVersion: argument must be dictionary with appropriate keys.")

    def addEquipment(self, item):
        if isinstance(dict, item) and "id" in item and "name" in item and "amount" in item:
            self.equipment.append(item)
        else:
            raise Exception("Invalid argument passed to _labItem.addEquipment: argument must be dictionary with appropriate keys.")

    def addSupportDoc(self, doc):
        if isinstance(dict, doc) and "name" in doc and "path" in doc:
            self.support_docs.append(doc)
        else:
            raise Exception("Invalid argument passed to _labItem.addSupportDoc: argument must be dictionary with appropriate keys.")


























#-----------------------------------------
#      EXAMPLE CODE AND USE CASES
#-----------------------------------------







if __name__ == "__main__":

    def addNewEntry():

        #-----------------------------------------
        #CREATING A NEW ENTRY IN THE LAB DATABASE
        #-----------------------------------------


        #Import an XML and make a database object

        db = labDB("../labDB.xml")



        #make a new lab object with the next available lab ID

        newlab = db.newLab(db.new_id)



        #Add the simple stuff; name and type

        newlab.name = "Fraunhofer Diffraction"
        newlab.lab_type = "Lab"



        #Add disciplines and topics

        newlab.disciplines = ["Optics", "Math", "Laboratory Skills"]
        newlab.topics = ["ODE", "PDE", "Polarization"]



        #Add versions

        versions = [{"path": "/data/repository/path/to/pdf",
                     "semester": "Fall",
                     "year": "2013",
                     "course": "PHYS 375",
                     "directory": "/data/repository/path/to/directory/"},
                    {"path": "/data/repository/path/to/pdf",
                     "semester": "Summer",
                     "year": "2016",
                     "course": "PHYS 369",
                     "directory": "/data/repository/path/to/directory/"},
                    {"path": "/data/repository/path/to/pdf",
                     "semester": "Winter",
                     "year": "2015",
                     "course": "PHYS 375",
                     "directory": "/data/repository/path/to/directory/"}]
        newlab.versions = versions



        #Add equipment

        equipment = [{"id": "0035", "name": "Fluke multimeter", "amount": "2"},
                     {"id": "0003", "name": "Anatek power supply", "amount": "1"},
                     {"id": "0143", "name": "small optical bench mount", "amount": "12"},
                     {"id": "0205", "name": "1 m optical bench", "amount": "1"}]
        newlab.equipment = equipment



        #Add support documents and software

        supportdocs = [{"name": "Hugo's notes", "path": "/data/repository/path/to/file"},
                       {"name": "TEX document", "path": "/data/repository/path/to/file"}]
        newlab.support_docs = supportdocs

        software = ["1D motion.cmbl", "Vernier Logger Pro", "VPython"]
        newlab.software = software



        #Add this new lab to the database and save the changes

        db.addLab(newlab)
        db.save("../../dev/updated_lab_database.xml", ignore_validation=False)



    def modifyEntry():

        #MODIFYING A LAB IN THE DATABASE


        #get the lab you want by name

        lab = db.getLab(name="Faraday's Law")

        #or by id number

        lab = db.getLab(idnum=37)


        #change any of its properties

        lab.topics = ["PDE", "Polarization"]


        #...or add a new version to a lab

        new_version = {"path": "/data/repository/path/to/pdf",
                       "semester": "Fall",
                       "year": "2013",
                       "course": "PHYS 375",
                       "directory": "/data/repository/path/to/directory/"}
        lab.addVersion(new_version)


        #add back to the db to replace the previous version

        db.addLab(lab)
        db.save("../../dev/updated_lab_database.xml", ignore_validation=False)





    def validateDB():

        #VALIDATING A DATABASE

        db = labDB("../labDB.xml")
        db.validateFull(error_log=True)  #full validation suite

        # with db.log_file_object() as f:
        #     db.hasValidTypes(log_file=f)  #check for valid lab types (Lab or Labatorial)

        #db.noDuplicateIDs(log_file=f)  #check for duplicate lab IDs
        #db.hasValidTopics(log_file=f)  #make sure all topics match those in README
        #db.hasValidDisciplines(log_file=f)  #make sure all disciplines match those in README
        #db.hasUniqueEquipIDs(log_file=f)  #make sure all equipment IDs are assigned to only one name
        #db.hasValidPathRoots(log_file=f)  #check all paths for proper directory root



    validateDB()
