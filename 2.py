import cv2
import numpy as np

# Detect keypoints and match features using SIFT and BFMatcher
def detect_and_match_keypoints(img1, img2):
    sift = cv2.SIFT_create()
    
    # Detect keypoints and descriptors
    keypoints1, descriptors1 = sift.detectAndCompute(img1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(img2, None)
    
    # Use Brute-Force Matcher with L2 norm 
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
    
    # Match descriptors
    matches = bf.match(descriptors1, descriptors2)
    
    # Sort matches based on distance
    matches = sorted(matches, key=lambda x: x.distance)
    
    return keypoints1, keypoints2, matches

# Stitch two images together using homography
def stitch_images(img1, img2):
    keypoints1, keypoints2, matches = detect_and_match_keypoints(img1, img2)
    
    # Extract location of good matches
    src_pts = np.float32([keypoints1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

    # Compute homography
    H, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    
    # Warp image
    h1, w1 = img1.shape[:2]
    h2, w2 = img2.shape[:2]
    
    # Create a panorama canvas
    panorama_width = w1 + w2
    panorama_height = max(h1, h2)
    
    panorama = cv2.warpPerspective(img1, H, (panorama_width, panorama_height))
    panorama[0:h2, 0:w2] = img2
    
    return panorama

# Load images
img1 = cv2.imread("./input_images/temp_2.jpg")
img2 = cv2.imread("./input_images/temp_1.jpg")

# Resizing for consistency
img1 = cv2.resize(img1, (800, 600))
img2 = cv2.resize(img2, (800, 600))

# Detect keypoints and matches
keypoints1, keypoints2, matches = detect_and_match_keypoints(img1, img2)

# Draw keypoints on images
img1_keypoints = cv2.drawKeypoints(img1, keypoints1, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
img2_keypoints = cv2.drawKeypoints(img2, keypoints2, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Show keypoints
cv2.imshow("Keypoints Image 1", img1_keypoints)
cv2.imshow("Keypoints Image 2", img2_keypoints)
cv2.imwrite("keypoints_1.jpg", img1_keypoints)
cv2.imwrite("keypoints_2.jpg", img2_keypoints)

# Stitch images
panorama = stitch_images(img1, img2)

# Show and save output
cv2.imshow("Panorama", panorama)
cv2.imwrite("./output_images/panorama_output.jpg", panorama)
cv2.waitKey(0)
cv2.destroyAllWindows()
