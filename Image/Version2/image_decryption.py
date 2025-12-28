import cv2
import numpy as np
import os


def decrypt_image(encrypted_path, inverse_key, output_folder):

    # Read the encrypted image
    encrypted_image = cv2.imread(encrypted_path)
    
    if encrypted_image is None:
        print("Error: Could not read encrypted image")
        return None
    
    height, width = encrypted_image.shape[:2]
    channels = encrypted_image.shape[2] if len(encrypted_image.shape) == 3 else 1
    total_pixels = height * width
    
    # Flatten the encrypted image
    flat_encrypted = encrypted_image.reshape(total_pixels, channels)
    
    # Create decrypted image array
    decrypted_flat = np.zeros_like(flat_encrypted)
    
    # Reverse the shuffling using vectorized operations
    shuffled_positions = inverse_key[:, 0]
    original_positions = inverse_key[:, 1]
    
    # Copy pixels back to original positions
    decrypted_flat[original_positions] = flat_encrypted[shuffled_positions]
    
    # Reshape back to original dimensions
    decrypted_image = decrypted_flat.reshape(height, width, channels)
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Generate output filename
    filename = os.path.basename(encrypted_path)
    name, ext = os.path.splitext(filename)
    # Remove '_encrypted' from name if present
    name = name.replace('_encrypted', '')
    output_path = os.path.join(output_folder, f"{name}_decrypted_v2{ext}")
    
    # Save decrypted image with high quality
    if ext.lower() in ['.jpg', '.jpeg']:
        cv2.imwrite(output_path, decrypted_image, [cv2.IMWRITE_JPEG_QUALITY, 100])
    elif ext.lower() == '.png':
        cv2.imwrite(output_path, decrypted_image, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    else:
        cv2.imwrite(output_path, decrypted_image)
    
    print(f"Decrypted image saved: {output_path}")
    
    return output_path


if __name__ == "__main__":
    print("Use main.py to run decryption")
