# Plan of Work (System Architecture)

## 1. The "Faulty Zipper" Concept
Most video players decrypt the whole file or big chunks at once. My player would acts like a **"faulty zipper"**.

*   **The Jacket:** The scrambled video stream.
*   **The Slider:** The seek bar (where you are watching).
*   **The Magic:** As you drag the slider, the code grabs *just* that specific frame, unscrambles it, shows it to you, and then throws it away. The rest of the file stays scrambled.

This keeps the content secure because the "clean" video never exists as a full file on the computer.

## 2. Making it Fast (The Python Challenge)
Video has millions of pixels. Processing them one by one in Python is way too slow.

### Attempt 1: The Slow Way (Loops)
At first, I tried using a standard `for` loop.
```python
# This took seconds per frame - too slow for video!
for i in range(total_pixels):
    output[new_pos[i]] = input[i]
```

### Attempt 2: The Fast Way (Vectors)
I switched to **NumPy**. It lets me move all pixels at once using vector instructions.
```python
# This moves 2 million pixels instantly
output[key] = input
```
This optimization was the key to making the video playable.

## 3. The "MP4" Problem
I learned the hard way that you can't just save scrambled noise as an MP4.
*   **The Problem:** MP4 compression tries to "smooth" out the image to save space. It saw my scrambled noise and tried to blur it. This changed the pixel values, so when I tried to decrypt it, the keys didn't match anymore.
*   **The Solution:** I used **FFV1**, a codec that is mathematically lossless. It keeps every pixel exactly as it is, ensuring the decryption works perfectly.

## 4. The SVD Experiment (Why Math Failed)
I also attempted to use **Singular Value Decomposition (SVD)** to create a stronger, more mathematical encryption.

### What is SVD?
SVD is a mathematical technique that breaks a matrix (image) into three separate matrices:
*   **$U$:** Represents the vertical patterns in the image.
*   **$\Sigma$ (Sigma):** Represents the "strength" or importance of those patterns.
*   **$V^T$:** Represents the horizontal patterns.

### The Idea
*   **Deeper Scrambling:** Instead of just moving pixels around (like shuffling a deck of cards), SVD allows you to scramble the *structure* of the image itself.
*   **Compression:** SVD is naturally good at compressing data, so I hoped it would keep file sizes small while encrypting.

### Why it Failed
SVD is extremely **sensitive**.
*   **The Issue:** Video frames often have slight variations in pixel values (noise) due to compression or rendering.
*   **The Result:** SVD relies on precise math. If a pixel value changes even slightly (e.g., from 200 to 201), the resulting $U$ and $V$ matrices change drastically. When I tried to apply the inverse key to decrypt it, the math no longer lined up, and the image failed to reconstruct.

## 5. The Storage Challenge (File Size Explosion)
One of the biggest trade-offs in this project was the significant increase in file size.

### The "Lenna" Benchmark
For my image tests, I used **Lenna**, the standard "Hello World" image of the computer vision industry. It is widely used because it contains a good mix of details, flat regions, and shading, making it perfect for testing compression and processing algorithms.

### The Data
| File Type | Original Size | Encrypted Size | Decrypted Size |
| :--- | :--- | :--- | :--- |
| **Image (Lenna.png)** | 462 KB | 761 KB | 508 KB |
| **Video (Video.mp4)** | 53.0 MB | **8.79 GB** | 2.05 GB |

### Why did the size explode?
The exponential increase (from 53MB to 8.79GB) happens due to the destruction of two fundamental properties that modern compression relies on:

1.  **Spatial Redundancy (The "Entropy" Problem):**
    *   **Normal Images:** In a normal photo, blue sky pixels are next to other blue sky pixels. Compression algorithms (like PNG/JPEG) say "repeat blue pixel 500 times" instead of writing "blue" 500 times.
    *   **Encrypted Images:** My shuffling moves every pixel to a random location. A blue pixel is now next to a red one, which is next to a green one. This creates **Maximum Entropy**. The compression algorithm can find *zero* patterns to summarize, so it is forced to save the raw value of every single pixel individually.

2.  **Temporal Redundancy (The "Video" Problem):**
    *   **Normal Video (H.264):** Videos are smart. If a person is standing still, the video file only saves the background *once* and tells the player "keep showing this background for 10 seconds." This is called Inter-frame compression.
    *   **Encrypted Video:** Because I shuffle every frame differently, Frame 1 looks like static noise, and Frame 2 looks like *different* static noise. The video codec thinks the entire world has changed between every single frame. It cannot reuse any data from the previous frame, forcing it to save a full, high-resolution image for every fraction of a second.

3.  **The Cost of Lossless (FFV1):**
    *   To ensure the decryption works, I had to use the **FFV1** codec. Unlike Netflix or YouTube (which throw away invisible data to save space), FFV1 keeps every bit perfect. This alone increases file size by 10-20x compared to standard MP4s.
