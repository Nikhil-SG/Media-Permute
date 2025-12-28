# What I Learned

> **Note:** I built this project to test an idea. Now that I have more understanding in cryptography, I went back to audit my own code. Here is what I found.

## 1. The "Color" Problem
**The Issue:**
My algorithm shuffles pixels, but it doesn't change their *colors*.
*   **Why it matters:** If you take a picture of the ocean and shuffle the pixels, it's still a big blue blob. An attacker can look at the colors and guess what the image is.
*   **The Fix:** In a real system, I would need to change the pixel values (Substitution), not just move them.

## 2. The "Repeating Key" Problem
**The Issue:**
I use the same shuffling pattern for every frame in the video.
*   **Why it matters:** If the camera moves, the "scrambled" noise moves with it in a predictable way. This makes it easier to crack.
*   **The Fix:** The key should change for every frame (like a rotating password).

## 3. Confusion vs. Diffusion (The Theory)
In cryptography, a secure system needs two things: **Diffusion** (spreading things out) and **Confusion** (masking what things are). Here is how my project stacks up:

### 3.1. Diffusion (The Blender) - Present
My project handles this well. By shuffling the pixel positions, I successfully destroy the structure of the image. You can't recognize faces or shapes because the pixels are scattered everywhere.

### 3.2. Confusion (The Mask) - Does not present
This is the missing piece. While I move the pixels around, I don't change their *colors*. A red pixel stays red; it just moves to a new spot.

**The Jigsaw Analogy:**
*   **My Project:** I take a puzzle of the Mona Lisa and scatter the pieces on the floor. You can't see the picture, but if you look at the pile, you can still see a lot of dark green and skin tones. You can guess what it is.
*   **AES Encryption:** Paints over every single puzzle piece with random noise *before* scattering them. Now, the pile just looks like gray static. You have no clue what the original image was.

## 4. Comparison with Industry Standards

| Feature | This Project | Industry Standard (AES) |
|---------|--------------|-------------------------|
| **Method** | Shuffling Pixels | Math & XOR Operations |
| **Speed** | Slower (Memory heavy) | Fast (Hardware optimized) |
| **Security** | Good for hiding shapes | Unbreakable |
| **Best Use** | Visual Obfuscation | Data Protection |