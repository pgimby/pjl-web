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


def itemIdDic(filename):
    itemdic = {}
    with open(filename, "r") as f:
        for line in f.readlines():
            itemdic[line.split("\t")[1].strip("\n")] = line.split("\t")[0].strip("\n")
    return itemdic





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
        if num_children != 0 and item.get("id") == "0000":
            #num = getNumber(item[0].text)
            #item[0].text = item[0].text.strip().replace("("+num+")", "").replace("  ", " ").strip()
            #item[1].text = num
            
            count += 1
            try:
                i = dic[item[0].text]
                item.attrib["id"] = i
            except:
                bad += 1
                print("no match")


print("matched ",str(100*(1-bad/count))[:4], "%")
tree.write("../labDB.xml", encoding="unicode")



