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



def validFilename(name):
    try:
        str(filename)
        return True
    except:
        return False





class labDB():

    """
    For modifying and appending to the lab database XML file
    """

    def __init__(self, tree):
        self.tree = tree
        self.root = tree.getroot()
        self.labs = []
        self._makelabs()
        self.new_id = self._getNextAvailableID()
        self.length = len(self.labs)
        self._valid_disciplines = []
        self._valid_topics = []
        self._valid_types = []
        


    def _makelabs(self):
        for child in self.root:
            self.labs.append(_labItem(lab=child))

            

    def validateFull(self, error_log=False):
        if error_log:
            date = datetime.datetime.today()
            date = str(date.year) + "-" + str(date.month) + "-" + \
                   str(date.day) + "-" + str(date.hour) + "-" + \
                   str(date.minute) + "-" + str(date.second)
            filename = "error_log-" + date + ".dat"
            f = open(filename, "w")
        else:
            f = None
        tests = [self.noDuplicateIDs(log=f),
                 self.hasValidPathRoots(log=f),
                 self.hasValidTypes(log=f),
                 self.hasValidDisciplines(log=f),
                 self.hasValidTopics(log=f),
                 self.hasUniqueEquipIDs(log=f)]
        f.close()
        if all(tests):
            return True
        else:
            return False


        
    def noDuplicateIDs(self, log=None):
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
            if log:
                [log.write(i + "\n") for i in error_log]
            else:
                [print(i) for i in error_log]
        return good



    def hasUniqueEquipIDs(self, log=None):
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
            if log:
                [log.write(i + "\n") for i in error_log]
            else:
                [print(i) for i in error_log]
        return good
    

    def hasValidPathRoots(self, log=None):
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
            if log:
                [log.write(i + "\n") for i in error_log]
            else:
                [print(i) for i in error_log]
        return good



    def hasValidTypes(self, log=None):
        error_log = []
        good = True
        valid_types = ["Lab", "Labatorial"]
        for lab in self.labs:
            if lab.lab_type not in valid_types:
                good = False
                error_log.append("Invalid type \"" +
                                 lab.lab_type + "\" in lab " +
                                 lab.id_num + " (" +
                                 lab.name + ")")
        if good == False:
            if log:
                [log.write(i + "\n") for i in error_log]
            else:
                [print(i) for i in error_log]
        return good

    
    
    def hasValidTopics(self, log=None):
        error_log = []
        good = True
        valid_topics = getTopics()
        for lab in self.labs:
            for topic in lab.topics:
                if topic not in valid_topics:
                    good = False
                    error_log.append("Invalid topic \"" +
                                     topic + "\" in lab " +
                                     lab.id_num + " (" +
                                     lab.name + ")")
        if good == False:
            if log:
                [log.write(i + "\n") for i in error_log]
            else:
                [print(i) for i in error_log]
        return good


    
    def hasValidDisciplines(self, log=None):
        error_log = []
        good = True
        valid_disciplines = getDisciplines()
        for lab in self.labs:
            for discipline in lab.disciplines:
                if discipline not in valid_disciplines:
                    good = False
                    error_log.append("Invalid discipline \"" +
                                     discipline + "\" in lab " +
                                     lab.id_num + " (" +
                                     lab.name + ")")
        if good == False:
            if log:
                [log.write(i + "\n") for i in error_log]
            else:
                [print(i) for i in error_log]
        return good

    

    def _getNextAvailableID(self):
        ids = set()
        for lab in self.labs:
            ids.add(lab.id_num)
        for i in range(1,10000):
            if str(i).zfill(4) not in ids:
                return str(i).zfill(4)
        


    def getLab(self, idnum=None, name=None):
        if not idnum and not name:
            return None
        if idnum:
            try:
                idnum = str(idnum)
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


    def newLab(self, idn):
        if isValidID(idn) and not self._idExistsAlready(idn):
            return _labItem(idnum=idn)
        else:
            raise Exception("Invalid lab ID number: IDs must be number strings of length 4 and mustn't exist already in the tree")
        


    def _idExistsAlready(self, idnum):
        for lab in self.labs:
            if lab.id_num == idnum:
                return True
        

    def addLab(self, labitem):
        if not isinstance(labitem, _labItem):
            raise TypeError("Argument passed to labDB.addLab was not a _labItem object")
        if labitem.id_num in [lab.id_num for lab in self.labs]:
            tmp = [labitem if labitem.id_num == lab.id_num else lab for lab in self.labs]
            self.labs = tmp[:]
            self._updateXML()
            self.length = len(self.root)
        else:
            self.labs.append(labitem)
            self.root.append(self._labItemToXMLNode(labitem))
            self.length = len(self.root)


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


    def _labExistsByName(self, name):
        for lab in self.labs:
            if name == lab.name:
                return True


    def _updateXML(self):
        self.root.clear()
        for lab in self.labs:
            self.root.append(self._labItemToXMLNode(lab))
            


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
                              "course": i.findtext("Course")} for i in lab.find("Versions").findall("Version")]
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















            












class equipmentDB():

    """
    For modifying and appending to the equipment database XML file
    """
    
    def __init__(self, tree):
        self.tree = tree
        self.root = tree.getroot()
        self.items = []
        self._makeitems()


    def _makeitems():
        pass





class _equipmentItem():

    def __init__(self, item):
        pass











if __name__ == "__main__":
   
    def addNewEntry():

    #-----------------------------------------
        #CREATING A NEW ENTRY IN THE LAB DATABASE
        #-----------------------------------------


        #Import an XML and make a database object

        tree = ET.parse("../labDB.xml")
        db = labDB(tree)



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
                     "course": "PHYS 375"},
                    {"path": "/data/repository/path/to/pdf",
                     "semester": "Summer",
                     "year": "2016",
                     "course": "PHYS 369"},
                    {"path": "/data/repository/path/to/pdf",
                     "semester": "Winter",
                     "year": "2015",
                     "course": "PHYS 375"}]
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

        lab = db.getLab(idnum="0037")


        #change any of its properties

        lab.topics = ["PDE", "Polarization"]


        #add back to the db to replace the previous version

        db.addLab(lab)
        db.save("../../dev/updated_lab_database.xml", ignore_validation=False)
 




    def validateDB():

        #VALIDATING A DATABASE

        tree = ET.parse("../labDB.xml")
        db = labDB(tree)
        db.validateFull(error_log=True)  #full validation suite
        #db.noDuplicateIDs()  #check for duplicate lab IDs
        #db.hasValidTopics()  #make sure all topics match those in README
        #db.hasValidDisciplines  #make sure all disciplines match those in README
        #db.hasUniqueEquipIDs()  #make sure all equipment IDs are assigned to only one name
        #db.hasValidTypes()  #check for valid lab types (Lab or Labatorial)
        #db.hasValidPathRoots()  #check all paths for proper directory root



    validateDB()
