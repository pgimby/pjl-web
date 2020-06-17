#!/usr/bin/python3
#
# Script is to be run on web server to update contents of lab repository used in the live version
#
# Written by Peter Gimby, Nov 17 2017


import os, subprocess, argparse, filecmp, time
startTime = time.process_time()


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

#labFolders = ["downloads", "equipimg", "equipman", "landingpage", "repository", "safety", "schedules", "web-security","tools"]
webFolders = ["staffresources"]
#webFiles = ["index.html", "README.md"]
#mountInfo = [{"source": webSource, "mountPt": webMount}, {"source": labSource, "mountPt": labMount}]


'''define owners of files and general permissions'''
owner = "pgimby"
group = "pjl_admins"
apacheUser = "www-data"
devhost=["slug","fry","scruple"]
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

def wheel(dest,key,source,osTest):
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
parser.add_argument('-p', '--perm', help='test adding to xml without moving folders', action='store_true')
args = parser.parse_args()
testMode = args.test
perm = args.perm

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

'''rsync webpage folders'''
for i in webFolders:
    source = webSource + "/" + i + "/"
    dest = webMount + "/" + i + "/"
    syncFolder(rsycnOption,source,dest)
    changePerm(dest,owner,group,"644"," -type f",osTest)
    changePerm(dest,owner,group,"755"," -type d",osTest)

'''unmounts folders used for syncing files'''
umountFolder(webMount)
umountFolder(labMount)

print("...and then there will be cake")
