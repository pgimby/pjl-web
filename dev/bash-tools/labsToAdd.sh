#! /bin/bash

# Script to take a collection of version folders and build a csv file that can be fed into a updateNewSemester.py for adding new version of labs to the labDB.xml
#
# Written by Peter Gimby Sept 15, 2017

versionList=$(ls | grep PHYS)

for I in $versionList
do
	labID=$(echo $I | cut -c1-4)
	parentPath=$(find /usr/local/master/labs/repository -maxdepth 1 -type d | grep $labID | sed 's/usr\/local\/master\/labs/data/g')
	pdfName=$(ls -R $I | grep 2017 | grep -v TA |grep -v CG | grep -v FULL | grep .pdf)
	pdfPath="$parentPath/$I/$pdfName"
	course=$(echo $I | cut -c10-12)
	semesterAb=$(echo $I | cut -c13-14)
	year=$(echo $I | cut -c15-18)
	case "$semesterAb" in
		FA)
			semester="Fall"
			;;
		SP)
			semester="Spring"
			;;
		SU)
			semester="Summer"
			;;
		WI)
			semester="Winter"
			;;
		*)
			exit 0
			;;
	esac
	csvLine="$labID,$pdfPath,$semester,$year,PHYS $course,$parentPath/"
	echo $csvLine >> list.csv
	#echo $labID, $pdfPath, $parentPath,
done

echo "...and then there shall be cake"
exit 0


