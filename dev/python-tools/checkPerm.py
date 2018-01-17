#!/usr/bin/python3
#
# Script is to be run on slug to update permissions and ownership of files to sync to webserver
#
# Written by Peter Gimby Jan 17, 2018
#
# Must be run with sudo
import os

root="/usr/local/master/labs"
webSecurity = root + "/web-security"
downloads = root + "/downloads"
landingpage  = root + "/landingpage"
repository  = root + "/repository"
safety = root + "/safety"
schedules  = root + "/safety"
underConstruction  = root + "/under-construction"
publicDocs = [downloads, landingpage, repository, safety, schedules, underConstruction]

# define owners of files
owner = "pgimby"
group = "pjl_admins"

# change permissions and ownerships of files and folders
def changePerm(varDir,owner,group,filePerm,dirPerm):
	os.system("sudo find " + varDir + " -type d -exec chmod " + dirPerm + " {} \;")
	os.system("sudo find " + varDir + " -type f -exec chmod " + filePerm + " {} \;")
	os.system("sudo find " + varDir + " -type d -exec chown " + owner + "." + group + " {} \;")
	os.system("sudo find " + varDir + " -type d -exec chown " + owner + "." + group + " {} \;")


# check that script is being run on intended computer
host="slug"
myhost = os.uname()[1]
if host == myhost:
	changePerm(webSecurity,"root","root","644","755")
	for i in publicDocs:
		changePerm(i,"pgimby","pjl_admins","644","755")
else:
	print("This script is designed to be run on " + host + " only")
	print("Exiting")
	exit()

print("...and then there will be cake")
	#changePerm(webSecurity,"root","root","644","755")
	#for i in publicDocs:
	
	#	changePerm(i,"pgimby","pjl_admins","644","755")
