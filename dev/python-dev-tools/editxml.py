#!/usr/bin/python3

from bs4 import BeautifulSoup
#from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import xml.etree.ElementTree as ET
# print "hello"


original = open("source.html", "r")
xml = open("archives.xml", "w")
soup = BeautifulSoup(original, 'html.parser')
labs = ET.Element('Labs')

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





