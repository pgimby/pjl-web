#!/usr/bin/python3

#import packages
import os
import re
import urllib.request as rq
import xml.etree.ElementTree as ET




r = re.compile(r'href="([^"]*)"')
links = []
pjlroot = "http://www.pjl.ucalgary.ca"
count404 = 0


def get_status_code(url):
    """ This function retreives the status code of a website by requesting
        HEAD data from the host. This means that it only requests the headers.
        If the host cannot be reached or something else goes wrong, it returns
        None instead.
    """
    try:
        req = rq.Request(url, headers={"User-Agent": "Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}, method="HEAD")
        conn = rq.urlopen(req)
        return str(conn.getcode())
    except Exception as e:
        return str(e.code)

def getPathsFromXML(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    paths = root.findall(".//Path")
    paths[:] = [pjlroot + i.text for i in paths]
    return paths


def checkLink(url, filename=None):
    global count404
    status = get_status_code(url)
    if status != "401":
        if filename:
            print("STATUS: " + status + "       for link " + url + " in file " + dirpath + "/" + ff)
        else:
            print("STATUS: " + status + "       for link " + url)
    else:
        count404 += 1
        return

for dirpath, dirnames, files in os.walk("../../"):
    for ff in files:
        if (ff.endswith(".html") or ff.endswith(".txt")):
            with open(dirpath + "/" + ff, "r") as f:
                try:
                    s = f.read()
                    for m in re.findall(r, s):
                        if m.startswith("http"):
                            checkLink(m)
                except:
                    print("Failed to read file: ", dirpath + "/" + ff)


[checkLink(i) for i in getPathsFromXML("../../data/labDB.xml")]
print(str(count404), "forbidden requests")
