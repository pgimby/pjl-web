#!/usr/bin/python3

#import packages
import xml.etree.ElementTree as ET




    


def isValidID(idnum):
    try:
        int(idnum)
    except:
        return False
    if isinstance(idnum, str) and len(idnum) == 4:
        return True
    else:
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


    def validateFull(self, tree):
        tests = [self.noDuplicateIDs(tree),
                 self.hasProperOrdering(tree),
                 self.hasValidPathRoots(tree),
                 self.hasValidTypes(tree)]
        if all(tests):
            return True
        else:
            return False


    def noDuplicateIDs(self, tree):
        pass


    def hasProperOrdering(self, tree):
        pass


    def hasValidPathRoots(self, tree):
        pass


    def _getNextAvailableID(self):
        ids = set()
        for lab in self.labs:
            ids.add(lab.idnum)
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
                    if lab.idnum == idnum:
                        return lab
                return None
            except:
                return None
        else:
            try:
                name = str(name)
                for lab in self.labs:
                    if name == lab.name:
                        return lab
                return None
            except:
                return None


    def newLab(self, idn):
        if isValidID(idn) and not self._idExistsAlready(idn):
            return _labItem(idnum=idn)
        else:
            raise Exception("Invalid lab ID number: IDs must be number strings of length 4 and mustn't exist already in the tree")


    def _idExistsAlready(self, idnum):
        for child in self.labs:
            if child.idnum == idnum:
                return True
        

    def addLab(self, labitem):
        if not isinstance(labitem, _labItem):
            raise TypeError("Argument passed to labDB.addLab was not a _labItem object")
        else:
            self.labs.append(labitem)
            self.root.append(self._labItemToXMLNode(labitem))
            self.length = len(self.root)


    def save(self, filename):
        if not isinstance(filename, str):
            raise TypeError("Argument of labDB.save must be string")
        if self.validateFull(self.tree):
            self.tree.write(filename, encoding="UTF-8")
            print("XML object successfully validated and written to " + filename)
            return True
        else:
            print("XML object not valid\nXML not saved to " + filename)
            return False


    def _labItemToXMLNode(self, labitem):
        if labitem.idnum:
            lab = ET.Element("Lab", {"labId": labitem.idnum})
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
                number = ET.SubElement(item, "Number")
                number.text = i["number"]
            typ = ET.SubElement(lab, "Type")
            typ.text = labitem.labtype
            supportdocs = ET.SubElement(lab, "SupportDocs")
            for i in labitem.supportdocs:
                doc = ET.SubElement(supportdocs, "Doc", {"type": i["name"]})
                doc.text = i["path"]
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
                               "amount": i.findtext("Number")} for i in lab.find("Equipment").findall("Item")]
            self.lab_type = lab.findtext("Type")
            self.support_docs = [{"name": i.attrib["type"],
                                 "path": i.text} for i in lab.find("SupportDocs").findall("Doc")]
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
    db.save("../../dev/updated_lab_database.xml")
