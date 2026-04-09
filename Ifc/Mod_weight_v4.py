import re
import ifcopenshell
import os

# ----------------------------
# SETTINGS
# ----------------------------
INPUT_IFC = "f-bru_K34-Sakariasjordet_overgangsbru_Armering.ifc"
OUTPUT_IFC = "f-bru_K34-Sakariasjordet_overgangsbru_Armering_edited_H.ifc"

# Source
SOURCE_PSET = "Merknader"
SOURCE_PROP = "R08 Total vekt (kg)"

# Special condition
CHECK_PSET = "Prosessinfo"
CHECK_PROP = "P06 Enhet"
CHECK_VALUE = "stk"

# Target
TARGET_PSET = "Prosessinfo"
TARGET_PROP = "P05 Mengde"



def get_pset_relation(element, pset_name):
    """Return the IfcRelDefinesByProperties and IfcPropertySet for the object."""
    if not hasattr(element, "IsDefinedBy"):
        return None, None

    for rel in element.IsDefinedBy or []:
        if not rel.is_a("IfcRelDefinesByProperties"):
            continue
        pset = rel.RelatingPropertyDefinition
        if pset and pset.is_a("IfcPropertySet") and pset.Name == pset_name:
            return rel, pset
    return None, None


def get_pset(element, pset_name):
    """Return IfcPropertySet by name, or None."""
    _, pset = get_pset_relation(element, pset_name)
    return pset


def get_pset_property(pset, prop_name):
    """Return IfcPropertySingleValue by name, or None."""
    if not pset:
        return None

    for prop in pset.HasProperties or []:
        if prop.is_a("IfcPropertySingleValue") and prop.Name == prop_name:
            return prop
    return None


def get_pset_property_value(element, pset_name, prop_name):
    """Read wrapped IFC property value."""
    pset = get_pset(element, pset_name)
    prop = get_pset_property(pset, prop_name)
    if not prop or prop.NominalValue is None:
        return None
    return prop.NominalValue.wrappedValue


def create_pset(model, element, pset_name):
    """Create a new property set and assign it to the element."""
    owner_history = model.by_type("IfcOwnerHistory")
    owner_history = owner_history[0] if owner_history else None

    pset = model.create_entity(
        "IfcPropertySet",
        ifcopenshell.guid.new(),
        owner_history,
        pset_name,
        None,
        []
    )

    model.create_entity(
        "IfcRelDefinesByProperties",
        ifcopenshell.guid.new(),
        owner_history,
        None,
        None,
        [element],
        pset
    )
    return pset


def get_or_create_pset(model, element, pset_name):
    pset = get_pset(element, pset_name)
    if pset:
        return pset
    return create_pset(model, element, pset_name)


def clone_nominal_value(model, nominal_value):
    """Clone an IFC simple value entity."""
    if nominal_value is None:
        return None
    return model.create_entity(nominal_value.is_a(), nominal_value.wrappedValue)


def clone_property(model, prop):
    """Clone a single-value IFC property."""
    if not prop.is_a("IfcPropertySingleValue"):
        return None

    return model.create_entity(
        "IfcPropertySingleValue",
        prop.Name,
        prop.Description,
        clone_nominal_value(model, prop.NominalValue),
        prop.Unit
    )


def ensure_writable_pset(model, element, pset_name):
    """Return a property set that can be safely modified for this object."""
    rel, pset = get_pset_relation(element, pset_name)
    if not pset:
        return create_pset(model, element, pset_name), False

    related_objects = list(rel.RelatedObjects or [])
    if len(related_objects) <= 1:
        return pset, False

    cloned_pset = create_pset(model, element, pset_name)
    cloned_properties = []
    for prop in pset.HasProperties or []:
        cloned_prop = clone_property(model, prop)
        if cloned_prop:
            cloned_properties.append(cloned_prop)
    cloned_pset.HasProperties = cloned_properties

    rel.RelatedObjects = [obj for obj in related_objects if obj.id() != element.id()]
    return cloned_pset, True


def set_real_property(model, element, pset_name, prop_name, value):
    """
    Force TARGET_PROP to IfcReal.
    value must be a Python float.
    """
    pset, was_split = ensure_writable_pset(model, element, pset_name)
    prop = get_pset_property(pset, prop_name)

    nominal_value = model.create_entity("IfcReal", float(value))

    if prop:
        prop.NominalValue = nominal_value
    else:
        new_prop = model.create_entity(
            "IfcPropertySingleValue",
            prop_name,
            None,
            nominal_value,
            None
        )
        props = list(pset.HasProperties) if pset.HasProperties else []
        props.append(new_prop)
        pset.HasProperties = props

    return was_split


def clean_number(value):
    """
    Convert IFC/text value to float robustly.
    Handles:
    - 12000
    - 12000.0
    - "12000"
    - "12,000"
    - "12 000"
    - "12000 mm"
    - "12000,5"
    """
    if value is None:
        return None

    if isinstance(value, (int, float)):
        return float(value)

    s = str(value).strip()

    if not s:
        return None

    # Remove unit text except digits, comma, dot, minus
    s = re.sub(r"[^0-9,.\-]", "", s)

    if not s:
        return None

    # Decide decimal separator
    # If both comma and dot exist, assume comma is thousands separator
    if "," in s and "." in s:
        s = s.replace(",", "")
    # If only comma exists, assume decimal comma
    elif "," in s:
        s = s.replace(",", ".")

    try:
        return float(s)
    except ValueError:
        return None


def main():
    script_folder = os.path.dirname(os.path.abspath(__file__))
    input_candidates = [INPUT_IFC, os.path.join(script_folder, INPUT_IFC)]
    input_path = next((path for path in input_candidates if os.path.exists(path)), None)

    if not input_path:
        print(f"Error: Input IFC file not found at {input_candidates[0]} or {input_candidates[1]}")
        return

    output_path = OUTPUT_IFC
    if not os.path.isabs(output_path):
        output_path = os.path.join(script_folder, OUTPUT_IFC)

    print(f"Input IFC: {input_path}")

    model = ifcopenshell.open(input_path)
    elements = model.by_type("IfcObject")


    count_total = 0
    count_updated = 0
    count_stk = 0
    count_skipped = 0
    count_failed_parse = 0
    count_split = 0

    for element in elements:
        count_total += 1

        source_value = get_pset_property_value(element, SOURCE_PSET, SOURCE_PROP)
        unit_value = get_pset_property_value(element, CHECK_PSET, CHECK_PROP)

        # Rule: if "Stk", write 1.0 as float
        if str(unit_value).strip() == CHECK_VALUE:
            was_split = set_real_property(
                model,
                element,
                TARGET_PSET,
                TARGET_PROP,
                1.0
            )
            count_updated += 1
            count_stk += 1
            if was_split:
                count_split += 1
            continue

        cleaned = clean_number(source_value)
        if cleaned is None:
            if source_value is None:
                count_skipped += 1
            else:
                count_failed_parse += 1
            continue

        new_value = cleaned / 1000.0

        was_split = set_real_property(
            model,
            element,
            TARGET_PSET,
            TARGET_PROP,
            float(new_value)
        )
        count_updated += 1
        if was_split:
            count_split += 1

    model.write(output_path)

    print(f"Processed:      {count_total}")
    print(f"Updated:        {count_updated}")
    print(f"Stk -> 1.0:     {count_stk}")
    print(f"Split target:   {count_split}")
    print(f"Skipped empty:  {count_skipped}")
    print(f"Failed parse:   {count_failed_parse}")
    print(f"Saved as:       {output_path}")


if __name__ == "__main__":
    main()