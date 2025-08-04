import base64

def encode_pdf_to_base64(pdf_path, output_path):
    try:
        with open(pdf_path, 'rb') as pdf_file:
            encoded = base64.b64encode(pdf_file.read())
        with open(output_path, 'wb') as out_file:
            out_file.write(encoded)
    except Exception as e:
        print(f"Error encoding PDF to base64: {e}")

def decode_base64_to_pdf(encoded_path, output_path):
    try:
        with open(encoded_path, 'rb') as encoded_file:
            decoded = base64.b64decode(encoded_file.read())
        with open(output_path, 'wb') as pdf_file:
            pdf_file.write(decoded)
    except Exception as e:
        print(f"Error decoding base64 to PDF: {e}")


# Example usage:
# encode_pdf_to_base64('example.pdf', 'encoded.txt')
# decode_base64_to_pdf('encoded.txt', 'decoded.pdf')

