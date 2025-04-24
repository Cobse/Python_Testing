#!/usr/bin/python
# -*- coding: utf-8 -*-

# This section is common to all Python task scripts. 
import clr
import System

clr.AddReference("RevitAPI")
clr.AddReference("RevitAPIUI")
clr.AddReference(r"C:\ProgramData\Autodesk\Revit\Addins\2023\RhinoInside.Revit\R7\RhinoInside.Revit.dll")
# Import Grasshopper
from RhinoInside.Revit import Revit, GH_Document

from Autodesk.Revit.DB import *

import revit_script_util
from revit_script_util import Output
from Autodesk.Revit.UI import RevitCommandId

sessionId = revit_script_util.GetSessionId()
uiapp = revit_script_util.GetUIApplication()

doc = revit_script_util.GetScriptDocument()
revitFilePath = revit_script_util.GetRevitFilePath()

#######################
## Script Start #######
#######################
Output("Starting Rhino.Inside.Revit...")

try:
    # Output all loaded add-ins
    for app in uiapp.LoadedApplications:
        addin_name = app.GetType().Name
        assembly_location = app.GetType().Assembly.Location
        Output("Add-in Name: {}".format(addin_name))
        Output("Add-in Path: {}".format(assembly_location))

    # Path to the Grasshopper definition
    gh_path = "C:\\Users\\FKJN\\Downloads\\Message.gh"

    # Start Rhino.Inside.Revit 

    # Load the Grasshopper definition
    gh_doc = GH_Document.LoadFromFilePath(gh_path)
    Output("Grasshopper definition loaded successfully.")




except Exception as e:
    Output("An error occurred: {}".format(e))