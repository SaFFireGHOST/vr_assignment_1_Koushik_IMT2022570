import cv2
import numpy as np
from skimage import measure, color, morphology
import matplotlib.pyplot as plt
import os

# Create output directory if it doesn't exist
output_dir = "./output_images"
os.makedirs(output_dir, exist_ok=True)

# Function 1: Edge Detection & Contour-based Counting
def detect_coins_with_contours(image_path):
    image = cv2.imread(image_path)
    resized = cv2.resize(image, (300, 300), interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 3)

    # Apply Canny Edge Detection
    canny = cv2.Canny(blurred, 100, 150)

    # Save Canny Edge Image
    cv2.imwrite(os.path.join(output_dir, "canny_edges.jpg"), canny)

    # Find contours
    contours, _ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours
    contour_img = resized.copy()
    cv2.drawContours(contour_img, contours, -1, (0, 255, 0), 2)  

    # Save Contours Image
    cv2.imwrite(os.path.join(output_dir, "contours_detected.jpg"), contour_img)

    num_coins = len(contours)
    print(f"[Contours] Total Coins Detected: {num_coins}")

    # Display results
    plt.figure(figsize=(15, 5))
    plt.subplot(1, 3, 1)
    plt.title('Original Image')
    plt.imshow(cv2.cvtColor(resized, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.title('Canny Edges')
    plt.imshow(canny, cmap='gray')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.title('Detected Coins (Contours)')
    plt.imshow(cv2.cvtColor(contour_img, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.show()


# Function 2: Segmentation-based Coin Detection
def detect_coins_with_segmentation(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian Blur
    blurred = cv2.GaussianBlur(gray, (21, 21), 0)  

    # Otsu's Thresholding 
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Apply morphological operations to remove small noise
    kernel = np.ones((5, 5), np.uint8)
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # Identify connected components
    labels = measure.label(cleaned, connectivity=2)

    # Remove small objects (less than 500 pixels)
    labels = morphology.remove_small_objects(labels, min_size=500)

    # Convert labels to a colored image
    colored_labels = color.label2rgb(labels, bg_label=0)

    # Convert to OpenCV format (uint8)
    segmented_img = (colored_labels * 255).astype(np.uint8)

    # Save Segmented Image
    cv2.imwrite(os.path.join(output_dir, "segmented_coins.jpg"), cv2.cvtColor(segmented_img, cv2.COLOR_RGB2BGR))

    print(f"[Segmentation] Total Coins Detected: {len(np.unique(labels)) - 1}")

    # Display the results
    plt.figure(figsize=(10, 6))
    plt.subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.title("Segmented Coins")
    plt.imshow(colored_labels)
    plt.axis("off")

    plt.show()


# Run detection
image_path = "./input_images/3.jpg"  

detect_coins_with_contours(image_path)
detect_coins_with_segmentation(image_path)
