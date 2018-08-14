#!/usr/bin/python3
#
# Script is to be run on web server to update contents of lab repository used in the live version
#
# Written by Peter Gimby, Nov 17 2017


import os, subprocess, argparse, filecmp, time

'''define folder locations'''
root = "/usr/local/master/"
webSource = root + "pjl-web"
labSource = root + "labs"
webDest = "/mnt/local/pjl-web"
labDest = "/mnt/local/labs"
webMount = "/mnt/pjl-web-mnt"
labMount = "/mnt/lab-mnt"
devEquipXML = webSource + "/dev/equipmentDB.xml"
dataEquipXML = webSource + "/data/equipmentDB.xml"
liveEquipXML = webMount + "/data/equipmentDB.xml"

labFolders = ["downloads", "equipimg", "equipman", "landingpage", "repository", "safety", "schedules", "web-security"]
webFolders = ["css", "data", "dev", "doc", "fonts", "img", "js", "php", "repository", "staffresources"]
webFiles = ["index.html", "README.md"]
webFileReverse = ["equipmentDB.xml"]
mountInfo = [{"source": webSource, "mountPt": webMount}, {"source": labSource, "mountPt": labMount}]


'''define owners of files and general permissions'''
owner = "pgimby"
group = "pjl_admins"
apacheUser = "www-data"
devhost=["slug","fry"]
webserver="watt.pjl.ucalgary.ca"


def testHost(host):
    thishost = os.uname()[1]
    if thishost not in host:
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
    os.system(osTest + "mv " + dest + "/" + key + ".xml " + dest + "/" + key + "-0.xml")
    os.system(osTest + "cp " + source + "/" + key + ".xml " + dest + "/" + key + ".xml")
    #os.system(osTest + "rm " + dest + "/" + key + "-8.xml")


def wheel(dest,key,source,osTest):
    print("updating equipmentDB.xml")
    dbFiles = getDbFiles(dest,key)
    #print(dbFiles)
    incrementFiles(list(reversed(dbFiles)),dest,key,source,osTest)

# def wheel(dbFile,source,dest,key,osTest):
#     print("updating equipmentDB.xml")
#     dbFiles = getDbFiles(dest,key)
#     #incrementFiles(list(reversed(dbFiles)),dest,key,source,osTest)

def changePerm(varDir,owner,group,filePerm,options,osTest):
    print("changing permissions of " + varDir + " with find" + options + ". This may take a minute.")
    os.system(osTest + "find " + varDir + options + " -exec chmod " + filePerm + " {} \;")
    os.system(osTest + "find " + varDir + options + " -exec chown " + owner + "." + group + " {} \;")

def gracefullExit(mountInfo):
    for i in mountInfo:
        umountFolder(i["mountPt"])
    exit()

'''checks that file a is newer that file b'''
def whichIsNewer(a,b,testMode):
    if os.path.isfile(a) and os.path.isfile(b):
        if os.path.getmtime(a) > os.path.getmtime(b):
            if testMode:
                print(a + " is newer than " + b )
                print(a + " " + str(os.path.getmtime(a)))
                print(b + " " + str(os.path.getmtime(b)))
            return True
        else:
            if testMode:
                print(b + " is newer than " + a)
                print(a + " " + str(os.path.getmtime(a)))
                print(b + " " + str(os.path.getmtime(b)))
            return False
    else:
        if not os.path.isfile(a):
            print("File " + a + " Does not exist. Exiting...")
            gracefullExit(mountInfo)
        if not os.path.isfile(b):
            print("File " + b + " Does not exist. Exiting...")
            gracefullExit(mountInfo)
    # if os.path.getmtime(a) > os.path.getmtime(b):
    #     return True
    # else:
    #     return False

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
if whichIsNewer(liveEquipXML,devEquipXML,testMode) and whichIsNewer(liveEquipXML,dataEquipXML,testMode):
    print("The live version of equipmentDB.xml is newer than the dev version.")
    if input("Do you wish to continue? y/N ") == "y":
        key = "equipmentDB"
        dataFolder = webSource + "/data"
        liveSource = webMount + "/data"
        wheel(dataFolder,key,liveSource,osTest)
        #wheel(i,source,dest,key,osTest)
    else:
        print("Exiting...")
        gracefullExit(mountInfo)


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
