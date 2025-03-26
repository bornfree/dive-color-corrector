"""Deep SESR model for underwater image enhancement."""

import os
from pathlib import Path

import cv2
import numpy as np
import tensorflow as tf


class DeepSESR:
    """Deep SESR model for underwater image enhancement."""

    def __init__(self, model_path: str | Path | None = None):
        """Initialize the Deep SESR model.

        Args:
            model_path: Path to the model file. If None, will look for 'deep_sesr_2x_1d.keras' in models directory.
        """
        # Convert model_path to Path object
        if model_path is None:
            # Get the package root directory (src/dive_color_corrector)
            package_root = Path(__file__).parent.parent.parent
            model_path = package_root / "models" / "deep_sesr_2x_1d.keras"
        else:
            model_path = Path(model_path)

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")

        # Load model from .keras file
        self.model = tf.keras.models.load_model(model_path)
        self.input_size = (240, 320)  # Input size from model architecture

    def preprocess_image(self, img: np.ndarray) -> np.ndarray:
        """Preprocess image for model input.
        
        Args:
            img: Input image in BGR format with shape (H, W, 3) and dtype uint8.
            
        Returns:
            Preprocessed image with shape (1, 240, 320, 3) and values in [0, 1].
        """
        # Convert to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Resize to model input size
        img = cv2.resize(img, (self.input_size[1], self.input_size[0]))
        
        # Normalize to [0, 1]
        img = img.astype(np.float32) / 255.0
        
        # Add batch dimension
        img = np.expand_dims(img, axis=0)
        
        return img

    def postprocess_image(self, img: np.ndarray) -> np.ndarray:
        """Postprocess model output to get final enhanced image.
        
        Args:
            img: Model output tensor with shape (1, H, W, 3) and values in [-1, 1].
            
        Returns:
            Enhanced image in BGR format with shape (H, W, 3) and dtype uint8.
        """
        # Remove batch dimension
        img = np.squeeze(img, axis=0)
        
        # Scale from [-1, 1] to [0, 1]
        img = (img + 1) / 2
        
        # Clip to [0, 1] range
        img = np.clip(img, 0, 1)
        
        # Convert to uint8
        img = (img * 255).astype(np.uint8)
        
        # Convert to BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
        return img

    def enhance(self, img: np.ndarray) -> np.ndarray:
        """Enhance an underwater image.
        
        Args:
            img: Input image in BGR format with shape (H, W, 3) and dtype uint8.
            
        Returns:
            Enhanced image in BGR format with shape (H, W, 3) and dtype uint8.
        """
        # Save original size
        original_size = img.shape[:2]
        
        # Preprocess
        x = self.preprocess_image(img)
        
        # Run inference
        y = self.model.predict(x)
        
        # Get the enhanced image (first output)
        enhanced = y[0] if isinstance(y, list) else y
        
        # Postprocess
        enhanced = self.postprocess_image(enhanced)
        
        # Resize back to original size
        if original_size != self.input_size:
            enhanced = cv2.resize(enhanced, (original_size[1], original_size[0]))
        
        return enhanced 