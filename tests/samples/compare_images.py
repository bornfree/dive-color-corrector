"""Compare original and corrected images."""

import cv2
import numpy as np

# Read images
original = cv2.imread("test/samples/underwater.jpg")
corrected = cv2.imread("test/samples/corrected.jpg")

# Create a side-by-side comparison
comparison = np.hstack([original, corrected])

# Add labels
cv2.putText(comparison, "Original", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
cv2.putText(comparison, "Corrected", (original.shape[1] + 10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# Save the comparison
cv2.imwrite("test/samples/comparison.jpg", comparison)
print("Comparison saved as test/samples/comparison.jpg") 