# -*- coding: utf-8 -*-
import os
import sys
from lxml import etree as ET
from classes import *
import subprocess
import time
import concurrent.futures as cf


class OGS(object):
    def __init__(self, **args):
        self.geo = geo.GEO()
        self.mesh = mesh.MESH()
        self.pyscript = python_script.PYTHON_SCRIPT()
        self.processes = processes.PROCESSES()
        self.media = media.MEDIA()
        self.timeloop = timeloop.TIMELOOP()
        self.local_coordinate_system = local_coordinate_system.LOCAL_COORDINATE_SYSTEM()
        self.parameters = parameters.PARAMETERS()
        self.curves = curves.CURVES()
        self.processvars = processvars.PROCESSVARS()
        self.linsolvers = linsolvers.LINSOLVERS()
        self.nonlinsolvers = nonlinsolvers.NONLINSOLVERS()
        sys.setrecursionlimit(10000)
        self.tag = []
        self.tree = None
        #self.loadmkl = None
        self.loadmkl = "source /opt/intel/mkl/bin/mklvars.sh intel64"
        self.ogs_name = ""
        if "PROJECT_FILE" in args:
            self.prjfile = args['PROJECT_FILE']
        else:
            print("PROJECT_FILE not given. Calling it default.prj.")
            self.prjfile = "default.prj"
        if "INPUT_FILE" in args:
            self.inputfile = args['INPUT_FILE']
        else:
            self.inputfile = "default.prj"
        if "ogs_mode" in args:
            self.ogs_mode = args["ogs_mode"]
        else:
            self.ogs_mode = "silent"

    def runModel(self, **args):
        if "path" in args:
            self.ogs_name = args["path"] + "/"
        else:
            self.ogs_name = ""
        if sys.platform == "win32":
            self.ogs_name = self.ogs_name + "ogs.exe"
        else:
            self.ogs_name = self.ogs_name + "ogs"
        procs = [0,1]
        def run(proc):
            running = True
            if proc == 0:
                print("OGS running...")
                if not self.loadmkl:
                    cmd = self.ogs_name + " " + self.prjfile + " >out"
                else:
                    cmd = self.loadmkl + " && " + self.ogs_name + " " + self.prjfile + " >out"
                returncode = subprocess.run([cmd], shell=True, executable="/bin/bash")
                if returncode.returncode == 0:
                    print("OGS finished")
                    return True
                else:
                    print("OGS execution not successfull. Error code: ", returncode.returncode)
                    raise RuntimeError
            if proc == 1:
                while running is True:
                    if self.ogs_mode == "silent":
                        running = False
                    else:
                        out=subprocess.check_output(["tail", "-10", "out"]).decode("ascii")
                        out2=out.split("\n")
                        for line in out2:
                            if "timestep" in line:
                                print("\r", line, end="")
                            if "stepping" in line:
                                print("\r", line, end="")
                            if "Iteration" in line:
                                print("\r", line, end="")
                            if "terminated" in line:
                                print("\r", line)
                                running = False
                            if "error:" in line:
                                print("An error during OGS execution occurred")
                                print("\r", line)
                                raise RuntimeError
                        time.sleep(0.5)
                return
        with cf.ThreadPoolExecutor() as executor:
            results = executor.map(run,procs)

    def __dict2xml(self, parent, dictionary):
        for entry in dictionary:
            self.tag.append(ET.SubElement(parent, dictionary[entry]['tag']))
            self.tag[-1].text = dictionary[entry]['text']
            for attr in dictionary[entry]['attr']:
                self.tag[-1].set(attr, dictionary[entry]['attr'][attr])
            if len(dictionary[entry]['children']) > 0:
                self.__dict2xml(self.tag[-1], dictionary[entry]['children'])

    def replaceTxt(self, value, xpath=".", occurance=-1):
        if self.tree is None:
            self.tree = ET.parse(self.inputfile)
        root = self.tree.getroot()
        find_xpath = root.findall(xpath)
        for i, entry in enumerate(find_xpath):
            if occurance < 0:
                entry.text = str(value)
            elif i == occurance:
                entry.text = str(value)

    def _getParameterPointer(self, root, name, xpath):
        parameters = root.findall(xpath)
        parameterpointer = None
        for parameter in parameters:
            for paramproperty in parameter:
                if paramproperty.tag == "name":
                    if paramproperty.text == name:
                        parameterpointer = parameter
        if parameterpointer is None:
            print("Parameter/Property not found")
            raise RuntimeError
        return parameterpointer

    def _getMediumPointer(self, root, mediumid):
        xpathmedia = "./media/medium"
        media = root.findall(xpathmedia)
        mediumpointer = None
        for medium in media:
            if medium.attrib['id'] == str(mediumid):
                mediumpointer = medium
        if mediumpointer is None:
            print("Medium not found")
            raise RuntimeError
        return mediumpointer

    def _getPhasePointer(self, root, phase):
        phases = root.findall("./phases/phase")
        phasetypes = root.findall("./phases/phase/type")
        phasecounter = None
        for i, phasetype in enumerate(phasetypes):
            if phasetype.text == phase:
                phasecounter = i
        phasepointer = phases[phasecounter]
        if phasepointer is None:
            print("Phase not found")
            raise RuntimeError
        return phasepointer

    def _setTypeValue(self, parameterpointer, value, values, parametertype):
        for paramproperty in parameterpointer:
            if paramproperty.tag == "value":
                if not value is None:
                    paramproperty.text = str(value)
            elif paramproperty.tag == "values":
                if not value is None:
                    paramproperty.text = str(values)
            elif paramproperty.tag == "type":
                if not parametertype is None:
                    paramproperty.text = str(parametertype)

    def replaceParameter(self, name=None, value=None, values=None, parametertype=None):
        if self.tree is None:
            self.tree = ET.parse(self.inputfile)
        root = self.tree.getroot()
        parameterpath = "./parameters/parameter"
        parameterpointer = self._getParameterPointer(root, name, parameterpath)
        self._setTypeValue(parameterpointer, value, values, parametertype)

    def replacePhaseProperty(self, mediumid=None, phase="AqueousLiquid", name=None, value=None, propertytype=None):
        if self.tree is None:
            self.tree = ET.parse(self.inputfile)
        root = self.tree.getroot()
        mediumpointer = self._getMediumPointer(root, mediumid)
        phasepointer = self._getPhasePointer(mediumpointer, phase)
        xpathparameter = "./properties/property"
        parameterpointer = self._getParameterPointer(phasepointer, name, xpathparameter)
        self._setTypeValue(parameterpointer, value, None, propertytype)

    def replaceMediumProperty(self, mediumid=None, name=None, value=None, propertytype=None):
        if self.tree is None:
            self.tree = ET.parse(self.inputfile)
        root = self.tree.getroot()
        mediumpointer = self._getMediumPointer(root, mediumid)
        xpathparameter = "./properties/property"
        parameterpointer = self._getParameterPointer(mediumpointer, name, xpathparameter)
        self._setTypeValue(parameterpointer, value, None, propertytype)

    def writeInput(self):
        if not self.tree is None:
            self.tree.write(self.prjfile,
                            encoding="ISO-8859-1",
                            xml_declaration=True,
                            pretty_print=True)
            return True
        else:
            self.root = ET.Element("OpenGeoSysProject")
            if len(self.geo.tree['geometry']['text']) > 0:
                self.__dict2xml(self.root, self.geo.tree)
            self.__dict2xml(self.root, self.mesh.tree)
            if len(self.pyscript.tree['pythonscript']['text']) > 0:
                self.__dict2xml(self.root, self.pyscript.tree)
            self.__dict2xml(self.root, self.processes.tree)
            if len(self.media.tree['media']['children']) > 0:
                self.__dict2xml(self.root, self.media.tree)
            self.__dict2xml(self.root, self.timeloop.tree)
            if len(self.local_coordinate_system.tree['local_coordinate_system']['children']) > 0:
                self.__dict2xml(self.root, self.local_coordinate_system.tree)
            self.__dict2xml(self.root, self.parameters.tree)
            if len(self.curves.tree['curves']['children']) > 0:
                self.__dict2xml(self.root, self.curves.tree)
            self.__dict2xml(self.root, self.processvars.tree)
            self.__dict2xml(self.root, self.nonlinsolvers.tree)
            self.__dict2xml(self.root, self.linsolvers.tree)
            # Reparsing for pretty_print to work properly
            parser = ET.XMLParser(remove_blank_text=True)
            self.tree_string = ET.tostring(self.root, pretty_print=True)
            self.tree = ET.fromstring(self.tree_string, parser=parser)
            self.tree_ = ET.ElementTree(self.tree)
            self.tree_.write(self.prjfile,
                         encoding="ISO-8859-1",
                         xml_declaration=True,
                         pretty_print=True)
            return True


