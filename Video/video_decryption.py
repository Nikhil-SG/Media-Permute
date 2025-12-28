import cv2
import numpy as np
import os

def decrypt_frame(frame, inverse_key):
 
    height, width = frame.shape[:2]
    channels = frame.shape[2] if len(frame.shape) == 3 else 1
    total_pixels = height * width
    
    # Flatten the frame
    flat_frame = frame.reshape(total_pixels, channels)
    
    # Create decrypted frame array
    decrypted_flat = np.zeros_like(flat_frame)
    
    # Reverse shuffling using vectorized operation
    shuffled_positions = inverse_key[:, 0]
    original_positions = inverse_key[:, 1]
    decrypted_flat[original_positions] = flat_frame[shuffled_positions]
    
    # Reshape back to frame dimensions
    decrypted_frame = decrypted_flat.reshape(height, width, channels)
    
    return decrypted_frame

def decrypt_video(encrypted_path, inverse_key, output_folder):
   
    # Open the encrypted video
    video = cv2.VideoCapture(encrypted_path)
    
    if not video.isOpened():
        print("Error: Could not open encrypted video")
        return None
    
    # Get video properties
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Create output folder
    os.makedirs(output_folder, exist_ok=True)
    
    # Generate output filename
    filename = os.path.basename(encrypted_path)
    name, ext = os.path.splitext(filename)
    name = name.replace('_encrypted', '')
    output_path = os.path.join(output_folder, f"{name}_decrypted.avi")
    
    # Create video writer (using FFV1 lossless codec to preserve colors)
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=True)
    
    print(f"Decrypting {frame_count} frames...")
    
    # Process each frame
    frame_num = 0
    while True:
        ret, frame = video.read()
        
        if not ret:
            break
        
        # Decrypt the frame
        decrypted_frame = decrypt_frame(frame, inverse_key)
        
        # Write decrypted frame
        out.write(decrypted_frame)
        
        frame_num += 1
        
        # Show progress every 60 frames
        if frame_num % 60 == 0:
            print(f"Processed {frame_num}/{frame_count} frames")
    
    # Release resources
    video.release()
    out.release()
    
    print(f"Decrypted video saved: {output_path}")
    
    return output_path

if __name__ == "__main__":
    print("Use main.py to run video decryption")