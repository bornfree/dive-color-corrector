"""Create a test underwater image."""

import cv2
import numpy as np

# Create a sample image with some shapes
img = np.zeros((480, 640, 3), dtype=np.uint8)

# Add some shapes
cv2.circle(img, (320, 240), 100, (255, 255, 255), -1)  # White circle
cv2.rectangle(img, (100, 100), (200, 200), (255, 0, 0), -1)  # Red rectangle
cv2.rectangle(img, (400, 100), (500, 200), (0, 255, 0), -1)  # Green rectangle

# Convert to RGB
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# Add blue tint to simulate underwater conditions
underwater = img.copy()
underwater[..., 2] = np.clip(underwater[..., 2] + 100, 0, 255)  # Add blue tint
underwater[..., 0] = np.clip(underwater[..., 0] * 0.7, 0, 255)  # Reduce red
underwater[..., 1] = np.clip(underwater[..., 1] * 0.8, 0, 255)  # Reduce green

# Save the image
cv2.imwrite("test/samples/underwater.jpg", cv2.cvtColor(underwater, cv2.COLOR_RGB2BGR)) 