#!/usr/bin/python3
#
# Script is to be run on web server to update contents of lab repository used in the live version
#
# Written by Peter Gimby, Nov 17 2017


import os


# define folder locations
slugFolder = "slug:/usr/local/master/labs/repository"
sourceFolder = "/mnt/local/repository.slug"
destFolder = "/mnt/local/repository"


# define owners of files
owner = "pgimby"
group = "pjl_admins"


# mount the master copy of the repository on to web server
os.system("mount " + slugFolder + " " + sourceFolder)


# sync master copy to live copy
os.system("rsync -avz " + sourceFolder + "/ " + destFolder + "/")


# change permissions and ownerships of files and folders
os.system("find " + destFolder + " -type d -exec chmod 755 {} \;")
os.system("find " + destFolder + " -type f -exec chmod 6445 {} \;")
os.system("find " + destFolder + " -type d -exec chown " + owner + "." + group + " {} \;")
os.system("find " + destFolder + " -type d -exec chown " + owner + "." + group + " {} \;")


# unmount source files
os.system("umount " + sourceFolder)


# confirm end of script
print("...and then there will be cake")
