import cv2
import numpy as np
import os


def encrypt_frame(frame, key_matrix):

    height, width = frame.shape[:2]
    channels = frame.shape[2] if len(frame.shape) == 3 else 1
    total_pixels = height * width
    
    # Flatten the frame
    flat_frame = frame.reshape(total_pixels, channels)
    
    # Create encrypted frame array
    encrypted_flat = np.zeros_like(flat_frame)
    
    # Shuffle pixels using vectorized operation
    original_positions = key_matrix[:, 0]
    new_positions = key_matrix[:, 1]
    encrypted_flat[new_positions] = flat_frame[original_positions]
    
    # Reshape back to frame dimensions
    encrypted_frame = encrypted_flat.reshape(height, width, channels)
    
    return encrypted_frame


def encrypt_video(video_path, key_matrix, output_folder):

    # Open the video
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        print("Error: Could not open video")
        return None
    
    # Get video properties
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Create output folder
    os.makedirs(output_folder, exist_ok=True)
    
    # Generate output filename
    filename = os.path.basename(video_path)
    name, ext = os.path.splitext(filename)
    output_path = os.path.join(output_folder, f"{name}_encrypted.avi")
    
    # Create video writer (using FFV1 lossless codec to preserve colors)
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height), isColor=True)
    
    print(f"Encrypting {frame_count} frames...")
    
    # Process each frame
    frame_num = 0
    while True:
        ret, frame = video.read()
        
        if not ret:
            break
        
        # Encrypt the frame
        encrypted_frame = encrypt_frame(frame, key_matrix)
        
        # Write encrypted frame
        out.write(encrypted_frame)
        
        frame_num += 1
        
        # Show progress every 60 frames
        if frame_num % 60 == 0:
            print(f"Processed {frame_num}/{frame_count} frames")
    
    # Release resources
    video.release()
    out.release()
    
    print(f"Encrypted video saved: {output_path}")
    
    return output_path

if __name__ == "__main__":
    print("Use main.py to run video encryption")