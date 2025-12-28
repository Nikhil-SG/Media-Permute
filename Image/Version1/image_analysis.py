import cv2
import os


def analyze_image(image_path):

    # Check if file exists
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return None
    
    # Read the image
    image = cv2.imread(image_path)
    
    if image is None:
        print("Error: Could not read the image")
        return None
    
    # Extract image properties
    height, width = image.shape[:2]
    channels = image.shape[2] if len(image.shape) == 3 else 1
    total_pixels = height * width
    file_size = os.path.getsize(image_path)
    
    # Create result dictionary
    result = {
        'height': height,
        'width': width,
        'channels': channels,
        'shape': image.shape,
        'total_pixels': total_pixels,
        'file_size': file_size
    }
    
    # Print analysis results
    print(f"Image Shape: {image.shape}")
    print(f"Dimensions: {height} x {width}")
    print(f"Total Pixels: {total_pixels}")
    print(f"File Size: {file_size} bytes")
    
    return result


if __name__ == "__main__":
    # Test with a sample image
    test_path = input("Enter image path: ")
    analyze_image(test_path)
