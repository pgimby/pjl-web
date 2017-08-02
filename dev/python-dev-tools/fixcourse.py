#!/usr/bin/python3
import xml.etree.ElementTree as ET

#
#from xml.etree.ElementTree import Element, SubElement, Comment, tostring
#print ("hello")


#original = open("source.html", "r")
#xml = "../labDB-test.xml"
#soup = BeautifulSoup(original, 'html.parser')
#labs = ET.Element('Labs')
tree = ET.parse('../labDB-test.xml')
root = tree.getroot()

for lab in root:
	name = lab[0][0].text
	versions = lab[3].getchildren()
	for i in  versions:
		path = i[0].text
		coursename = path.split("/")[1][7:10]
		coursename = "PHYS " + coursename
		course = ET.SubElement(i, 'Course')
		course.text = coursename
tree.write('../newlabDB.xml')
#ET.dump(tree)   # for debugging xml format
		#print(lab[3][0])
		#print()
	#print(name)
	#versions = []
	#paths = lab[3].getchildren()
	#print(paths)
	#for path in paths:
	#	print(path.text)

exit()

def getXML(filepath):
    tree = ET.parse(filepath)
    return tree

def addCourseToXML(xml):
    labs = xml.getroot()
    print (labs)

xmltree = getXML(xml)
addCourseToXML(xmltree)

exit()


def removeTag(xml):
	labs = xml.getroot()
	for lab in labs:
		print (lab)

def saveXML(filename, tree):
    tree.write(filename)

removeTag(xml)


# Function for generating a single set of tab for a new lab entry
def generateXML(lablist, labname):
	for el in labname:
		lab = ET.SubElement(labs, 'Lab', attrib={"labId": ""})
		names = ET.SubElement(lab, 'Names')
		name = ET.SubElement(names, 'Name')
		name.text = el
		disciplines = ET.SubElement(lab, 'Disciplines')
		discipline = ET.SubElement(disciplines, 'Discipline')
		courses = ET.SubElement(lab, 'Courses')
		for i in lablist:
			if el == i["Name"]:
				course = ET.SubElement(courses, 'Course')
				course.text = i["Course"]
		topics = ET.SubElement(lab, 'Topics')
		topic = ET.SubElement(topics, 'Topic')
		versions = ET.SubElement(lab, 'Versions')
		for i in lablist:
			if el == i["Name"]:
				version = ET.SubElement(versions, 'Version')
				path = ET.SubElement(version, 'Path')
				path.text = i["Path"]
				semester = ET.SubElement(version, "Semester")
				semester.text = convertSemesters(i["Semester"])
				year = ET.SubElement(version, "Year")
				year.text = i["Year"]
		equipment = ET.SubElement(lab, 'Equipment')
		item = ET.SubElement(equipment, 'Item')
		labtype = ET.SubElement(lab, 'Type')
		supportdoc = ET.SubElement(lab, 'SupportDocs')
	tree=ET.ElementTree(labs)	
	tree.write('blah.xml',short_empty_elements=False)  # for writing xml format to file
	#ET.dump(tree)   # for debugging xml format

def convertSemesters(semester):
	if semester == "FA":
		semester = "Fall"
	elif semester == "SP":
		semester = "Spring"
	elif semester == "SU":
		semester = "Summer"
	elif semester == "WI":
		semester = "Winter"
	return semester

# generat a list of unique names
def getLabsList():
	labinfo=[]
	for link in soup.find_all('a'):
		name=str(link.string)
		path=str(link.get('href'))
		info=path.split("/")
		year=info[0]
		course="PHYS " + info[1].split("-")[0][-3:]
		semester=info[1].split("-")[-1][:2]
		#print(semester)
		labinfo.append({"Name": name, "Path": path, "Year": year, "Course": course, "Semester": semester})
		#print(type(semester))
		#print({"Name": name, "Path": path, "Year": year, "Course": course, "Semester": semester})
	return labinfo

def getUniqueNames():
	uniquenames=[]
	for link in soup.find_all('a'):
		uniquenames.append(str(link.string))
	uniquenames=(list(set(uniquenames)))
	return uniquenames

lablist=getLabsList() 					# didctionary with all labs with individual entries for each version
names=getUniqueNames()					# list of unique names

#print(lablist)
generateXML(lablist, names)
#print(names)

# def labInfo():
# 	uniquenames = generateUniqueNames()	
# 	for i in uniquenames:





