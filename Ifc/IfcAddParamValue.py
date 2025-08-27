#!/usr/bin/env python3
"""
Script to add a base64 parameter to all objects in an IFC model using ifcopenshell.

This script:
1. Loads an IFC model
2. Reads base64 data from a text file
3. Creates a property set with base64 parameters
4. Adds this property set to all objects in the model except IfcReinforcingBar
5. Saves the modified model
"""

import ifcopenshell
import ifcopenshell.api
import os
import sys


def load_base64_data(file_path):
    """
    Load base64 data from a text file.
    
    Args:
        file_path (str): Path to the base64 encoded text file
        
    Returns:
        str: Base64 encoded string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            base64_data = file.read().strip()
        print(f"✓ Successfully loaded base64 data from {file_path}")
        print(f"  Data length: {len(base64_data)} characters")

        # Split base64_data into a list with max 4000 characters per item
        base64_data = [base64_data[i:i + 4000] for i in range(0, len(base64_data), 4000)]

        print(f"  Split into {len(base64_data)} chunks of max 4000 characters")

        return base64_data
    except FileNotFoundError:
        print(f"✗ Error: File {file_path} not found")
        return None
    except Exception as e:
        print(f"✗ Error reading base64 file: {e}")
        return None


def create_property_set(model, name, description=""):
    """
    Create a property set template in the IFC model.
    
    Args:
        model: IFC model object
        name (str): Name of the property set
        description (str): Description of the property set
        
    Returns:
        Property set object
    """
    try:
        # Create a property set
        property_set = ifcopenshell.api.run("pset.add_pset", model, 
                                          name=name, 
                                          description=description)
        print(f"✓ Created property set: {name}")
        return property_set
    except Exception as e:
        print(f"✗ Error creating property set: {e}")
        return None


def add_base64_parameter_to_objects(model, base64_data):
    """
    Add base64 parameter to all objects in the IFC model.
    
    Args:
        model: IFC model object
        base64_data (str): Base64 encoded string to add as parameter
        
    Returns:
        int: Number of objects that had the parameter added
    """
    objects_modified = 0
    
    # Get all objects that can have properties (typically building elements)
    # This includes walls, slabs, beams, columns, etc.
    # property_capable_objects = model.by_type("IfcObject")
    property_capable_objects = model.by_type("IfcBuilding")
    
    print(f"Found {len(property_capable_objects)} objects in the model")
    
    # Filter out objects that are not suitable for adding properties
    # For example, we might want to skip IfcReinforcingBar or other specific types
    # Here we assume that all IfcObject types are suitable, but you can customize this
    # Note: If you want to filter specific types, you can modify this section
    # For example, to skip IfcReinforcingBar:
    property_capable_objects = [obj for obj in property_capable_objects if not obj.is_a("IfcReinforcingBar")]



    print(f"Filtered to {len(property_capable_objects)} suitable objects for adding properties")
    if not property_capable_objects:
        print("✗ No suitable objects found for adding properties")
        return 0
    
     # Add the pset to the first object to create a template
    pset = ifcopenshell.api.run("pset.add_pset", 
                                          model, 
                                          product=property_capable_objects[0], 
                                          name="BIM_Base64")
    
    if not pset:
        print("✗ Failed to create property set for base64 data")
        return 0
    print(f"✓ Created property set 'BIM_Base64' for base64 data")

    # Assign the pset to all suitable objects
    print(f"Adding base64 parameter to {len(property_capable_objects)} objects...")
    pset_assigned = ifcopenshell.api.run("pset.assign_pset", 
                                                     model,
                                                     pset=pset, 
                                                     products=property_capable_objects)

    if not pset_assigned:
        print("✗ Failed to assign property set to objects")
        return 0
    print(f"✓ Assigned property set 'BIM_Base64' to {len(property_capable_objects)} objects")

    # Add the base64 property to the property set
    _iter = 1
    try:
        for chunk in base64_data:
            ifcopenshell.api.run("pset.edit_pset", model, 
                                pset=pset, 
                                properties={f"Base64_{1}.{_iter}": chunk})
            _iter += 1
        objects_modified = len(property_capable_objects)
    except Exception as e:
        print(f"✗ Error adding base64 data to property set: {e}")
        return 0
    
    print(f"✓ Successfully added base64 parameter to {objects_modified} objects")
    return objects_modified


def main():
    """
    Main function to execute the script.
    """
    # Define file paths
    ifc_file_name = "Mandalselva.ifc"
    ifc_file_path = os.path.join("ifc", ifc_file_name)
    base64_file_path = os.path.join("base64", "encoded_K100_001.txt")
    output_file_path = os.path.join("ifc", "Mandalselva_base64_test.ifc")
    
    print("=" * 60)
    print("IFC Base64 Parameter Addition Script")
    print("=" * 60)
    
    # Check if IFC file exists
    if not os.path.exists(ifc_file_path):
        print(f"✗ Error: IFC file {ifc_file_path} not found in current directory")
        print(f"Current directory: {os.getcwd()}")
        return False
    
    # Load base64 data
    print(f"\n1. Loading base64 data from: {base64_file_path}")
    base64_data = load_base64_data(base64_file_path)
    if not base64_data:
        return False
    
    # Load IFC model
    print(f"\n2. Loading IFC model: {ifc_file_path}")
    try:
        model = ifcopenshell.open(ifc_file_path)
        print(f"✓ Successfully loaded IFC model")
        print(f"  Schema: {model.schema}")
        print(f"  Total entities: {len(list(model))}")
    except Exception as e:
        print(f"✗ Error loading IFC model: {e}")
        return False
    
    # Add base64 parameter to all objects
    print(f"\n3. Adding base64 parameter to all objects...")
    objects_modified = add_base64_parameter_to_objects(model, base64_data)
    
    if objects_modified == 0:
        print("✗ No objects were modified. Check if the model contains valid objects.")
        return False
    
    # Save the modified model
    print(f"\n4. Saving modified model: {output_file_path}")
    try:
        model.write(output_file_path)
        print(f"✓ Successfully saved modified model to {output_file_path}")
    except Exception as e:
        print(f"✗ Error saving model: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("✓ Script completed successfully!")
    print(f"✓ Modified {objects_modified} objects")
    print(f"✓ Output file: {output_file_path}")
    print("=" * 60)
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
