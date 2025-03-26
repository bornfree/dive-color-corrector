"""Hue shift operations."""

import math

import numpy as np


def hue_shift_red(mat, h):
    """Apply hue shift to red channel.

    Args:
        mat: Input RGB matrix
        h: Hue shift angle in degrees

    Returns:
        RGB matrix with shifted hue
    """
    u = math.cos(h * math.pi / 180)
    w = math.sin(h * math.pi / 180)

    r = (0.299 + 0.701 * u + 0.168 * w) * mat[..., 0]
    g = (0.587 - 0.587 * u + 0.330 * w) * mat[..., 1]
    b = (0.114 - 0.114 * u - 0.497 * w) * mat[..., 2]

    return np.dstack([r, g, b])
