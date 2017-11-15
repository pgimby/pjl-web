#!/usr/bin/python3

#import packages
import xml.etree.ElementTree as ET




eqstandards = "../equipment-standards.dat"
xml_path = "../labDB.xml"



def getNumber(s):
    for i in range(1,20):
        if "(" + str(i) + ")" in s:
            return str(i)
    return "1"

#.replace("Ohm", "&#8486;").replace("micro", "&#181;")
def itemIdDic(filename):
    itemdic = {}
    with open(filename, "r") as f:
        for line in f.readlines():
            itemdic[line.split("\t")[1].strip("\n")] = line.split("\t")[0].strip("\n")
    return itemdic


def fixItemQuantity(xmlitem):
    num = getNumber(xmlitem[0].text)
    xmlitem[0].text = item[0].text.strip().replace("("+num+")", "").replace("  ", " ").strip()
    xmlitem[1].text = num
    return xmlitem[0].text, xmlitem[1].text


count = 0
bad = 0
dic = itemIdDic(eqstandards)
tree = ET.parse(xml_path)
root = tree.getroot()

for child in root:
    child[0].text = child[0].text.strip()




for equip in root.findall(".//Equipment"): #XPath syntax for getting all descendants
    for item in equip.findall("Item"):
        num_children = len(item.getchildren())
        if num_children != 0:
            #item[0].text, item[1].text = fixItemQuantity(item)
            
            count += 1
            try:
                i = dic[item[0].text]
                item.attrib["id"] = i
            except:
                bad += 1
                item.attrib["id"] = "0000"
                print("no match - setting to id='0000'")


print("matched ",str(100*(1-bad/count))[:4], "%")
tree.write("../labDB.xml", encoding="unicode")



