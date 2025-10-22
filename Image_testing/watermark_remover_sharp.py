import cv2
import numpy as np

def smart_blur_inpaint(image_path, output_path):
    """
    Remove watermarks with edge-preserving smoothing
    """
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    
    # Build mask (same detection as before)
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
    
    kernel_expand = np.ones((4, 4), np.uint8)
    filtered_mask = cv2.dilate(filtered_mask, kernel_expand, iterations=2)
    
    mask[roi_y_start:, :] = filtered_mask
    
    print(f"Processing {np.count_nonzero(mask)} watermark pixels")
    
    # NEW APPROACH: Edge-preserving filtering
    # Apply edgePreservingFilter which maintains sharpness
    result = img.copy()
    
    # Use bilateral filter stack to preserve edges while removing text
    for i in range(5):  # Multiple passes
        # Only filter masked regions
        temp = cv2.bilateralFilter(result, d=9, sigmaColor=75, sigmaSpace=75)
        result = np.where(mask[:,:,None] == 255, temp, result)
    
    # Apply edge-preserving filter
    result = cv2.edgePreservingFilter(result, flags=cv2.RECURS_FILTER, sigma_s=60, sigma_r=0.4)
    
    # Final detail enhancement using unsharp masking on non-watermark areas
    gaussian = cv2.GaussianBlur(result, (0, 0), 2.0)
    result = cv2.addWeighted(result, 1.5, gaussian, -0.5, 0)
    
    # Blend with original using mask
    mask_3d = mask[:,:,None].astype(float) / 255.0
    result = (result * mask_3d + img * (1 - mask_3d)).astype(np.uint8)
    
    cv2.imwrite(output_path, result)
    print(f"Saved to: {output_path}")
    
    comparison = np.hstack([img, cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR), result])
    cv2.imwrite(output_path.replace('.jpg', '_comparison.jpg'), comparison)

if __name__ == "__main__":
    smart_blur_inpaint("Images/2025_2C.jpg", "Images/2025_2C_sharp.jpg")
