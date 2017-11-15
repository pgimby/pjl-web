#! /bin/bash
#
# Script for updating the content on the pjl webserver watt.pjl.ucalgary.ca
#
# Written by Peter Gimby, Sept 15, 2017


# Define some bash tools that will be used

RSYNC="/usr/bin/rsync"
FIND="/usr/bin/which"


# Define all sources and destination

repositorySource="/usr/local/master/labs/repository/"
repositoryDest="watt:/var/www/html/data/repository/"

# set permissions for all files and folders in repository

$FIND -type d -exec chmod 755 {} $repositorySource. \;


exit 0
$FIND -type f -exec chmod 644 {} . \;
$FIND -type d -exec chown pgimby.pjl_admins {} . \;
$FIND -type f -exec chown pgimby.pjl_admins {} . \;


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
$RSYNC --delete -avz $repositorySource pgimby@$repositoryDest


#ls $webCode
#ls $repository


