


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

# Example usage
checksum = calculate_checksum(input_string)
print(f"Checksum for '{input_string}' with length: '{len(input_string)}'  is: {checksum}")