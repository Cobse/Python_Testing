import os
from PyPDF2 import PdfReader


pdf_file_name = "K100_001.pdf"
pdf_file_path = os.path.join("base64", pdf_file_name)

temp_values = None

# Read the pdf file and get the title
def read_pdf_title(pdf_path):
    """
    Reads the title from a PDF file.
    """
    try:
        reader = PdfReader(pdf_path)
        if reader.pages:
            temp_values = reader.metadata.values
            return reader.metadata.title_raw or "No Title Found"
        else:
            return "No Pages Found"
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return "Error Reading PDF"
    
output = read_pdf_title(pdf_file_path)
print(f"PDF Title: {output}")
print(f"PDF Metadata: {temp_values}")