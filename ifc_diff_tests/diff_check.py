import os
from pathlib import Path
from ifcdiff import IfcDiff
import ifcopenshell
import ifcdiff

# Get the ifc_files folder path
# Get the current python file path
current_file_path = Path(__file__).resolve()

# ifc_files_path = os.getcwd()  # Get the current working directory
ifc_files_path = os.path.join(current_file_path.parent, "ifc_files")

# Get all IFC files in the folder
old_file_name = r"SOS_20KOL_F_KON_Støttemur.ifc"
new_file_name = r"SOS_20KOL_F_KON_Støttemur_09C.ifc"

old_path = os.path.join(ifc_files_path, old_file_name)
new_path = os.path.join(ifc_files_path, new_file_name)

json_path = os.path.join(ifc_files_path, "diff_result.json")
export_path = os.path.join(ifc_files_path, "diff_result.ifc")

# Check if the files exist
if not os.path.exists(old_path):
    print(f"Error: Old IFC file not found at {old_path}")
    exit(1)

if not os.path.exists(new_path):
    print(f"Error: New IFC file not found at {new_path}")
    exit(1)

# relationship_types = set()
relationships = []
relationships.append("property")

old_ifc = ifcopenshell.open(old_path)
new_ifc = ifcopenshell.open(new_path)

ifc_diff = IfcDiff(old_ifc, new_ifc, relationships)

try:
    ifc_diff.diff()
    # ifc_diff.diff_element_relationships(old_ifc, new_ifc)
except Exception as e:
    print(f"Error during diffing: {e}")

print(ifc_diff.change_register)

# Get the folder from json_path
folder_path = os.path.dirname(json_path)
ifc_diff.export(json_path)