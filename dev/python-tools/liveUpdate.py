#!/usr/bin/python3
#
# Script is to be run on web server to update contents of lab repository used in the live version
#
# Written by Peter Gimby, Nov 17 2017


import os
import subprocess

# define folder locations
slugFolder = "slug:/usr/local/master/labs"
sourceFolder = "/mnt/local/labs.slug"
destFolder = "/mnt/local/labs"
repositoryFolder = "/mnt/local/labs/repository"
webRoot = "/var/www/html"

# define owners of files
owner = "pgimby"
group = "pjl_admins"
apacheUser = "www-data"

host="watt"
myhost = os.uname()[1]
if host == myhost:

    # mount the master copy of the repository on to web server
    os.system("mount " + slugFolder + " " + sourceFolder)


# Test to make sure master repository is mount, and if so sync master copy to live copy
    mountTest = os.system("mount | grep labs.slug > /dev/null")
    if mountTest == 0:
        os.system("rsync --delete -avz " + sourceFolder + "/repository/ " + destFolder + "/repository/")
        os.system("rsync --delete -avz " + sourceFolder + "/safety/ " + destFolder + "/safety/")
        os.system("rsync --delete -avz " + sourceFolder + "/schedules/ " + destFolder + "/schedules/")
        os.system("rsync --delete -avz " + sourceFolder + "/web-security/ " + destFolder + "/web-security/")
        os.system("rsync --delete -avz " + sourceFolder + "/landingpage/ " + destFolder + "/landingpage/")
        os.system("rsync --delete -avz " + sourceFolder + "/downloads/ " + destFolder + "/downloads/")

    # change permissions and ownerships of files and folders
    os.system("find " + destFolder + " -type d -exec chmod 755 {} \;")
    os.system("find " + destFolder + " -type f -exec chmod 644 {} \;")
    os.system("find " + destFolder + " -type d -exec chown " + owner + "." + group + " {} \;")
    os.system("find " + destFolder + " -type d -exec chown " + owner + "." + group + " {} \;")

    # Change permissions of a few important files/folders
    os.system("chown root." + apacheUser + " " + webRoot + "/data/labDB.xml" )
    os.system("chown root." + apacheUser + " " + webRoot + "/data/equipmentDB.xml" )
    os.system("chmod 660 " + webRoot + "/data/labDB.xml" )
    os.system("chmod 660 " + webRoot + "/data/equipmentDB.xml" )
    os.system("chown root." + apacheUser + " " + webRoot + "/data" )
    os.system("chmod 775 " + webRoot + "/data" )


    # unmount source files
    os.system("umount " + sourceFolder)
else:
    print("This script is designed to be run on " + host + " only")
    print("Exiting")
    exit()


print("...and then there will be cake")
