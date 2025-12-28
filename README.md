# Media-Permute

**Media-Permute** is a research project exploring privacy protection for media. It implements a custom encryption algorithm based on **pixel permutation** (shuffling), designed to scramble visual content while allowing for secure playback.

##  Project Structure

```text
Media-Permute/
├── Architecture.md       # Detailed explanation of the system design and "Faulty Zipper" concept
├── Review.md             # Self-audit of the project, discussing security flaws and lessons learned
├── README.md             # This file
├── requirements.txt      # Python dependencies
├── Data/                 # Input and output files
├── Keys/                 # Stores the .npy key files (the "passwords")
├── Image/                # Image encryption logic
│   ├── Version1/         # Initial implementation
│   └── Version2/         # Refined implementation
└── Video/                # Video encryption logic (frame-by-frame processing)
```

### Documentation Files
For detailed information about the system's design and security analysis, please refer to the following documents:

*   **[Architecture.md](Architecture.md)**: Covers the "Faulty Zipper" concept, Python performance optimizations (NumPy), and the technical challenges with MP4 compression and SVD.
*   **[Review.md](Review.md)**: A critical security audit discussing the "Color Problem", "Repeating Key" vulnerability, and a comparison with industry standards like AES.

## Usage

### 1. Prerequisites
Make sure you have Python installed. Then, install the required libraries:
```bash
pip install -r requirements.txt
```

### 2. Running the Code
The project is split into Image and Video modules. Each has an interactive `main.py` script.

#### For Images:
Navigate to the image version folder and run the script:
```bash
cd Image/Version1
python main.py
```
Follow the on-screen prompts to:
1.  **Encrypt:** Select an image file. The script will generate a key and save the encrypted image.
2.  **Decrypt:** Select an encrypted image and its corresponding key to restore it.

#### For Video:
Navigate to the video folder and run the script:
```bash
cd Video
python main.py
```
*Note: Video processing may take some time depending on the file size.*

### 3. Key Management
*   Keys are automatically saved in the `Keys/` folder.
*   **Important:** You need the exact key used for encryption to decrypt the file. If you lose the key, the data is lost forever.
