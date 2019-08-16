#!/usr/bin/python3

import argparse
import os
import fnmatch
import re

''' root path for generating collection of labs document '''
root="/usr/local/master/labs/under-construction/"
preamble="standard-preamble.tex"

''' Static organizational information '''
semesters={"WI": "Winter", "SP": "Spring", "SU": "Summer", "FA": "Fall"}
titles={"255": "Electomagnet Theory I", "323": "Optics and Electomagnetism", "325": "Modern Physics", "341": "Classical Mechanics", "365": "Acoustics, Optics, and Modern Physics for Engineers", "369": "Acoustics, Optics, and Radiation for Engineers", "375": "Introduction to Optics and Waves", "397": "Applied Physics Laboratory I", "497": "Applied Physics Laboratory II"}

'''lines to add to beginning of collection of labs documents: titlePage2 is generated based on course'''
titlePage1 = ["\\begin{document}\n", "\n" "\\begin{titlepage}\n","\\vspace*{\\fill}\n","\\begin{center}\n"]
titlePage3 = ["\\end{center}\n","\\vspace*{\\fill}\n","\\end{titlepage}\n","\\maketitle\n","\\begin{spacing}{0.5}\n","\\tableofcontents\n","\\end{spacing}\n"]

'''Possible files wanted as a preface to collection of labs document'''
rulesPath = "/usr/local/master/labs/safety/lab-rules/Lab-Rules.tex"
labSafetyPath = "/usr/local/master/labs/safety/training/Orientation/Orientation.tex"
radiationSafetyPath = "/usr/local/master/labs/safety/training/Radiation-Safety/Radiation-Safety-in-the-Undergraduate-Physics-Labs.tex"
possiblePrefacePaths = [rulesPath, labSafetyPath, radiationSafetyPath]





''' Functions that gather general in formation about course '''

''' Get course number '''
def getCourse(info):
	'''
	strips the course number from a string of the form PHYS###SSYYYY which
	 is entered by the user

	Args:
		info (str) string of the form PHYS###SSYYYY

	Return:
		course (str) string containing ### portion of input string
	'''
	course=info[4:7]
	return course

''' Get semester full name from ID'''
def getSemester(semesters,semesterID):
	semester = semesters.get(semesterID)
	return semester

''' Get year '''
def getYear(info):
	return info[9:13]

''' get Title of course '''
def getTitle(titles, course):
	title = titles.get(course)
	return title

''' Generate ordered list of experiment documents to compile '''
def listOfIDs(labDir,course,semester):
	orderFile = labDir + "/physics" + course + "-lab-order"
	IDs = []
	if os.path.isfile(orderFile):
		with open(orderFile, "r") as o:
			for i in o:
				IDs.append(i[0:4])
	else:
		print("lab order does not exist")
		exit()
	return IDs

''' Generate name of ouptput file '''
def getOutputName(path,year,semesterID):
	latexPath = getLatexFile(path,year,semesterID)
	splitPath = latexPath[0].split("/")[-1]
	out1 = splitPath.split("-")[0:-2]
	out1 = "-".join(out1)
	out2 = splitPath.split("-")[-1]
	output = path + "/" + out1 + "-ST-" + out2
	return output

''' Generate portion of title page that is specific to each course'''
def getTitlePage2(title, course, semester, year):
	titlePage2 = []
	titlePage2.append("\\huge{{\\bf Physics " + course +"}}\\\[0.4cm]\n")
	titlePage2.append("\\LARGE{Laboratory Manual}\\\[0.4cm]\n")
	titlePage2.append("\\huge{" + title + "}\\\[0.4cm]\n")
	titlePage2.append("\\large{"+ semester + " " + year + "}\n")
	return titlePage2

''' Generates list of source latex files '''
def getLatexFile(path,year,semester):
	testPar = "*FULL-" + semester + year + ".tex"
	latexPath = []
	for root, dirs, files in os.walk(path):
		for filename in fnmatch.filter(files,testPar):
			latexPath.append(os.path.join(root,filename))
	return latexPath

''' Generate list of course specific preface docs'''
def getPrefaceList(course,origLst,radiationSafetyPath):
	lst =[]
	if course == "325":
		lst = origLst
	else:
		for i in origLst:
			if i != radiationSafetyPath:
				lst.append(i)
	return lst


''' Functions that existance of important componensts '''

''' Check that a given directory exists'''
def checkDir(chkDir):
	print("A: " + chkDir )
	if os.path.isdir(chkDir):
		return True
	else:
		print("Missing Path " + chkDir)
		exit()





