#!/usr/bin/python3

#import packages
import xml.etree.ElementTree as ET


#each data row, in order: lab name, disciplines, topics, equip, type





#parameters

xml_path = "./archives.xml"
details_data_path = "./lab-details.dat"

#functions

def getXML(filepath):
    tree = ET.parse(filepath)
    return tree


def getLabDetailData(filepath):
    data = []
    with open(filepath, "r") as f:
        f.readline()
        lines = f.readlines()
    for line in lines:
        cols = line.split("\t") #split row on tabs
        cols = [i.strip() for i in cols] #strip end whitespace from each column entry
        cols = [[j.strip() for j in i.split(",")] for i in cols] #break cols into lists on commas
        data.append(cols)
    return data


def appendDetailstoXML(xml, data):
    labs = xml.getroot()
    for lab in labs:
        coursesNode = removeDuplicateCourses(lab[2])
        lab.remove(lab[2])
        lab.insert(2, coursesNode)

        name = lab[0][0].text #remove Labatorial: junk from name
        if "labatorial" in name.lower():
            name = name.split(":")[-1]
        name = name.strip()
        name = name.replace("Traveling", "Travelling")
        lab[0][0].text = name


    labs[:] = [lab for lab in labs if not lab[0][0].text.lower().endswith("ta notes")]
    for lab in labs:
        lab[1].clear()
        lab[3].clear()
        lab[5].clear()
        for datum in data:
            if datum[0][0] == lab[0][0].text:
                for disc in datum[1]:
                    child = ET.SubElement(lab[1], "Discipline")
                    child.text = disc
                for topic in datum[2]:
                    child = ET.SubElement(lab[3], "Topic")
                    child.text = topic
                for equip in datum[3]:
                    child = ET.SubElement(lab[5], "Item")
                    child.text = equip
                lab[6].text = datum[4][0];
                

                    
    saveXML("archives-mod.xml", xml)


def removeDuplicateCourses(courses):
    courseslist = []
    for child in courses:
        courseslist.append(child.text)
    courseslist = list(set(courseslist))

    newCourses = ET.Element("Courses")
    for el in courseslist:
        course = ET.SubElement(newCourses, "Course")
        course.text = el

    return newCourses

    

def saveXML(filename, tree):
    tree.write(filename)



#load/define data

data = getLabDetailData(details_data_path)
xmltree = getXML(xml_path)
appendDetailstoXML(xmltree, data)

#print(i) for i in data]

#manipulate data



#present data

