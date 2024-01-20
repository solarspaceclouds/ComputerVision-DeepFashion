
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2

# Load the original image 
original_img_path = 'data/images/MEN-Denim-id_00000080-01_7_additional.jpg'  # Replace with your image path
original_img = Image.open(original_img_path)
original_img = np.array(original_img)

plt.imshow(original_img)

# Load the segmentation map
segm_path = '/home/solarspaceclouds/Desktop/DeepFashion/data/segm/MEN-Denim-id_00000080-01_7_additional_segm.png'  # Replace with your segmentation map path
segm = Image.open(segm_path)
segm = np.array(segm)


# Check if original image is in RGB format
if original_img.shape[2] != 3:
    raise ValueError("Original image is not in RGB format")

# Function to change color
def change_top_color(original_img, segm, new_color):
    img = original_img.copy()
    top_label = 1  # Label for 'top'
    mask = segm == top_label

    # Apply the mask to each color channel
    for c in range(3):  # RGB channels
        img[:, :, c][mask] = new_color[c]

    return img

# Apply the function
new_color = (255, 0, 0)  # New color for 'top', e.g., red
modified_img = change_top_color(original_img, segm, new_color)

# Display the original and modified images
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(original_img)
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(modified_img)
plt.title('Modified Image')
plt.axis('off')

plt.show()


plt.imshow(original_img)

# Convert the original image to HSV
hsv_img = cv2.cvtColor(original_img, cv2.COLOR_RGB2HSV)

# New color in HSV (convert the RGB to its corresponding HSV values
# new_hue, new_saturation, _ = (0, 255, 255)  #  new color in HSV
indigo = [120, 255, 255]
red = [0, 255, 255]
teal = [100, 170, 170]

new_hue, new_saturation, _ = indigo  

# Define the function to change color
def change_top_color_hsv(hsv_img, segm, new_hue, new_saturation):
    hsv_img = hsv_img.copy()
    
    top_label = 1  # Label for 'top'
    mask = segm == top_label

    # Replace hue and saturation for 'top' area
    hsv_img[:, :, 0][mask] = new_hue
    hsv_img[:, :, 1][mask] = new_saturation

    return hsv_img

# Apply the function
modified_hsv_img = change_top_color_hsv(hsv_img, segm, new_hue, new_saturation)

# Convert back to RGB
modified_rgb_img = cv2.cvtColor(modified_hsv_img, cv2.COLOR_HSV2RGB)

# Display the original and modified images
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(original_img)
plt.title('Original Image')
plt.axis('off')

plt.subplot(1, 2, 2)
plt.imshow(modified_rgb_img)
plt.title('Modified Image')
plt.axis('off')

plt.show()

# # Save Modified Image Result

print(original_img_path)
result_img_path = original_img_path.replace("data","task1")
print(result_img_path)

import os
# Extract the directory path from the full image path
directory = os.path.dirname(result_img_path)

# Check if the directory exists, and if not, create it
if not os.path.exists(directory):
    os.makedirs(directory)
    print(f"Created directory: {directory}")
else:
    print(f"Directory already exists: {directory}")


im = Image.fromarray(modified_rgb_img)
im.save(result_img_path)


