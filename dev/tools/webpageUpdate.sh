#! /bin/bash
#
# Script for updating the content on the pjl webserver watt.pjl.ucalgary.ca
#
# Written by Peter Gimby, Sept 15, 2017


# Define some bash tools that will be used

RSYNC="/usr/bin/rsync"


# Source paths
webCode="/home/pgimby/pjl-web/"
repository="/usr/local/master/labs/repository"

# Destinations

dest="watt:/mnt/local/legacy/html-future/"

$RSYNC -avnz $webCode pgimby@$dest

#ls $webCode
#ls $repository


