"""Constants for color correction."""

from dive_color_corrector.core.utils.constants import (
    BLUE_MAGIC_VALUE,
    MAX_HUE_SHIFT,
    MIN_AVG_RED,
    THRESHOLD_RATIO,
)

__all__ = ["BLUE_MAGIC_VALUE", "MAX_HUE_SHIFT", "MIN_AVG_RED", "THRESHOLD_RATIO"]

SAMPLE_SECONDS = 2  # Extracts color correction from every N seconds
