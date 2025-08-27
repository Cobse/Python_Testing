# -*- coding: utf-8 -*-

# PDF Merger Tool
import os
from PyPDF2 import PdfMerger

# Create a method that takes a path and get all the pdf files in this path.
# Merge all the pdf files into a new single pdf file. This should happen in the same directory.

def merge_pdfs_in_directory(directory_path, output_filename="merged_output.pdf"):


    # Create a PdfMerger object
    merger = PdfMerger()

    # List all files in the given directory
    for item in os.listdir(directory_path):
        if item.lower().endswith('.pdf'):
            pdf_path = os.path.join(directory_path, item)
            merger.append(pdf_path)

    # Define the output path
    output_path = os.path.join(directory_path, output_filename)

    # Write out the merged PDF
    merger.write(output_path)
    merger.close()

    print(f"Merged PDF saved as: {output_path}")

dir_path = r"G:\My Drive\Privat\Støttemur\Nabovarsel\Nabovarsel_kvitteringer"

merge_pdfs_in_directory(dir_path)