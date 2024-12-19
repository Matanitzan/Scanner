# Scanner Project

This project implements a document scanner using OpenCV.
The scanner takes an image as input, detects the boundaries of a document within the image,
and outputs a perspective-transformed version of the document as if it were scanned.
The result is saved to an output file and displayed on the screen.

---

## Features

- Detects the largest contour in the image (assumed to be the document).
- Approximates the contour to a quadrilateral using the Ramer-Douglas-Peucker algorithm.
- Calculates the dimensions of the document in pixels.
- Applies a perspective transformation to "flatten" the document.
- Saves the scanned document to a specified output file.

---

## Prerequisites

Ensure the following are installed in your Python environment:

1. Python 3.6 or higher
2. OpenCV

You can install OpenCV using pip:

```bash
pip install opencv-python
```

---

## How to Use

### Running the Script

1. **Input Image**:

   - Prepare an image containing a document (e.g., `input/IMG-3763.jpg`).
   - Ensure the image is in the correct path relative to the script.

2. **Command**:
   Run the script with the following command:

   ```bash
   python3 Scanner.py <input_image_path> <output_image_path>
   ```

   Example:

   ```bash
   python3 Scanner.py input/IMG-3763.jpg output/scanned_image.jpg
   ```

3. **Output**:

   - The script will display the scanned document.
   - The transformed document will be saved to the specified output path.

### Example Input and Output

- **Input**: A photo of a document on a surface.
- **Output**: The perspective-transformed scanned document.

---

## Requirements

- OpenCV 4.0 or higher
- Numpy

---

