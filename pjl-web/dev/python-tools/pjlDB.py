#!/usr/bin/python3

#import packages
import xml.etree.ElementTree as ET
import re
import datetime

readme_location = "../../README.md"


class IDDoesNotExist(Exception):
    pass

class EQIDDoesNotExist(Exception):
    pass


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

    with open(readme_location, "r") as f:
        s = f.read()
        m = re.search(r"<!---start topics-->\n([.\s\S]*)\n<!---end topics-->", s)
    lst = [i.strip() for i in m.group(0).split("\n")[1:-1]]
    return lst



def getDisciplines():

    """returns a list of strings"""

    with open(readme_location, "r") as f:
        s = f.read()
        m = re.search(r"<!---start disciplines-->\n([.\s\S]*)\n<!---end disciplines-->", s)
    lst = [i.strip() for i in m.group(0).split("\n")[1:-1]]
    return lst


def crossValidateEquipment(eqdb, labdb):
    labs = labdb.labs
    equipment = eqdb.equipment
    error_log = []
    for lab in labs:
        items = lab.equipment
        for item in items:
            itemfound = False
            for eq in equipment:
                if eq.name == item["name"] and eq.id_num == item["id"]:
                    itemfound = True
                    break
            if not itemfound and not labdb._isItAKit(item["id"]):
                error_log.append("Item " + item["name"] + "(" + item["id"] + ")" + " from lab " + lab.id_num + " not found in equipment database.")
    if error_log:
        [print(i) for i in error_log]
    else:
        print("A place for everything and everything in its place. No errors found. Gold sticker.")


def rightNow():
        date = datetime.datetime.today()
        date = str(date.year) + "-" + str(date.month).zfill(2) + "-" + \
               str(date.day).zfill(2) + "T" + str(date.hour).zfill(2) + ":" + \
               str(date.minute).zfill(2) + ":" + str(date.second).zfill(2)
        return date




