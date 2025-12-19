


def calculate_checksum(bvbs_without_checksum: str) -> str:
    """
    Calculate checksum for BVBS line using ASCII values.
    
    Args:
        bvbs_without_checksum (str): Input string without checksum
    
    Returns:
        str: Calculated checksum as string
    """
    # Convert string to ASCII bytes and sum them
    sum_bytes = sum(ord(char) for char in bvbs_without_checksum)
    
    # Calculate checksum: 96 - (sum modulo 32)
    checksum = 96 - (sum_bytes % 32)
    
    return str(checksum)


input_string = "BF2D@Hj123@rCP-32@i0@pG1-01-2/1500.1@l6300@n6@e9.94@d16@gB500NC@s50@a0@t0@Gl6300@w0@C"
# Curved rebar test case
input_string = "BF2D@HjTestPDF@r417@ia@p1@l12000@n10@e1.268@d12@gB500A@s48@v@Gl100@w0@r8402.5@w81.82676@w100@l0@w0@C"
# Curved rebar test case with different length
input_string = "BF2D@r8082@HjA267920@w85@rCP-0(?)@i0@pF4-1/1000@l12000@n3@e46.24@d25@gB500NC@s125@a0@t0@Gl0@r8082@w85@C"

#input_string = "BF2D@Hj123@rCP-1135(?)@i0@pOb1100@l5000@n128@e19.28@d25@gB500NC@s125@a0@t0@Gl375@w90@l3920@w180@l215@w0@C"


# Example usage
checksum = calculate_checksum(input_string)
print(f"Checksum for '{input_string}' with length: '{len(input_string)}'  is: {checksum}")