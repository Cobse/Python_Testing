import os
from base64_utils import encode_pdf_to_base64, decode_base64_to_pdf

if __name__ == "__main__":
    # Example usage
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print("Current script path:", script_dir)

    # print files in the current directory
    print("Files in current directory:", os.listdir(script_dir))

    # Use absolute paths for the files
    pdf_path = os.path.join(script_dir, 'COWI-NO-BRU_formkoder_NY.pdf')
    encoded_path = os.path.join(script_dir, 'encoded.txt')
    decoded_path = os.path.join(script_dir, 'decoded.pdf')

    encode_pdf_to_base64(pdf_path, encoded_path)
    decode_base64_to_pdf(encoded_path, decoded_path)

    png_path = os.path.join(script_dir, 'test.png')
    encoded_path = os.path.join(script_dir, 'encoded_png.txt')
    decoded_path = os.path.join(script_dir, 'decoded.png')

    encode_pdf_to_base64(png_path, encoded_path)
    decode_base64_to_pdf(encoded_path, decoded_path)

    pdf_path = os.path.join(script_dir, 'Presentation1.pdf')
    encoded_path = os.path.join(script_dir, 'encoded_Presentation1.txt')
    decoded_path = os.path.join(script_dir, 'decoded_Presentation1.pdf')
    
    encode_pdf_to_base64(pdf_path, encoded_path)
    decode_base64_to_pdf(encoded_path, decoded_path)

    pdf_path = os.path.join(script_dir, 'drawing.pdf')
    encoded_path = os.path.join(script_dir, 'encoded_drawing.txt')
    decoded_path = os.path.join(script_dir, 'decoded_drawing.pdf')

    encode_pdf_to_base64(pdf_path, encoded_path)
    decode_base64_to_pdf(encoded_path, decoded_path)

    
    pdf_path = os.path.join(script_dir, 'K100_001.pdf')
    encoded_path = os.path.join(script_dir, 'encoded_K100_001.txt')
    decoded_path = os.path.join(script_dir, 'decoded_K100_001.pdf')

    encode_pdf_to_base64(pdf_path, encoded_path)
    decode_base64_to_pdf(encoded_path, decoded_path)