class EquipDB():

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
        filename = "log/error_" + date + ".log"
        return open(filename, "w")



    def validateFull(self, error_log=False):
        if error_log:
            f = self.log_file_object()
            tests = [self.noDuplicateIDs(log_file=f),
                 self.hasValidPathRoots(log_file=f),
                 self.noDuplicateNames(log_file=f)]
            f.close()
        else:
            f = None
            tests = [self.noDuplicateIDs(log_file=f),
                 self.hasValidPathRoots(log_file=f),
                 self.noDuplicateNames(log_file=f)]
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



    def noDuplicateNames(self, log_file=None):
        error_log = []
        good = True
        seen = set()
        for item in self.equipment:
            if item.name not in seen:
                seen.add(item.name)
            else:
                good = False
                error_log.append("Equipment item \"" + item.name +
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
        valid_path_prefix = "/staffresources/equipment/equipman"
        for item in self.equipment:
            for document in item.documents:
                if not document["location"].startswith(valid_path_prefix):
                    good = False
                    error_log.append("Bad document path \"" +
                                     document["location"] + "\" in equipment item " +
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
                raise EQIDDoesNotExist("Exception: Equipment id \"" + idnum + "\" doesn't exist")
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



    def deleteItem(self, lab_database, idnum=None, name=None):
        if not idnum and not name:
            return None
        if not isinstance(lab_database, LabDB):
            raise TypeError("Argument 'lab_database' passed to EquipDB.deleteItem was not a LabDB object")

        if idnum and isValidID(idnum):
            check, labs = self._isPrimaryEquipment(idnum, lab_database)
            if check:
                print("Item " + str(idnum) + " is used in the following labs (primary equipment):\n")
                for lab in labs:
                    print(lab["name"] + " (" + lab["id"] + ")")
                goahead = input("Doth thou wisheth to proceed? (y/N)")
                if goahead != "Y" and goahead != "y":
                    print("Deletion aborted")
                    return None

            check, labs = self._isAlternateEquipment(idnum, lab_database)
            if check:
                print("Item " + str(idnum) + " is used in the following labs (alternate equipment):\n")
                for lab in labs:
                    print(lab["name"] + " (" + lab["id"] + ")")
                goahead = input("Doth thou wisheth to proceed? (y/N)")
                if goahead != "Y" and goahead != "y":
                    print("Deletion aborted")
                    return None

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
            return _EquipmentItem(idnum=idn)
        else:
            raise Exception("Invalid lab ID number: IDs must be number strings of length 4 and mustn't exist already in the tree")



    def addItem(self, equipitem):
        if not isinstance(equipitem, _EquipmentItem):
            raise TypeError("Argument passed to EquipDB.addItem was not an _EquipmentItem object")
        equipitem.last_modified = rightNow()
        if equipitem.id_num in [item.id_num for item in self.equipment]:
            tmp = [equipitem if equipitem.id_num == item.id_num else item for item in self.equipment]
            self.equipment = tmp[:]
            self._updateXML()
            self.length = len(self.root)
            self.new_id = self._getNextAvailableID()
        else:
            self.equipment.append(equipitem)
            self.root.append(self._equipItemToXMLNode(equipitem))
            self._updateXML()
            self.length = len(self.root)
            self.new_id = self._getNextAvailableID()


    def save(self, filename, ignore_validation=False, error_log=False):
        self._updateXML()
        if not isinstance(filename, str):
            raise TypeError("Argument of EquipDB.save must be string")
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



    def _isPrimaryEquipment(self, idnum, lab_database):
        check = False
        labs = []
        for lab in lab_database.labs:
            for eq in lab.equipment:
                if eq["id"] == idnum:
                    labs.append({"name": lab.name, "id": lab.id_num})
                    check = True
                    break
        return check, labs



    def _isAlternateEquipment(self, idnum, lab_database):
        check = False
        labs = []
        for lab in lab_database.labs:
            for eq in lab.equipment:
                if eq["alt-id"] == idnum:
                    labs.append({"name": lab.name, "id": lab.id_num})
                    check = True
                    break
        return check, labs



    def _makeEquipment(self):
        for child in self.root:
            self.equipment.append(_EquipmentItem(item=child))



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



    def _equipItemToXMLNode(self, equipitem):
        if equipitem.id_num:
            item = ET.Element("Item", {"id": equipitem.id_num, "lastModified": equipitem.last_modified})
            name = ET.SubElement(item, "InventoryName")
            name.text = equipitem.name
            identification = ET.SubElement(item, "Identification")
            manufacturer = ET.SubElement(identification, "Manufacturer")
            manufacturer.text = equipitem.manufacturer
            model = ET.SubElement(identification, "Model")
            model.text = equipitem.model
            thumb = ET.SubElement(identification, "Thumbnail")
            thumb.text = equipitem.thumbnail
            kit = ET.SubElement(item, "Kit")
            kit.attrib = {"isKit": "true" if equipitem.is_kit else "false"}
            kit.text = equipitem.kit
            locations = ET.SubElement(item, "Locations")
            for i in equipitem.locations:
                location = ET.SubElement(locations, "Location")
                room = ET.SubElement(location, "Room")
                room.text = i["room"]
                storage = ET.SubElement(location, "Storage")
                storage.text = i["storage"]
            quantity = ET.SubElement(item, "Quantity")
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
                docname.text = d["name"]
                loc = ET.SubElement(doc, "Location")
                loc.text = d["location"]
            return item
        else:
            raise Exception("Any piece of equipment added to the tree must have, at minimum, an ID number")














class _EquipmentItem():

    def __init__(self, item=None, idnum=None):
        if item and isinstance(item, ET.Element):
            self.id_num = item.attrib["id"]
            self.last_modified = item.attrib["lastModified"]
            self.name = item.findtext("InventoryName")
            self.manufacturer = item.findtext(".//Manufacturer")
            self.model = item.findtext(".//Model")
            self.thumbnail = item.findtext(".//Thumbnail")
            self.is_kit = True if item.find("Kit").attrib["isKit"] == "true" else False
            self.kit = item.findtext(".//Kit")
            self.locations = []
            for loc in item.findall("./Locations/Location"):
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
            self.last_modified = rightNow()
            self.name = ""
            self.manufacturer = ""
            self.model = ""
            self.is_kit = False
            self.kit = ""
            self.locations = []
            self.quantity = {"total": "", "service": "", "repair": ""}
            self.documents = []
            self.thumbnail = "/img/img-placeholder.png"

        else:
            raise Exception("Invalid arguments passed to _EquipmentItem: either a valid Item or a valid equipment ID must be passed")



    def addDocument(self, doc):
        if isinstance(doc, dict) and "name" in doc and "location" in doc:
            self.documents.append(doc)
        else:
            raise Exception("Invalid argument passed to _EquipmentItem.addDocument: argument must be dictionary with appropriate keys.")



    def addLocation(self, loc):
        if isinstance(loc, dict) and "room" in loc and "storage" in loc:
            self.locations.append(loc)
        else:
            raise Exception("Invalid argument passed to _EquipmentItem.addLocation: argument must be dictionary with appropriate keys.")
















class LabDB():

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
        self._valid_types = ["Lab", "Labatorial", "Home", "Remote"]



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
                 self.hasUniqueEquipIDs(log_file=f),
                 self.noDuplicateNames(log_file=f),
                 self.noDuplicateVersions(log_file=f)]
            f.close()
        else:
            f = None
            tests = [self.noDuplicateIDs(log_file=f),
                 self.hasValidPathRoots(log_file=f),
                 self.hasValidTypes(log_file=f),
                 self.hasValidDisciplines(log_file=f),
                 self.hasValidTopics(log_file=f),
                 self.hasUniqueEquipIDs(log_file=f),
                 self.noDuplicateNames(log_file=f),
                 self.noDuplicateVersions(log_file=f)]

        if f:
            f.close()
        if all(tests):
            return True
        else:
            return False

    def noDuplicateNames(self, log_file=None):
        error_log = []
        good = True
        seen = set()
        for item in self.labs:
            if item.name not in seen:
                seen.add(item.name)
            else:
                good = False
                error_log.append("Lab \"" + item.name +
                                 "\" is a duplicate of another item in the database")
        if good == False:
            if log_file:
                [log_file.write(i + "\n") for i in error_log]
            else:
                [print(i) for i in error_log]
        return good



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


    def noDuplicateVersions(self, log_file=None):
        error_log = []
        good = True
        seen = set()
        for lab in self.labs:
            versionInfo = []
            for version in lab.versions:
                versionDict = {}
                versionDict["course"] = version["course"]
                versionDict["year"] = version["year"]
                versionDict["semester"] = version["semester"]
                if versionDict not in versionInfo:
                    versionInfo.append(versionDict)
                else:
                    error_log.append("Lab \"" + lab.id_num +
                                     "\" has mulitple instance of the same version" )
                    good = False
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
                if not self._isItAKit(idn):
                    good = False
                    error_log.append("Equipment ID \"" + idn + "\" has multiple names.")
        if good == False:
            if log_file:
                [log_file.write(i + "\n") for i in error_log]
            else:
                [print(i) for i in error_log]
        return good



    def _isItAKit(self, idnum):
        tree = ET.parse("../../data/equipmentDB.xml")
        root = tree.getroot()
        for child in root:
            if child.attrib["id"] == idnum:
                if child.find(".//Kit").attrib["isKit"] == "true":
                    return True
                else:
                    return False
        raise Exception("Invalid equipment ID number.")






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
                raise IDDoesNotExist("Lab id \"" + idnum + "\" doesn't exist")
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
            return _LabItem(idnum=idn)
        else:
            raise Exception("Invalid lab ID number: IDs must be number strings of length 4 and mustn't exist already in the tree")



    def addLab(self, labitem):
        if not isinstance(labitem, _LabItem):
            raise TypeError("Argument passed to LabDB.addLab was not a _LabItem object")
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
        self._updateXML()
        if not isinstance(filename, str):
            raise TypeError("Argument of LabDB.save must be string")
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


    def replaceEquipment(self, replaced, replaced_with, push_to_alternate=False):
        if replaced and replaced_with and isValidID(replaced):
            for i, lab in enumerate(self.labs):
                for j, item in enumerate(lab.equipment):
                    if item["id"] == replaced:
                        if push_to_alternate:
                            self.labs[i].equipment[j]["alt-id"] = self.labs[i].equipment[j]["id"]
                            self.labs[i].equipment[j]["alt-name"] = self.labs[i].equipment[j]["name"]
                        self.labs[i].equipment[j]["id"] = replaced_with.id_num
                        self.labs[i].equipment[j]["name"] = replaced_with.name
        else:
            raise Exception("Invalid arguments passed to _LabDB.replaceEquipment")



    def _makelabs(self):
        for child in self.root:
            self.labs.append(_LabItem(lab=child))



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
                if i["alt-id"] and i["alt-name"]:
                    alt = ET.SubElement(item, "Alt")
                    alt.text = i["alt-name"]
                    alt.attrib = {"id": i["alt-id"]}
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













class _LabItem():

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
                               "amount": i.findtext("Amount"),
                               "alt-name": i.findtext("Alt") if isinstance(i.find("Alt"), ET.Element) else "",
                               "alt-id": i.find("Alt").attrib["id"] if isinstance(i.find("Alt"), ET.Element) else ""} for i in lab.find("Equipment").findall("Item")]
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
            raise Exception("Invalid arguments passed to _LabItem: either a valid lab or a valid lab ID must be passed")



    def addVersion(self, version):
        if isinstance(version, dict) \
           and "path" in version \
           and "semester" in version \
           and "year" in version \
           and "course" in version \
           and "directory" in version:
            self.versions.append(version)
        else:
            raise Exception("Invalid argument passed to _LabItem.addVersion: argument must be dictionary with appropriate keys.")



    def addEquipment(self, item):
        if isinstance(item, dict) and "id" in item and "name" in item and "amount" in item:
            if "alt-id" in item and "alt-name" in item:
                self.equipment.append(item)
            else:
                item["alt-id"] = ""
                item["alt-name"] = ""
                self.equipment.append(item)
        else:
            raise Exception("Invalid argument passed to _LabItem.addEquipment: argument must be dictionary with appropriate keys.")



    def addSupportDoc(self, doc):
        if isinstance(doc, dict) and "name" in doc and "path" in doc:
            self.support_docs.append(doc)
        else:
            raise Exception("Invalid argument passed to _LabItem.addSupportDoc: argument must be dictionary with appropriate keys.")


























#-----------------------------------------
#      EXAMPLE CODE AND USE CASES
#-----------------------------------------







if __name__ == "__main__":

    def addNewEntry():

        #-----------------------------------------
        #CREATING A NEW ENTRY IN THE LAB DATABASE
        #-----------------------------------------


        #Import an XML and make a database object

        db = LabDB("../labDB.xml")



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

        db = LabDB("../labDB.xml")
        db.validateFull(error_log=True)  #full validation suite

        # with db.log_file_object() as f:
        #     db.hasValidTypes(log_file=f)  #check for valid lab types (Lab or Labatorial)

        #db.noDuplicateIDs(log_file=f)  #check for duplicate lab IDs
        #db.hasValidTopics(log_file=f)  #make sure all topics match those in README
        #db.hasValidDisciplines(log_file=f)  #make sure all disciplines match those in README
        #db.hasUniqueEquipIDs(log_file=f)  #make sure all equipment IDs are assigned to only one name
        #db.hasValidPathRoots(log_file=f)  #check all paths for proper directory root



    validateDB()
