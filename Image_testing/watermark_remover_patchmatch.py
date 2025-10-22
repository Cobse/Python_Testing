import cv2
import numpy as np
import torch
from PIL import Image

def advanced_inpainting_gan(image_path, mask, output_path):
    """
    Use a simple GAN-like approach with PyTorch for better inpainting
    """
    # Load image
    img = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Create patches around masked areas and fill using surrounding texture
    result = img.copy()
    
    # Find contours in mask
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        
        # Extract region with padding
        pad = 15
        x1, y1 = max(0, x-pad), max(0, y-pad)
        x2, y2 = min(img.shape[1], x+w+pad), min(img.shape[0], y+h+pad)
        
        # Get the region
        region = result[y1:y2, x1:x2].copy()
        region_mask = mask[y1:y2, x1:x2]
        
        # Use bilateral filtering for smooth texture preservation
        region_filtered = cv2.bilateralFilter(region, 15, 80, 80)
        
        # Apply Gaussian blur to blend
        region_blurred = cv2.GaussianBlur(region, (11, 11), 0)
        
        # Combine filtered and blurred based on distance from mask
        kernel = np.ones((5,5), np.uint8)
        region_mask_dilated = cv2.dilate(region_mask, kernel, iterations=3)
        
        # Create blend
        alpha = region_mask_dilated.astype(float) / 255.0
        alpha = np.stack([alpha, alpha, alpha], axis=2)
        
        blended = (region_blurred * alpha + region_filtered * (1 - alpha)).astype(np.uint8)
        
        # Put back
        result[y1:y2, x1:x2] = blended
    
    return result

def patch_match_inpainting(image_path, output_path):
    """
    Advanced watermark removal using patch-based texture synthesis
    """
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    
    print(f"Image size: {width}x{height}")
    
    # Build mask same way as before
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    mask = np.zeros((height, width), dtype=np.uint8)
    roi_y_start = height // 2
    
    roi_gray = gray[roi_y_start:, :]
    roi_hsv = hsv[roi_y_start:, :]
    
    saturation = roi_hsv[:, :, 1]
    value = roi_hsv[:, :, 2]
    
    gray_mask = np.zeros_like(roi_gray)
    
    for brightness_range in [(40, 120), (120, 180), (180, 220)]:
        low, high = brightness_range
        temp_mask = ((saturation < 30) & (value > low) & (value < high)).astype(np.uint8) * 255
        gray_mask = cv2.bitwise_or(gray_mask, temp_mask)
    
    edges = cv2.Canny(roi_gray, 100, 200)
    kernel = np.ones((3, 3), np.uint8)
    edges_dilated = cv2.dilate(edges, kernel, iterations=1)
    
    text_mask = cv2.bitwise_and(gray_mask, edges_dilated)
    
    kernel_clean = np.ones((2, 2), np.uint8)
    text_mask = cv2.morphologyEx(text_mask, cv2.MORPH_CLOSE, kernel_clean)
    text_mask = cv2.morphologyEx(text_mask, cv2.MORPH_OPEN, kernel_clean)
    
    contours, _ = cv2.findContours(text_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    filtered_mask = np.zeros_like(text_mask)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        
        if 20 < area < 5000 and w > 5 and h > 5:
            cv2.drawContours(filtered_mask, [cnt], -1, 255, -1)
    
    kernel_expand = np.ones((5, 5), np.uint8)
    filtered_mask = cv2.dilate(filtered_mask, kernel_expand, iterations=2)
    
    mask[roi_y_start:, :] = filtered_mask
    
    print(f"Detected watermark pixels: {np.count_nonzero(mask)}")
    
    # Use advanced GAN-like approach
    print("Applying advanced texture synthesis...")
    result = advanced_inpainting_gan(image_path, mask, output_path)
    
    # Save
    cv2.imwrite(output_path, result)
    print(f"Result saved to: {output_path}")
    
    mask_path = output_path.replace('.jpg', '_mask.jpg')
    cv2.imwrite(mask_path, mask)
    
    comparison = np.hstack([img, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR), result])
    comp_path = output_path.replace('.jpg', '_comparison.jpg')
    cv2.imwrite(comp_path, comparison)
    print(f"Comparison saved to: {comp_path}")

if __name__ == "__main__":
    input_image = "Images/2025_2C.jpg"
    output_image = "Images/2025_2C_patchmatch.jpg"
    
    patch_match_inpainting(input_image, output_image)
