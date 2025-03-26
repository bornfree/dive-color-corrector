"""Tests for the Deep SESR model."""

import numpy as np
import pytest
from pathlib import Path

from dive_color_corrector.core.models.sesr import DeepSESR


def test_model_initialization():
    """Test model initialization with default and custom paths."""
    # Test with default path
    model = DeepSESR()
    assert model.input_size == (240, 320)
    assert model.model is not None

    # Test with custom path
    custom_path = Path("src/dive_color_corrector/models/deep_sesr_2x_1d.keras")
    model = DeepSESR(custom_path)
    assert model.input_size == (240, 320)
    assert model.model is not None

    # Test with non-existent path
    with pytest.raises(FileNotFoundError):
        DeepSESR("non_existent_model.keras")


def test_preprocess_image():
    """Test image preprocessing."""
    model = DeepSESR()
    
    # Create a test image
    img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    # Preprocess
    processed = model.preprocess_image(img)
    
    # Check output shape and range
    assert processed.shape == (1, 240, 320, 3)
    assert processed.dtype == np.float32
    assert np.all(processed >= 0) and np.all(processed <= 1)


def test_postprocess_image():
    """Test image postprocessing."""
    model = DeepSESR()
    
    # Create a test tensor
    img = np.random.uniform(-1, 1, (1, 240, 320, 3)).astype(np.float32)
    
    # Postprocess
    processed = model.postprocess_image(img)
    
    # Check output shape and range
    assert processed.shape == (240, 320, 3)
    assert processed.dtype == np.uint8
    assert np.all(processed >= 0) and np.all(processed <= 255)


def test_enhance():
    """Test image enhancement pipeline."""
    model = DeepSESR()
    
    # Create a test image
    img = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    # Enhance
    enhanced = model.enhance(img)
    
    # Check output shape and type
    assert enhanced.shape == img.shape
    assert enhanced.dtype == np.uint8
    assert np.all(enhanced >= 0) and np.all(enhanced <= 255) 