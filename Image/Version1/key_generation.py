import numpy as np
import os


def generate_key(height, width, seed=None):

    total_pixels = height * width
    
    # Set random seed if provided
    if seed is not None:
        np.random.seed(seed)
    
    # Create original positions array (0 to total_pixels-1)
    original_positions = np.arange(total_pixels)
    
    # Create shuffled positions
    shuffled_positions = np.random.permutation(total_pixels)
    
    # Create key matrix: [original_position, new_position]
    key_matrix = np.column_stack((original_positions, shuffled_positions))
    
    # Create inverse key matrix for decryption
    # Maps shuffled position back to original
    inverse_key = np.zeros((total_pixels, 2), dtype=np.int64)
    inverse_key[:, 0] = shuffled_positions
    inverse_key[:, 1] = original_positions
    
    # Sort inverse key by first column for easy lookup
    inverse_key = inverse_key[inverse_key[:, 0].argsort()]
    
    return key_matrix, inverse_key


def save_keys(key_matrix, inverse_key, keys_folder, filename="image"):

    # Create keys folder if it doesn't exist
    os.makedirs(keys_folder, exist_ok=True)
    
    # Save keys as numpy files
    key_path = os.path.join(keys_folder, f"{filename}_key.npy")
    inverse_key_path = os.path.join(keys_folder, f"{filename}_inverse_key.npy")
    
    np.save(key_path, key_matrix)
    np.save(inverse_key_path, inverse_key)
    
    print(f"Keys saved to {keys_folder}")
    
    return key_path, inverse_key_path


def load_keys(keys_folder, filename="image"):

    key_path = os.path.join(keys_folder, f"{filename}_key.npy")
    inverse_key_path = os.path.join(keys_folder, f"{filename}_inverse_key.npy")
    
    key_matrix = np.load(key_path)
    inverse_key = np.load(inverse_key_path)
    
    print("Keys loaded successfully")
    
    return key_matrix, inverse_key


if __name__ == "__main__":
    # Test key generation
    height = int(input("Enter image height: "))
    width = int(input("Enter image width: "))
    
    key, inv_key = generate_key(height, width, seed=42)
    print(f"Key shape: {key.shape}")
    print(f"Inverse key shape: {inv_key.shape}")
