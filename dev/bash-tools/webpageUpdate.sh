#! /bin/sh
#
# Script for updating the content on the pjl webserver watt.pjl.ucalgary.ca
#
# Written by Peter Gimby, Sept 15, 2017


# Define some bash tools that will be used

RSYNC="/usr/bin/rsync"
FIND="/usr/bin/which"


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


find /usr/local/master/labs/repository/ -type d -exec chmod 755 {} \;
find -type f -exec chmod 644 {} $repositorySource \;
find -type d -exec chown pgimby.pjl_admins {} $repositorySource \;
find -type f -exec chown pgimby.pjl_admins {} $repositorySource \;

chown root.www-data /var/www/html/data/labDB.xml
chown root.www-data /var/www/html/data/equipmentDB.xml

exit 0

# Source paths
#webSource="/home/pgimby/pjl-web/"

# Destinations
#webDest="watt:/var/www/html/data/repmnt/local/legacy/html-future/"

# set permissions
#chmod 644 $webSource/index.html
#chmod 644 $webSource/css/site-wide.css
#chmod 644 $webSource/js/pjl.js
#chmod 644 $webSource/js/jquery-3.2.1.min.js
#chmod 644 $webSource/img/*
#chmod 755 $webSource/repository
#chmod 644 $webSource/repository/index.html

#sed 's/\/\/var siteroot = "\/pjl-web"/;

#chmod 644 $webSource/index.html


#$RSYNC --delete -avz $webSource pgimby@$webDest



#ls $webCode
#ls $repository


