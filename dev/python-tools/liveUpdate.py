#!/usr/bin/python3
#
# Script is to be run on web server to update contents of lab repository used in the live version
#
# Written by Peter Gimby, Nov 17 2017


import os, subprocess, argparse, filecmp, time

'''define folder locations'''
webSource = "/usr/local/master/pjl-web"
labSource = "/usr/local/master/labs"
webDest = "/mnt/local/pjl-web"
labDest = "/mnt/local/labs"
webMount = "/mnt/pjl-web-mnt"
labMount = "/mnt/lab-mnt"
labFolders = ["downloads", "equipimg", "equipman", "landingpage", "repository", "safety", "schedules", "web-security"]
webFolders = ["css", "data", "dev", "doc", "fonts", "img", "js", "php", "repository", "staffresources"]
webFiles = ["index.html", "README.md"]
webFileReverse = ["equipmentDB.xml"]
mountInfo = [{"source": webSource, "mountPt": webMount}, {"source": labSource, "mountPt": labMount}]

'''define owners of files and general permissions'''
owner = "pgimby"
group = "pjl_admins"
apacheUser = "www-data"
devhost="slug"
webserver="watt"


def testHost(host):
    thishost = os.uname()[1]
    if not host == thishost:
        print("This script is designed to be run on " + thishost + " only. Exiting...")
        gracefullExit(mountInfo)

def mountFolder(source,mountPoint,remote,option):
    fullSource = remote + ":" + source
    os.system("mount -t nfs -o " + option + " " + fullSource + " " + mountPoint)
    if not os.system("mount | grep " + fullSource + " > /dev/null") == 0:
        print(fullSource + " did not mount properly. Exiting...")
        gracefullExit(mountInfo)

def umountFolder(mountPoint):
    os.system("umount " + mountPoint )

def syncFolder(testMode,source,dest):
    print("syning " + source)
    os.system("rsync" + testMode + " " + source + " " + dest)

def getDbFiles(dest,key):
    allFiles = os.listdir(dest)
    dbFiles = []
    for f in allFiles:
        if f.startswith(key) and f.split(".")[0][-1] in ['0','1','2','3','4','5','6','7']:
            dbFiles.append(f)
    return sorted(dbFiles)

def incrementFiles(files,dest,key,source,osTest):
    for i,f in enumerate(files):
        name = f.split(".")[0]
        index = int(name[-1])
        index += 1
        f = name[:-1] + str(index) + ".xml"
        os.system(osTest + "mv " + dest + "/" + files[i] + " " + dest + "/" + f)
    os.system(osTest + "mv " + dest + key + ".xml " + dest + "/" + key + "-0.xml")
    os.system(osTest + "cp " + source + " " + dest)


def wheel(dbFile,source,dest,key,osTest):
    print("updating equipmentDB.xml")
    dbFiles = getDbFiles(dest,key)
    incrementFiles(list(reversed(dbFiles)),dest,key,source,osTest)

def changePerm(varDir,owner,group,filePerm,options,osTest):
    print("changing permissions of " + varDir + " with find" + options + ". This may take a minute.")
    os.system(osTest + "find " + varDir + options + " -exec chmod " + filePerm + " {} \;")
    os.system(osTest + "find " + varDir + options + " -exec chown " + owner + "." + group + " {} \;")

def gracefullExit(mountInfo):
    for i in mountInfo:
        umountFolder(i["mountPt"])
    exit()

'''Main Script'''

'''User input to allow for a test mode during development'''
parser = argparse.ArgumentParser()
parser.add_argument('-t', '--test', help='test adding to xml without moving folders', action='store_true')
args = parser.parse_args()
testMode = args.test

if not os.getuid() == 0:
    print("This script must be run by \"The Great and Powerful Sudo\".")
    exit()

'''Parameters and options for operating in test mode'''
if testMode == True:
    rsycnOption = " -avnz --no-l"
    osTest = "echo "
else:
    rsycnOption = " -az --no-l"
    osTest = ""

'''Confirm that this script won't accidently run on the wrong machine'''
testHost(devhost)

'''mounts folder for syncing files and confirms success'''
mountFolder(webDest,webMount,webserver,"rw")
mountFolder(labDest,labMount,webserver,"rw")

'''update equipmenDB.xml from web server to development space if it is newer'''
for i in webFileReverse:
    key = "equipmentDB"
    source = webMount + "/data/" + i
    dest = webSource + "/data/"
    if os.path.getctime(source) >  os.path.getctime(dest + "equipmentDB.xml"):
    #if not filecmp.cmp(source, dest + i):
        wheel(i,source,dest,key,osTest)

'''Set permissions and owners of files and folders'''
changePerm(labSource,owner,group,"644"," -type f",osTest)
changePerm(labSource,owner,group,"755"," -type d",osTest)
changePerm(webSource,owner,group,"644"," -type f",osTest)
changePerm(webSource,owner,group,"755", " -type d",osTest)

'''Sets the permission for executable'''
changePerm(webSource,owner,group,"750"," -type f -name \'*.py\'",osTest)

'''rsync lab content folders'''
for i in labFolders:
    source = labSource + "/" + i + "/"
    dest = labMount + "/" + i + "/"
    print(i)
    syncFolder(rsycnOption,source,dest)

'''rsync webpage folders'''
for i in webFolders:
    source = webSource + "/" + i + "/"
    dest = webMount + "/" + i + "/"
    syncFolder(rsycnOption,source,dest)

'''rsync webpage files'''
for i in webFiles:
    source = webSource + "/" + i
    dest = webMount + "/"
    syncFolder(rsycnOption,source,dest)

'''changes the permissions of specific files and folders needed for live update of equipment numbers'''
changePerm(webMount + "/data" ,"root","www-data","660"," -type f -name equipmentDB.xml",osTest)
changePerm(webMount + "/data" ,"root","www-data","775"," -type d -name \'data\'",osTest)

'''unmounts folders used for syncing files'''
umountFolder(webMount)
umountFolder(labMount)

print("...and then there will be cake")
