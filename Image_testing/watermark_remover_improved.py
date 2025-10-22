import cv2
import numpy as np

def remove_watermark_improved(image_path, output_path):
    """
    Improved watermark removal with better inpainting
    """
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    
    print(f"Image size: {width}x{height}")
    
    # Convert to different color spaces
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Create mask - focus on bottom half
    mask = np.zeros((height, width), dtype=np.uint8)
    roi_y_start = height // 2
    
    # Extract ROI
    roi_gray = gray[roi_y_start:, :]
    roi_hsv = hsv[roi_y_start:, :]
    
    # Detect gray text (low saturation, varying value)
    saturation = roi_hsv[:, :, 1]
    value = roi_hsv[:, :, 2]
    
    gray_mask = np.zeros_like(roi_gray)
    
    # Detect multiple gray levels
    for brightness_range in [(40, 120), (120, 180), (180, 220)]:
        low, high = brightness_range
        temp_mask = ((saturation < 30) & (value > low) & (value < high)).astype(np.uint8) * 255
        gray_mask = cv2.bitwise_or(gray_mask, temp_mask)
    
    # Edge detection to find text
    edges = cv2.Canny(roi_gray, 100, 200)
    kernel = np.ones((3, 3), np.uint8)
    edges_dilated = cv2.dilate(edges, kernel, iterations=1)
    
    # Combine gray pixels with edges
    text_mask = cv2.bitwise_and(gray_mask, edges_dilated)
    
    # Clean up
    kernel_clean = np.ones((2, 2), np.uint8)
    text_mask = cv2.morphologyEx(text_mask, cv2.MORPH_CLOSE, kernel_clean)
    text_mask = cv2.morphologyEx(text_mask, cv2.MORPH_OPEN, kernel_clean)
    
    # Filter by contour size
    contours, _ = cv2.findContours(text_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    filtered_mask = np.zeros_like(text_mask)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        
        if 20 < area < 5000 and w > 5 and h > 5:
            cv2.drawContours(filtered_mask, [cnt], -1, 255, -1)
    
    # IMPORTANT: Dilate the mask to ensure complete coverage of watermark edges
    kernel_expand = np.ones((5, 5), np.uint8)
    filtered_mask = cv2.dilate(filtered_mask, kernel_expand, iterations=2)
    
    # Place in full mask
    mask[roi_y_start:, :] = filtered_mask
    
    print(f"Detected watermark pixels: {np.count_nonzero(mask)}")
    
    # Try multiple inpainting passes with increasing radius for better results
    result = img.copy()
    
    # First pass: Telea algorithm (better for texture)
    result = cv2.inpaint(result, mask, inpaintRadius=7, flags=cv2.INPAINT_TELEA)
    
    # Second pass: Navier-Stokes (better for structure)
    result = cv2.inpaint(result, mask, inpaintRadius=10, flags=cv2.INPAINT_NS)
    
    # Save results
    cv2.imwrite(output_path, result)
    print(f"Result saved to: {output_path}")
    
    mask_path = output_path.replace('.jpg', '_mask.jpg')
    cv2.imwrite(mask_path, mask)
    print(f"Mask saved to: {mask_path}")
    
    # Detailed comparison
    comparison = np.hstack([
        img,
        cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR),
        result
    ])
    comp_path = output_path.replace('.jpg', '_comparison.jpg')
    cv2.imwrite(comp_path, comparison)
    print(f"Comparison saved to: {comp_path}")

if __name__ == "__main__":
    input_image = "Images/2025_2C.jpg"
    output_image = "Images/2025_2C_improved.jpg"
    
    remove_watermark_improved(input_image, output_image)
