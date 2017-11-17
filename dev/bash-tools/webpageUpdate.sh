#! /bin/bash
#
# Script for updating the content on the pjl webserver watt.pjl.ucalgary.ca
#
# Written by Peter Gimby, Sept 15, 2017


# Define some bash tools that will be used

RSYNC="/usr/bin/rsync"


# Source paths
#webSource="/home/pgimby/pjl-web/"
#webSource="/mnt/local/repository.slug/"
repositorySource="/mnt/local/repository.slug/"

# Destinations
#webDest="/mnt/local/legacy/html-future/"
repositoryDest="/mnt/local/repository/"

$RSYNC --delete -anvz $repositorySource $repositoryDest



exit
# set permissions
#chmod 644 $webSource/index.html
#chmod 644 $webSource/css/site-wide.css
#chmod 644 $webSource/js/pjl.js
#chmod 644 $webSource/js/jquery-3.2.1.min.js
#chmod 644 $webSource/img/*
chmod 755 $webSource/repository
chmod 644 $webSource/repository/index.html

#sed 's/\/\/var siteroot = "\/pjl-web"/;

#chmod 644 $webSource/index.html


$RSYNC --delete -avz $webSource pgimby@$webDest


#ls $webCode
#ls $repository


