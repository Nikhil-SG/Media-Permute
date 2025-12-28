import cv2
import numpy as np
import os


def encrypt_image(image_path, key_matrix, output_folder):
    # Read the image
    image = cv2.imread(image_path)
    
    if image is None:
        print("Error: Could not read image")
        return None
    
    height, width = image.shape[:2]
    total_pixels = height * width
    
    # Flatten the image to 1D array of pixels
    # Shape: (total_pixels, 3) for RGB
    flat_image = image.reshape(total_pixels, -1)
    
    # Create empty array for encrypted image
    encrypted_flat = np.zeros_like(flat_image)
    
    # Shuffle pixels using key matrix
    # Version 1: Simple position swap (causes quality issues)
    for i in range(total_pixels):
        original_pos = key_matrix[i, 0]
        new_pos = key_matrix[i, 1]
        encrypted_flat[new_pos] = flat_image[original_pos]
    
    # Reshape back to original image dimensions
    encrypted_image = encrypted_flat.reshape(height, width, -1)
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Generate output filename
    filename = os.path.basename(image_path)
    name, ext = os.path.splitext(filename)
    output_path = os.path.join(output_folder, f"{name}_encrypted_v1{ext}")
    
    # Save encrypted image
    cv2.imwrite(output_path, encrypted_image)
    
    print(f"Encrypted image saved: {output_path}")
    
    return output_path


if __name__ == "__main__":
    print("Use main.py to run encryption")