''' Functions for pulling or editing code from source files '''

''' Strips out the latex code from the source latex file'''
def stripLatex(latexPath,o,path,start,stop):
	latexCode = []
	with open(latexPath[0], "r") as labDoc:
		fullDoc = labDoc.read()
		labBody = re.findall(start + "[.\s\S]*?\n([.\s\S]*?)" + stop + "[.\s\S]*?\n",fullDoc)
		for i in labBody:
			o.write(fixGraphicPath(i,latexPath,path))

''' Strips out the latex code from preface documents'''
def stripPreface(path,start,stop,o,prefaceDir):
	latexCode = []
	with open(path, "r") as labDoc:
		fullDoc = labDoc.read()
		labBody = re.findall(start + "[.\s\S]*?\n([.\s\S]*?)" + stop + "[.\s\S]*?\n",fullDoc)
		for i in labBody:
			o.write(fixGraphicPath(i,path,prefaceDir))

''' Replaces relative path names for graphics with abosolute path names '''
def fixGraphicPath(labBodyLine,latexPath,path):
	typ = ["pdf", "jpg", "png", "eps"]
	for graphicType in typ:
		testExp = r"{([^\{]*?\." + graphicType + ")}"
		graphic = re.findall(testExp,labBodyLine,flags=re.IGNORECASE)
		graphic = list(set(graphic))
		for i in graphic:
			newPath = path + "/" + i
			labBodyLine = re.sub(i, newPath, labBodyLine)
	return labBodyLine




''' Functions for compiling output document(s) '''

''' Initial document and add title page content'''
def largeDocStart(o,course, title, semester,labDir,preamble, titlePage1, titlePage3,year):
	o.write("\\input{" + labDir + "/" + preamble + "}\n")
	titlePage2 = getTitlePage2(title, course, semester, year)
	for i in titlePage1:
		o.write(i)
	for i in titlePage2:
		o.write(i)
	for i in titlePage3:
		o.write(i)

''' Add latex code that separates chapters/labs '''
def addLabPreamble(o,chapter):
	o.write("\\setcounter{chapter}{"+ str(chapter) +"}\n")
	o.write("\\setcounter{equation}{0}\n\\setcounter{table}{0}\n\\setcounter{figure}{0}")





''' Higher level functions for compiling latex code'''

''' Generate student specific documents '''
def addStudentLab(year,semesterID,o,path):
	print(str(path))
	checkDir(path)
	latexPath = getLatexFile(path,year,semesterID)
	start = "%%%start document"
	stop = "%%%end document"
	stripLatex(latexPath,o,path,start,stop)

''' Add preface documents to student version of lab '''
def addPrefaceST(o,path):
	start = "%%%start document"
	stop = "%%%end document"
	for i in path:
		prefaceDir = "/".join(i.split("/")[:-1])
		stripPreface(i,start,stop,o,prefaceDir)

''' Generate TA specific documents '''
def addTALab(year,semesterID,o,path):
	checkDir(path)
	latexPath = getLatexFile(path,year,semesterID)
	start = "%%%start companion guide"
	stop = "%%%end companion guide"
	stripLatex(latexPath,o,path,start,stop)

''' Add prefece documents to TA version of lab '''
def addPrefaceCG(o,path):
	start = "%%%start companion guide"
	stop = "%%%end companion guide"
	for i in path:
		prefaceDir = "/".join(i.split("/")[:-1])
		stripPreface(i,start,stop,o,prefaceDir)

''' Genterate indivudual student version of lab documents'''
def buildIndividualStudent(year,semesterID,preamble,args,path):
	indOutput = getOutputName(path,year,semesterID)
	print(indOutput)
	with open(indOutput, "w") as ind:
		ind.write("\\input{" + preamble + "}\n")
		ind.write("\\begin{document}\n")
		addStudentLab(year,semesterID,ind,path)
		ind.write("\\end{document}\n")
	if args.compile == True:
		compileLatex(indOutput)
		compileLatex(indOutput)





''' Compile the output latex file twice'''
def compileLatex(o):

	'''compile the output .tex file'''
	path = o.split("/")[:-1]
	path = "/".join(path)
	os.system("pdflatex -output-directory=" + path + " " + o)
	os.system("pdflatex -output-directory=" + path + " " + o)





'''START OF SCRIPT'''


