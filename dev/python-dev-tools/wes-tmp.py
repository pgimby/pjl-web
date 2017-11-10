#!/usr/bin/python3

#import packages
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import xml.etree.ElementTree as ET

validtopics = ["Electrostatics",
               "Circuits",
               "PDE",
               "ODE",
               "Statistics",
               "Linear Algebra",
               "Integration",
               "Differentiation",
               "Rotational Motion",
               "Statics",
               "Kinematics",
               "Collisions",
               "Dynamics",
               "Measurements",
               "Work and Energy",
               "Friction and Drag",
               "Momentum",
               "Conservation Laws",
               "Magnetism",
               "Interference",
               "Polarization",
               "Newton’s Laws",
               "Wave Mechanics",
               "Refraction",
               "Hydrostatics",
               "Gas Laws",
               "Programming"]
validdisc = ["Newtonian Mechanics",
             "Electricity and Magnetism",
             "Optics",
             "Thermodynamics",
             "Fluid Mechanics",
             "Statistical Mechanics",
             "Quantum Mechanics",
             "Relativity",
             "Particle Physics",
             "Nuclear Physics",
             "Math",
             "Laboratory Skills",
             "Computer Skills"]


tree = ET.parse("../labDB.xml")
root = tree.getroot()
data = []
with open("../wes-tmp.txt") as f:
    f.readline()
    for line in f.readlines():
        labid = line.split("\t")[0]
        disc = line.split("\t")[1]
        tops = line.split("\t")[2]
        disc = [i.strip() for i in disc.split(",")]
        tops = [i.strip() for i in tops.split(",")]
        for d in disc:
            if d not in validdisc:
                raise Exception(disc, d)
        for t in tops:
            if t not in validtopics:
                raise Exception(tops, t)
        data.append([labid, disc, tops])


for datum in data:
    for lab in root:
        
        if lab.attrib["labId"] == str(datum[0]):
            discnode = lab.find("Disciplines")
            discnode.clear()
            for d in datum[1]:
                subel = ET.SubElement(discnode, "Discipline")
                subel.text = str(d)
            topsnode = lab.find("Topics")
            topsnode.clear()
            for t in datum[2]:
                subel = ET.SubElement(topsnode, "Topic")
                subel.text = t

tree.write("../labDB.xml")
