#!/usr/bin/python3

import fnmatch
import os
import re


'''Define Paths '''
root_path = "/usr/local/master/labs"
repository = root_path + "/repository"
output_path = root_path + "/landingpage/tikz-examples"
output_file = output_path + "/tikz-examples.tex"
typ = ["mainfigure", "marginfigure", "figure"]

'''Define other parameters'''
pattern = "*FULL*"
doc_preamble = ['\\input{' + output_path + '/standard-preamble.tex}\n', '\\begin{document}\n', '\\title{Sample Tikz Diagrams}\n', '\\tableofcontents', '\\newpage' ]
doc_end = ['\\end{document}\n']


def listOfLabs(repository):

	'''generate list of lab folders with absolute path names'''
	listOfLabs = []
	for lab in os.listdir(repository):
		listOfLabs.append(os.path.join(repository,lab))
	return listOfLabs


def listOfTex(lab):

	'''generates list of absolute paths of tex files'''
	texFiles = []
	for root, dirs, files in os.walk(lab):
		for filename in fnmatch.filter(files,pattern):
			if fnmatch.fnmatch(filename, "*.tex"):
				if filename:
					texFiles.append(os.path.join(root,filename))
	return texFiles


def getTitle(lab):
	
	'''get name of lab'''
	name = lab.split("/")[-1]
	name = name.split("-")[1:]
	name = " ".join(name)
	name = "\chapter{" + name + "}"
	#print(name)
	return name


def getTikz(lab, typ):
	
	'''find all code for diagrams'''
	texCode = []
	texFiles = listOfTex(lab)
	for tex in texFiles:
		#print(tex)
		#if "2015" in tex and "323" in tex:
			#print(tex)
		with open(tex, "r", encoding="latin-1") as f:
			s = f.read()
			s = re.sub(r"\\begin{comment}[.\s\S]*?\\end{comment}", "", s)
			#print(s)
			for t in typ:
				match = re.findall(r"\\begin{" + t + "}[.\s\S]*?\n([.\s\S]*?)\\\end{" + t + "}", s)
				for i in match:
					if "tikzpicture" in i:
						texCode.append(i)
	return list(set(texCode))

def addTextFromList(text_list, o):

	'''writes list of lines to latex file'''
	for i in text_list:
		o.write(str(i) + "\n")


def writeTikzToFile(texCode, o):
	o.write(texCode[0] + "\n\n")
	for i in texCode[1]:
		o.write("\\begin{figure}\n")
		o.write(i)
		o.write("\\end{figure}\n")
		o.write("\n")


def compileLatex(o):

	'''compile the output .tex file'''
	os.system("pdflatex " + o)

with open(output_file, "w") as o:
	addTextFromList(doc_preamble, o)
	lablist = listOfLabs(repository)

	for lab in lablist:
	#for i in range(23,25):
		#lab = lablist[i]
		labInfo = []
		#print(lab)
		labInfo.append(getTitle(lab))
#		o.write("chapter{" + labTitle + "}")
		if getTikz(lab, typ):
			labInfo.append(getTikz(lab, typ))
			writeTikzToFile(labInfo, o)
	o.write("\\end{document}")
#compileLatex(output_file)
#compileLatex(output_file)