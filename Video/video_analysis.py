import cv2
import os

def analyze_video(video_path):

    # Check if file exists
    if not os.path.exists(video_path):
        print(f"Error: Video not found at {video_path}")
        return None
    
    # Open the video
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        print("Error: Could not open the video")
        return None
    
    # Extract video properties
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps if fps > 0 else 0
    total_pixels = height * width
    file_size = os.path.getsize(video_path)
    
    # Release video
    video.release()
    
    # Create result dictionary
    result = {
        'height': height,
        'width': width,
        'fps': fps,
        'frame_count': frame_count,
        'duration': duration,
        'total_pixels': total_pixels,
        'file_size': file_size
    }
    
    # Print analysis results
    print(f"Video Dimensions: {height} x {width}")
    print(f"FPS: {fps:.2f}")
    print(f"Frame Count: {frame_count}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"Pixels per Frame: {total_pixels}")
    print(f"File Size: {file_size} bytes")
    
    return result

if __name__ == "__main__":
    # Test with a sample video
    test_path = input("Enter video path: ")
    analyze_video(test_path)