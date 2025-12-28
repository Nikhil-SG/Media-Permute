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
    channels = image.shape[2] if len(image.shape) == 3 else 1
    total_pixels = height * width
    
    # Flatten the image to 1D array of pixels
    # Shape: (total_pixels, channels)
    flat_image = image.reshape(total_pixels, channels)
    
    # Create encrypted image array
    encrypted_flat = np.zeros_like(flat_image)
    
    # Version 2: Proper pixel shuffling with complete RGB data
    # Use vectorized operation for better performance and accuracy
    original_positions = key_matrix[:, 0]
    new_positions = key_matrix[:, 1]
    
    # Copy pixels from original positions to new positions
    # This properly copies all RGB channels together
    encrypted_flat[new_positions] = flat_image[original_positions]
    
    # Reshape back to original image dimensions
    encrypted_image = encrypted_flat.reshape(height, width, channels)
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Generate output filename
    filename = os.path.basename(image_path)
    name, ext = os.path.splitext(filename)
    output_path = os.path.join(output_folder, f"{name}_encrypted_v2{ext}")
    
    # Save encrypted image with high quality
    if ext.lower() in ['.jpg', '.jpeg']:
        cv2.imwrite(output_path, encrypted_image, [cv2.IMWRITE_JPEG_QUALITY, 100])
    elif ext.lower() == '.png':
        cv2.imwrite(output_path, encrypted_image, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    else:
        cv2.imwrite(output_path, encrypted_image)
    
    print(f"Encrypted image saved: {output_path}")
    
    return output_path


if __name__ == "__main__":
    print("Use main.py to run encryption")
