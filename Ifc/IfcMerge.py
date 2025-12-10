import ifcopenshell
import ifcopenshell.api
import ifcpatch
import os



ifc_folder_path = r"C:\Users\fkjn\Downloads\Mandalselsva"

ifc_substructure = "f-bru_K100_Mandalselva-bru_substructure.ifc"
ifc_superstructure = "f-bru_K100_Mandalselva-bru_superstructure.ifc"
ifc_merged_output = "f-bru_K100_Mandalselva-bru_merged.ifc"


# Check if ifc files exist
if not os.path.exists(os.path.join(ifc_folder_path, ifc_substructure)):
    print(f"✗ IFC substructure file not found: {ifc_substructure}")
    exit(1)

if not os.path.exists(os.path.join(ifc_folder_path, ifc_superstructure)):
    print(f"✗ IFC superstructure file not found: {ifc_superstructure}")
    exit(1)

# Use IfcPatch to merge the IFC files
# Syntax: ifcpatch.execute({"input": "input.ifc", "file": model, "recipe": "MergeProjects", "arguments": ["/path/to/model2.ifc"]})
print("Merging IFC files...")
ifc_substructure_path = os.path.join(ifc_folder_path, ifc_substructure)
ifc_superstructure_path = os.path.join(ifc_folder_path, ifc_superstructure)
ifc_merged_output_path = os.path.join(ifc_folder_path, ifc_merged_output)

#input_substructure_model = ifcopenshell.open(ifc_substructure_path)
#input_superstructure_model = ifcopenshell.open(ifc_superstructure_path)

# Load the substructure model (this will be the base model)
base_model = ifcopenshell.open(ifc_substructure_path)

merged_model = ifcpatch.execute({
    "input": ifc_substructure_path,
    "file": base_model,
    "recipe": "MergeProjects",
    "arguments": [ifc_superstructure_path]
})

# Save the merged IFC model
merged_model.write(ifc_merged_output_path)
print(f"✓ Merged IFC file saved to: {ifc_merged_output_path}")