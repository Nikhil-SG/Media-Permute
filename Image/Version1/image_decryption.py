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
    total_pixels = height * width
    
    # Flatten the encrypted image
    flat_encrypted = encrypted_image.reshape(total_pixels, -1)
    
    # Create empty array for decrypted image
    decrypted_flat = np.zeros_like(flat_encrypted)
    
    # Reverse the shuffling using inverse key
    for i in range(total_pixels):
        shuffled_pos = inverse_key[i, 0]
        original_pos = inverse_key[i, 1]
        decrypted_flat[original_pos] = flat_encrypted[shuffled_pos]
    
    # Reshape back to original dimensions
    decrypted_image = decrypted_flat.reshape(height, width, -1)
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    # Generate output filename
    filename = os.path.basename(encrypted_path)
    name, ext = os.path.splitext(filename)
    # Remove '_encrypted' from name if present
    name = name.replace('_encrypted', '')
    output_path = os.path.join(output_folder, f"{name}_decrypted_v1{ext}")
    
    # Save decrypted image
    cv2.imwrite(output_path, decrypted_image)
    
    print(f"Decrypted image saved: {output_path}")
    
    return output_path


if __name__ == "__main__":
    print("Use main.py to run decryption")
