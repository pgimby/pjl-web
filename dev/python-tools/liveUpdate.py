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
webRoot = "/var/www/html"

# define owners of files
owner = "pgimby"
group = "pjl_admins"
apacheUser = "www-data"

# mount the master copy of the repository on to web server
#os.system("mount " + slugFolder + " " + sourceFolder)


# sync master copy to live copy
#os.system("rsync --delete -avz " + sourceFolder + "/ " + destFolder + "/")


# unmount source files
#os.system("umount " + sourceFolder)


# change permissions and ownerships of files and folders
#os.system("find " + destFolder + " -type d -exec chmod 755 {} \;")
#os.system("find " + destFolder + " -type f -exec chmod 644 {} \;")
#os.system("find " + destFolder + " -type d -exec chown " + owner + "." + group + " {} \;")
#os.system("find " + destFolder + " -type d -exec chown " + owner + "." + group + " {} \;")

os.system("echo chown root." + apacheUser + " " + webRoot + "/data/labDB.xml" )
os.system("echo chown root." + apacheUser + " " + webRoot + "/data/labDB.xml" )
os.system("echo chmod 660 " + webRoot + "/data/labDB.xml" )
os.system("echo chmod 660 " + webRoot + "/data/equipmentDB.xml" )

os.system("echo chown root" + apacheUser + " " + webRoot + "/data/labDB.xml" )
os.system("echo chmod 775 " + webRoot + "/data" )

# confirm end of script
print("...and then there will be cake")
