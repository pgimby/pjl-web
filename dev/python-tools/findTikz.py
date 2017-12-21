#!/usr/bin/python3

import fnmatch
import os
import re


'''Define Paths '''
root_path = "/usr/local/master/labs/"
repository = root_path + "/repository"
output_path = root_path + "/landingpage/templates"
output_file = output_path + "/tikz.tex"
typ = ["mainfigure", "marginfigure", "figure"]

'''Define other parameters'''
pattern = "*FULL*"
doc_preamble = ['\\input{standard-preamble.tex}\n', '\\begin{document}\n', '\\title{Sample Tikz Diagrams}\n', '\\listoffigures', '\\newpage' ]
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
	name = "\section{" + name + "}"
	return name


def getTikz(lab, typ):
	
	'''find all code for diagrams'''
	texCode = []
	texFiles = listOfTex(lab)
	for tex in texFiles:
		with open(tex, "r", encoding="latin-1") as f:
			s = f.read()
			for t in typ:
				match = re.findall(r"\\begin{" + t + "}[.\s\S]*?\n([.\s\S]*?)\\\end{" + t + "}", s)
				for i in match:
					if "tikzpicture" in i:
						print(i, "\n\n\n")
						texCode.append(i)
	
	return list(set(texCode))

def addTextFromList(text_list, o):

	'''writes list of lines to latex file'''
	for i in text_list:
		o.write(str(i) + "\n")


def writeTikzToFile(texCode, o):
	o.write(texCode[0] + "\n\n")
	[print(i) for i in texCode[1]]
	for i in texCode[1]:
		o.write("\\begin{figure}\n")
		o.write(i + "\n")
		o.write("\\end{figure}\n")


def compileLatex(o):

	'''compile the output .tex file'''
	os.system("pdflatex " + o)

with open(output_file, "w") as o:
	addTextFromList(doc_preamble, o)
	lablist = listOfLabs(repository)
	for lab in lablist:
		labInfo = []
		labInfo.append(getTitle(lab))
		if getTikz(lab, typ):
			labInfo.append(getTikz(lab, typ))
			writeTikzToFile(labInfo, o)
#compileLatex(output_file)
#compileLatex(output_file)