''' Set flags from user'''
parser = argparse.ArgumentParser(
	formatter_class=argparse.RawDescriptionHelpFormatter,
	epilog='''
Know bugs and other important information:
------------------
	A) All labs must be located in their own folder, inside of a master folder
		- inside this folder must be a text file with the labID numbers of all labs to include
		- lab order file must not have blank lines
''')
parser.add_argument('courseinfo', help='PHYS###SSYYYY ie PHYS325WI2018')
parser.add_argument('-d', '--debug', help='debug code', action='store_true')
parser.add_argument('-p', '--preface', help='add preface documents to start of complete document for course', action='store_true')
parser.add_argument('-s', '--student', help='student version', action='store_true')
parser.add_argument('-t', '--ta', help='TA version', action='store_true')
parser.add_argument('-i', '--individual', type=int, help='Compile Single Lab Only: 0 - all labs, 1 - first lab in list, 2 - second lab in list...etc')
parser.add_argument('-c', '--compile', help='Will compile any output .tex file', action='store_true')
parser.add_argument('-l', '--list', help='Generate list of pdfs to be added to website', action='store_true')
parser.add_argument('-m', '--man', help='print extra information about program', action='store_true')
args = parser.parse_args()



''' Gather information about labs to compile'''
courseinfo=args.courseinfo
course = getCourse(args.courseinfo)
semesterID = courseinfo[7:9]
semester = getSemester(semesters,semesterID)
labDir = root + args.courseinfo
IDs = listOfIDs(labDir,course,semester)
title = getTitle(titles, course)
year = getYear(args.courseinfo)
prefacelist = getPrefaceList(course,possiblePrefacePaths,radiationSafetyPath)

''' Compile documents - Student Version'''
if args.student == True:
	output = labDir + "/" + args.courseinfo + "-ST.tex"
	chapter = 0
	with open(output, "w") as o:
		largeDocStart(o,course,title,semester,labDir,preamble,titlePage1,titlePage3,year)
		if args.preface == True:
			addPrefaceST(o,prefacelist)
		for lab in IDs:
			chapter += 1
			addLabPreamble(o,chapter)
			path = labDir + "/" + lab + "-" + courseinfo
			addStudentLab(year,semesterID,o,path)
		o.write("\\end{document}\n")
	if args.compile == True:
		compileLatex(output)



'''Compile TA Version'''
if args.ta == True:
	output = labDir + "/" + args.courseinfo + "-CG.tex"
	chapter = 0
	with open(output, "w") as o:
		title = title + " - Companion Guide"
		largeDocStart(o,course,title,semester,labDir,preamble,titlePage1,titlePage3,year)
		if args.preface == True:
			addPrefaceST(o,prefacelist)
			addPrefaceCG(o,prefacelist)
		for lab in IDs:
			chapter += 1
			addLabPreamble(o,chapter)
			path = labDir + "/" + lab + "-" + courseinfo
			addStudentLab(year,semesterID,o,path)
			addTALab(year,semesterID,o,path)
		o.write("\\end{document}\n")
	if args.compile == True:
		compileLatex(output)


'''Compile individual student documents'''
if type(args.individual) == int:
	if args.individual != 0:
		labref = args.individual - 1
		print(labref)
		individualID = IDs[labref]
		path = labDir + "/" + individualID + "-" + courseinfo
		buildIndividualStudent(year,semesterID,preamble,args,path)
	if args.individual ==0:
		for i in IDs:
			print(i)
			path = labDir + "/" + i + "-" + courseinfo
			buildIndividualStudent(year,semesterID,preamble,args,path)


''' Generates a csv for adding lab to repository '''
if args.list == True:
	output = root + courseinfo + "/" + courseinfo + ".csv"
	webroot = "/data/repository/"
	#print(output)
	with open(output, 'w') as o:
		for i in IDs:
			idnum = ("\'" + i + "\'")
			repDir="/usr/local/master/labs/repository"
			for dr in os.listdir(repDir):
				if i in dr:
					labDir = repDir + "/" + dr + "/"
			testPar = "*ST-" + semesterID + year + ".pdf"
			for root, dirs, files in os.walk(labDir):
				for filename in fnmatch.filter(files,testPar):
					name = filename
			labName = labDir.split("/")[-2:-1]
			path = webroot + labName[0] + "/" + i + "-" + courseinfo + "/" + name
			o.write(idnum + ",'" + path + "','" + semester + "','" + year + "','PHYS " + str(course) +"'\n")



print("...and then there will be cake")