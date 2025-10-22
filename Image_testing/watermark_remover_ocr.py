import cv2
import numpy as np
import easyocr

def remove_watermark_ocr(image_path, output_path):
    """
    Remove watermarks using OCR to detect text locations precisely.
    Uses EasyOCR to find 'NORSK SKOLEFOTO' text and inpaint only those areas.
    """
    # Read the image
    img = cv2.imread(image_path)
    
    if img is None:
        print(f"Error: Could not read image from {image_path}")
        return
    
    print(f"Image loaded: {img.shape}")
    height, width = img.shape[:2]
    
    # Initialize EasyOCR reader
    print("Initializing OCR...")
    reader = easyocr.Reader(['no', 'en'], gpu=False)
    
    # Detect text in the image
    print("Detecting text...")
    results = reader.readtext(image_path)
    
    # Create a mask for watermark regions
    mask = np.zeros((height, width), dtype=np.uint8)
    
    watermark_count = 0
    for (bbox, text, prob) in results:
        # Look for watermark text
        text_upper = text.upper()
        if 'NORSK' in text_upper or 'SKOLEFOTO' in text_upper or 'ARIEL' in text_upper or 'FOTO NORDEN' in text_upper or 'NORDEN' in text_upper:
            print(f"Found watermark text: {text} (confidence: {prob:.2f})")
            
            # Get bounding box coordinates
            top_left = tuple(map(int, bbox[0]))
            top_right = tuple(map(int, bbox[1]))
            bottom_right = tuple(map(int, bbox[2]))
            bottom_left = tuple(map(int, bbox[3]))
            
            # Draw filled polygon on mask with some padding
            pts = np.array([top_left, top_right, bottom_right, bottom_left], np.int32)
            cv2.fillPoly(mask, [pts], 255)
            
            # Add padding around detected text
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.dilate(mask, kernel, iterations=1)
            
            watermark_count += 1
    
    print(f"Detected {watermark_count} watermark regions")
    
    if watermark_count == 0:
        print("No watermarks detected. Trying alternative approach...")
        # Fallback: detect brackets and text in bottom half
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        roi_y_start = height // 2
        roi = gray[roi_y_start:, :]
        
        # Detect edges more conservatively
        edges = cv2.Canny(roi, 100, 200)
        kernel = np.ones((2, 2), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        
        mask[roi_y_start:, :] = edges
    
    # Apply inpainting
    result = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
    
    # Save the result
    cv2.imwrite(output_path, result)
    print(f"Watermark removed. Output saved to: {output_path}")
    
    # Save the mask for inspection
    mask_path = output_path.replace('.jpg', '_mask.jpg')
    cv2.imwrite(mask_path, mask)
    print(f"Mask saved to: {mask_path}")

if __name__ == "__main__":
    input_image = "Images/2025_2C.jpg"
    output_image = "Images/2025_2C_no_watermark_ocr.jpg"
    
    remove_watermark_ocr(input_image, output_image)
