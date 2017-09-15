#!/usr/bin/python3
import xml.etree.ElementTree as ET
import os, glob, fnmatch


def findAll(pattern, path):
	result = []
	for root, dirs, files in os.walk(path):
	#for root in os.walk(path):
		result.append(str(dirs))
		#print(str(dirs))
		#for name in files:
		#	print(os.path.join(root, name))
			#print(pattern + " " + name)
			#if fnmatch.fnmatch(name,pattern)):
			#	print("found match")
				#print(name + " " + str(files))
			#	result.append(os.path.join(root,name))
				#print(root)
				#print(dirs)
		print(result)

#	print(str(result))
			#result.append(os.path.join(root,name))
	#print(result)

findAll("testing", 'test-full')
#for name in glob.glob('test/*'):
	#print(name)



































exit()
print("should not see this")


def newLabFolder(orig,idnum,rootpath):						# Builds the name of the new folders for lab
	print("original " +orig)
	orig = orig.replace(' ', '-')
	orig = orig.replace("'", "")
	orig = orig.replace("(", "")
	orig = orig.replace(")", "")
	orig = orig.strip()
	newname = rootpath + "/"+ idnum + "-" + orig
	return newname

def originalPath(orig):							# Finds name of original folder
	originalpath = orig[0].text
	print(originalpath)

def convertSemesters(semester):					# Finds the semsester and converts to abbreviation
	if semester == "Fall":
		semester = "FA"
	elif semester == "Spring":
		semester = "SP"
	elif semester == "Summer":
		semester = "SU"
	elif semester == "Winter":
		semester = "WI"
	return semester

def newFolder(orig,idnum,labfolder):			# Builds the name for new folders for versions
	year = orig[2].text
	course = orig[3].text
	course = str(course)
	course = course.replace(" ","")
	semester = orig[1].text
	semester = convertSemesters(semester)
	newname = labfolder + "/" + idnum + '-' + course + semester + year
	return(newname)

def findParentDir(pdf, path, year, paths):					# Finds the original folder of each version
	for root, dirs, files in os.walk(path):
		testpartrue = pathTestName(paths)
		try:
			testpar = root.split("/")[8]
			if pdf in files and testpar == testpartrue:
				return os.path.join(root)
		except:
			pass
		
			

def pathTestName(paths):
	return paths.split("/")[2]

def moveFolder(orig, parent, version):
	#print("From" + orig)
	#print("parent lab folder" + parent)
	#print("new version folder full path - " + version)
	if os.path.isdir(parent) == False:
		os.mkdir(parent)
	os.rename(orig,version)

def modifyXml(folder,i,pdf):
	start = "/data/repository/"
	print(i[0].text)
	folder = folder.split("/")[6:]
	folder = [str(i) for i in folder]
	folder = "/".join(folder)
	newxml = start + folder + "/"+ pdf
	i[0].text = newxml

tree = ET.parse('../../dev/labDB.xml')
root = tree.getroot()
rootpath="/usr/local/master/labs/repository"

for lab in root:
	idnum = lab.get('labId')
	#if idnum == "0073":
	name = lab[0].text
	labfolder = newLabFolder(name,idnum,rootpath)
	versions = lab[3].getchildren()
	for i in  versions:
		year = i[2].text									# current year of pdf being searched for
		course = i[3].text									# current course of pdf being searhed for
		versionfolder = newFolder(i,idnum,labfolder) 		# absolute path of new version folder
		paths = i[0].text									# current path in xml file
		pdf = paths.split("/")[-1]							# file name of pdf to be searched for
		pdf = str(pdf)	
		pdfpath = findParentDir(pdf, rootpath, year, paths) # absolute path of folder to be moved
		print(pdfpath)
		modifyXml(versionfolder,i, pdf)
		moveFolder(pdfpath, labfolder, versionfolder)
tree.write('blah.xml',short_empty_elements=False)
