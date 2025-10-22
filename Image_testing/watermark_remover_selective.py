import cv2
import numpy as np

def remove_watermark_selective(image_path, output_path):
    """
    Selective watermark removal - only target gray text in specific patterns
    """
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    
    print(f"Image size: {width}x{height}")
    
    # Convert to different color spaces for better detection
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    # Create mask for watermark - focus on bottom half
    mask = np.zeros((height, width), dtype=np.uint8)
    roi_y_start = height // 2
    
    # Extract ROI
    roi_gray = gray[roi_y_start:, :]
    roi_bgr = img[roi_y_start:, :]
    
    # Method: Detect low saturation (gray) pixels with specific brightness ranges
    roi_hsv = hsv[roi_y_start:, :]
    
    # Gray watermarks have low saturation
    saturation = roi_hsv[:, :, 1]
    value = roi_hsv[:, :, 2]
    
    # Detect gray text (low saturation, varying value)
    # Adjust these ranges based on watermark gray levels
    gray_mask = np.zeros_like(roi_gray)
    
    # Multiple passes for different gray levels
    for brightness_range in [(40, 120), (120, 180), (180, 220)]:
        low, high = brightness_range
        temp_mask = ((saturation < 30) & (value > low) & (value < high)).astype(np.uint8) * 255
        gray_mask = cv2.bitwise_or(gray_mask, temp_mask)
    
    # Now filter to keep only text-like regions (not entire areas)
    # Use edge detection to find text boundaries
    edges = cv2.Canny(roi_gray, 100, 200)
    
    # Combine: gray pixels that are near edges (text)
    kernel = np.ones((3, 3), np.uint8)
    edges_dilated = cv2.dilate(edges, kernel, iterations=1)
    
    # Keep only gray pixels that are close to text edges
    text_mask = cv2.bitwise_and(gray_mask, edges_dilated)
    
    # Clean up with morphological operations
    kernel_clean = np.ones((2, 2), np.uint8)
    text_mask = cv2.morphologyEx(text_mask, cv2.MORPH_CLOSE, kernel_clean)
    text_mask = cv2.morphologyEx(text_mask, cv2.MORPH_OPEN, kernel_clean)
    
    # Find contours and filter by size
    contours, _ = cv2.findContours(text_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    filtered_mask = np.zeros_like(text_mask)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Keep medium-sized components (letters/words)
        if 20 < area < 5000 and w > 5 and h > 5:
            cv2.drawContours(filtered_mask, [cnt], -1, 255, -1)
    
    # Place in full mask
    mask[roi_y_start:, :] = filtered_mask
    
    print(f"Detected watermark pixels: {np.count_nonzero(mask)}")
    
    # Apply inpainting with smaller radius for precision
    result = cv2.inpaint(img, mask, 5, cv2.INPAINT_NS)
    
    # Save results
    cv2.imwrite(output_path, result)
    print(f"Result saved to: {output_path}")
    
    mask_path = output_path.replace('.jpg', '_mask.jpg')
    cv2.imwrite(mask_path, mask)
    print(f"Mask saved to: {mask_path}")
    
    # Create detailed comparison
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
    output_image = "Images/2025_2C_selective.jpg"
    
    remove_watermark_selective(input_image, output_image)
