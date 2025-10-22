import cv2
import numpy as np

def remove_watermark_advanced(image_path, output_path):
    """
    Remove repeating text watermarks with varying grayscale values.
    Uses edge detection and morphological operations to create a mask.
    """
    # Read the image
    img = cv2.imread(image_path)
    
    if img is None:
        print(f"Error: Could not read image from {image_path}")
        return
    
    print(f"Image loaded: {img.shape}")
    height, width = img.shape[:2]
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Create mask focusing on bottom half where watermarks are
    mask = np.zeros_like(gray)
    
    # Focus on bottom half of image (y/2 to bottom)
    roi_y_start = height // 2
    roi = gray[roi_y_start:, :]
    
    # Method 1: Detect text edges using Canny
    edges = cv2.Canny(roi, 50, 150)
    
    # Dilate edges to connect text regions
    kernel = np.ones((3, 3), np.uint8)
    edges_dilated = cv2.dilate(edges, kernel, iterations=2)
    
    # Method 2: Detect varying grayscale watermarks using adaptive thresholding
    # This works better for text with varying intensities
    adaptive = cv2.adaptiveThreshold(roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY_INV, 15, 2)
    
    # Combine both methods
    combined = cv2.bitwise_or(edges_dilated, adaptive)
    
    # Clean up noise - remove small artifacts
    kernel_cleanup = np.ones((2, 2), np.uint8)
    combined = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel_cleanup)
    combined = cv2.morphologyEx(combined, cv2.MORPH_OPEN, kernel_cleanup)
    
    # Place the ROI mask back into full mask
    mask[roi_y_start:, :] = combined
    
    # Dilate the final mask slightly to ensure full watermark coverage
    mask = cv2.dilate(mask, kernel, iterations=1)
    
    # Apply inpainting using Navier-Stokes based method (better for larger areas)
    result = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
    
    # Save the result
    cv2.imwrite(output_path, result)
    print(f"Watermark removed. Output saved to: {output_path}")
    
    # Save the mask for inspection
    mask_path = output_path.replace('.jpg', '_mask.jpg')
    cv2.imwrite(mask_path, mask)
    print(f"Mask saved to: {mask_path}")
    
    # Save edge detection result for debugging
    debug_path = output_path.replace('.jpg', '_debug.jpg')
    debug_img = np.zeros_like(img)
    debug_img[roi_y_start:, :] = cv2.cvtColor(combined, cv2.COLOR_GRAY2BGR)
    cv2.imwrite(debug_path, debug_img)
    print(f"Debug image saved to: {debug_path}")

if __name__ == "__main__":
    input_image = "Images/2025_2C.jpg"
    output_image = "Images/2025_2C_no_watermark_v2.jpg"
    
    remove_watermark_advanced(input_image, output_image)
