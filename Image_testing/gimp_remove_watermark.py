#!/usr/bin/env python3
"""
GIMP script to remove watermarks using heal selection
Run with: gimp-console-3.0 -idf --batch-interpreter python-fu-eval -b - < gimp_remove_watermark.py
"""

import sys

# GIMP Script-Fu code
gimp_script = '''
from gimpfu import *
import os

def remove_watermark(input_file, mask_file, output_file):
    # Load the image
    image = pdb.gimp_file_load(input_file, input_file)
    drawable = pdb.gimp_image_get_active_layer(image)
    
    # Load mask as layer
    mask_layer = pdb.gimp_file_load_layer(image, mask_file)
    pdb.gimp_image_insert_layer(image, mask_layer, None, 0)
    
    # Convert mask to selection
    pdb.gimp_image_select_item(image, 2, mask_layer)  # 2 = CHANNEL_OP_REPLACE
    
    # Remove the mask layer
    pdb.gimp_image_remove_layer(image, mask_layer)
    
    # Use heal selection (like content-aware fill)
    pdb.python_fu_heal_selection(image, drawable, 50, 0, 0)
    
    # Save the result
    pdb.gimp_file_save(image, drawable, output_file, output_file)
    
    # Clean up
    pdb.gimp_image_delete(image)

# Main execution
input_img = r"E:\\Github\\Python_Testing\\Image_testing\\Images\\2025_2C.jpg"
mask_img = r"E:\\Github\\Python_Testing\\Image_testing\\Images\\2025_2C_patchmatch_mask.jpg"  
output_img = r"E:\\Github\\Python_Testing\\Image_testing\\Images\\2025_2C_gimp.jpg"

remove_watermark(input_img, mask_img, output_img)

pdb.gimp_quit(0)
'''

print(gimp_script)
