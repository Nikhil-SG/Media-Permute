import os
import sys

# Add parent directories to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from video_analysis import analyze_video
from key_generation import generate_key, save_keys, load_keys
from video_encryption import encrypt_video
from video_decryption import decrypt_video

# Valid video extensions
VALID_EXTENSIONS = ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm']

def is_valid_video(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    return ext in VALID_EXTENSIONS

def get_project_root():
    # Go up from Video to project root
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def main():
    project_root = get_project_root()
    
    # Define folders
    data_folder = os.path.join(project_root, "Data")
    encrypted_folder = os.path.join(project_root, "Encrypted")
    decrypted_folder = os.path.join(project_root, "Decrypted")
    keys_folder = os.path.join(project_root, "Keys")

    print("\nOptions:")
    print("1. Encrypt Video")
    print("2. Decrypt Video")
    print("3. Exit")
    
    choice = input("\nEnter choice (1/2/3): ").strip()
    
    if choice == "1":
        # Encryption
        video_path = input("Enter video path: ").strip()
        
        # Validate video
        if not os.path.exists(video_path):
            print("Error: File not found")
            return
        
        if not is_valid_video(video_path):
            print(f"Error: Invalid video format. Supported: {VALID_EXTENSIONS}")
            return
        
        # Analyze video
        analysis = analyze_video(video_path)
        
        if analysis is None:
            return
        
        # Generate keys
        seed = input("Enter seed (press Enter for random): ").strip()
        seed = int(seed) if seed else None
        
        key_matrix, inverse_key = generate_key(
            analysis['height'], 
            analysis['width'], 
            seed=seed
        )
        
        # Save keys
        filename = os.path.splitext(os.path.basename(video_path))[0]
        save_keys(key_matrix, inverse_key, keys_folder, filename)
        
        # Encrypt video
        encrypted_path = encrypt_video(video_path, key_matrix, encrypted_folder)
        
        if encrypted_path:
            print("\nEncryption complete!")
    
    elif choice == "2":
        # Decryption
        encrypted_path = input("Enter encrypted video path: ").strip()
        
        if not os.path.exists(encrypted_path):
            print("Error: File not found")
            return
        
        if not is_valid_video(encrypted_path):
            print(f"Error: Invalid video format. Supported: {VALID_EXTENSIONS}")
            return
        
        # Load keys
        filename = os.path.splitext(os.path.basename(encrypted_path))[0]
        filename = filename.replace('_encrypted', '')
        
        try:
            _, inverse_key = load_keys(keys_folder, filename)
        except FileNotFoundError:
            print("Error: Key files not found. Make sure you encrypted this video first.")
            return
        
        # Decrypt video
        decrypted_path = decrypt_video(encrypted_path, inverse_key, decrypted_folder)
        
        if decrypted_path:
            print("\nDecryption complete!")
    
    elif choice == "3":
        print("Exiting...")
    
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()