import ifcpatch
import ifcopenshell
import os

file_path = r"C:\Users\fkjn\Downloads\Mandalselsva\f-bru_K100_Mandalselva-bru_merged - Copy.ifc"

# Check if ifc files exist
if not os.path.exists(file_path):
    print(f"✗ IFC file not found: {file_path}")
    exit(1)

# Use IfcPatch to mergeDuplicateTypes
# Syntax: ifcpatch.execute({"input": "input.ifc", "file": model, "recipe": "MergeDuplicateTypes"})
print("Merging duplicate types in IFC file...")
input_model = ifcopenshell.open(file_path)

merged_model = ifcpatch.execute({
    "input": file_path,
    "file": input_model,
    "recipe": "MergeDuplicateTypes",
    "arguments": ["Name"]
})


merged_model.write(file_path.replace(".ifc", "_merged_dup.ifc"))
