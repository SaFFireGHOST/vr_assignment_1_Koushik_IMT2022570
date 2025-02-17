# Coin Detection and Image Stiching

## Overview

This project consists of two parts:

1. **Coin Detection, Segmentation, and Counting**  
   - Detect coins using edge detection.  
   - Segment individual coins using region-based segmentation.  
   - Count the total number of detected coins.  

2. **Image Stitching for Panorama Creation**  
   - Detect key points in overlapping images.  
   - Use homography to align and stitch images into a panorama.  

## Part 1: Coin Detection, Segmentation, and Counting

### Requirements  
Install the required dependencies using:  
```bash
pip install opencv-python numpy scikit-image matplotlib
```

### How to Run  
Place your input image in the `input_images/` folder and update the image path in `1.py`. Then, run:  
```bash
python 1.py
```

### Methods Used
- **Edge Detection & Contours**: Used Canny edge detection to find coin contours.
- **Segmentation**: Applied Gaussian blur, Otsu’s thresholding, and morphological operations to separate coins.
- **Counting**: The total number of coins is determined using contours and labeled regions.

### Example Inputs & Outputs  

#### Input Image:
![Input Coins](input_images/3.jpg)

#### Canny Edge Detection Output:
![Canny Edges](output_images/canny_edges.jpg)

#### Contour Detection Output:
![Contours](output_images/contours_detected.jpg)

#### Segmentation Output:
![Segmented Coins](output_images/segmented_coins.jpg)

---

## Part 2: Image Stitching

### Requirements  
Install dependencies:  
```bash
pip install opencv-python numpy
```

### How to Run  
Place overlapping images in the `input_images/` folder and update the image paths in `2.py`. Then, run:  
```bash
python 2.py
```

### Methods Used
- **Feature Detection**: Used SIFT to extract key points.
- **Matching**: Used Brute-Force Matcher with L2 norm.
- **Homography & Warping**: Computed homography to align images.

### Example Inputs & Outputs  

#### Input Images:
![Input 1](input_images/temp_1.jpg)
![Input 2](input_images/temp_2.jpg)

#### Keypoints Detected:
![Keypoints 1](output_images/keypoints_1.jpg)
![Keypoints 2](output_images/keypoints_2.jpg)

#### Final Stitched Panorama:
![Panorama](output_images/panorama_output.jpg)

---

## Folder Structure  
```
vr_assignment1_[Koushik]_[IMT2022570]/
│── input_images/
│   ├── 3.jpg (coins image)
│   ├── temp_1.jpg
│   ├── temp_2.jpg
│── output_images/
│   ├── canny_edges.jpg
│   ├── contours_detected.jpg
│   ├── segmented_coins.jpg
│   ├── keypoints_1.jpg
│   ├── keypoints_2.jpg
│   ├── panorama_output.jpg
│── 1.py  (Coin Detection & Segmentation)
│── 2.py  (Panorama Stitching)
│── README.md
```

