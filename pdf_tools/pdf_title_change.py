
import os
from PyPDF2 import PdfReader, PdfWriter

# Take the pdf file in pdf_input folder and change the pdf title in the pdf metadata

script_dir = os.path.dirname(os.path.abspath(__file__))
input_file = os.path.join(script_dir, "pdf_input", "NV42E39MB-KNS-K107 Mandalselva bru - IDV Plan.pdf")

# Check if the input file exists
if not os.path.exists(input_file):
    print(f"Input file '{input_file}' does not exist.")
    exit(1)

# Get the pdf file name without extension
file_name = os.path.splitext(os.path.basename(input_file))[0]

# Read the existing PDF
reader = PdfReader(input_file)
writer = PdfWriter()
writer.append_pages_from_reader(reader)
# Update the metadata
metadata = reader.metadata
metadata.update({
    "/Title": f"{file_name}"
})

output_dir = os.path.join(script_dir, "pdf_output")
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, f"{file_name}.pdf")

# Write the updated PDF to a new file
with open(output_file, "wb") as f:
    writer.write(f)
print(f"Updated PDF saved as '{output_file}' with title '{file_name}'")