#! /bin/sh
#
# Script for updating the content on the pjl webserver watt.pjl.ucalgary.ca
#
# Written by Peter Gimby, Sept 15, 2017


# Define some bash tools that will be used

RSYNC="/usr/bin/rsync"
FIND="/usr/bin/which"


<<<<<<< HEAD
# Source paths
#webSource="/home/pgimby/pjl-web/"
#webSource="/mnt/local/repository.slug/"
repositorySource="/mnt/local/repository.slug/"

# Destinations
#webDest="/mnt/local/legacy/html-future/"
repositoryDest="/mnt/local/repository/"
=======
# Define all sources and destination

repositorySource="/usr/local/master/labs/repository/"
#repositoryDest="watt:/mnt/local/repository/"
repositoryDest="watt:~/repository/"


# set permissions for all files and folders in repository

#find $repositorySource -type d -exec chmod 755 {} \;
#find $repositorySource -type f -exec chmod 644 {} \;
#find $repositorySource -type d -exec chown pgimby.pjl_admins {} \;
#find $repositorySource -type d -exec chown pgimby.pjl_admins {} \;


# sync files to web server


rsync --delete -anvz $repositorySource pgimby@$repositoryDest


#find /usr/local/master/labs/repository/ -type d -exec chmod 755 {} \;
#find -type f -exec chmod 644 {} $repositorySource \;
#find -type d -exec chown pgimby.pjl_admins {} $repositorySource \;
#find -type f -exec chown pgimby.pjl_admins {} $repositorySource \;


exit 0

# Source paths
#webSource="/home/pgimby/pjl-web/"

# Destinations
#webDest="watt:/var/www/html/data/repmnt/local/legacy/html-future/"
>>>>>>> eafcef468f8d9ddbb77eb2bea0bd8872852758f5

$RSYNC --delete -anvz $repositorySource $repositoryDest



exit
# set permissions
#chmod 644 $webSource/index.html
#chmod 644 $webSource/css/site-wide.css
#chmod 644 $webSource/js/pjl.js
#chmod 644 $webSource/js/jquery-3.2.1.min.js
#chmod 644 $webSource/img/*
<<<<<<< HEAD
chmod 755 $webSource/repository
chmod 644 $webSource/repository/index.html
=======
#chmod 755 $webSource/repository
#chmod 644 $webSource/repository/index.html
>>>>>>> eafcef468f8d9ddbb77eb2bea0bd8872852758f5

#sed 's/\/\/var siteroot = "\/pjl-web"/;

#chmod 644 $webSource/index.html


<<<<<<< HEAD
$RSYNC --delete -avz $webSource pgimby@$webDest
=======
#$RSYNC --delete -avz $webSource pgimby@$webDest

>>>>>>> eafcef468f8d9ddbb77eb2bea0bd8872852758f5


#ls $webCode
#ls $repository


