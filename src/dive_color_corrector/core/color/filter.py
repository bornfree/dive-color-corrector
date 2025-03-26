"""Color correction filter operations."""


import cv2
import numpy as np

from dive_color_corrector.core.color.constants import (
    BLUE_MAGIC_VALUE,
    MAX_HUE_SHIFT,
    MIN_AVG_RED,
    THRESHOLD_RATIO,
)
from dive_color_corrector.core.color.hue import hue_shift_red


def normalizing_interval(array):
    """Find the largest interval between consecutive values.

    Args:
        array: Input array of values

    Returns:
        Tuple of (low, high) values defining the interval
    """
    high = 255
    low = 0
    max_dist = 0

    for i in range(1, len(array)):
        dist = array[i] - array[i - 1]
        if dist > max_dist:
            max_dist = dist
            high = array[i]
            low = array[i - 1]

    return (low, high)


def apply_filter(mat, filt):
    """Apply color correction filter to matrix.

    Args:
        mat: Input RGB matrix
        filt: Filter matrix

    Returns:
        Filtered RGB matrix
    """
    r = mat[..., 0]
    g = mat[..., 1]
    b = mat[..., 2]

    r = r * filt[0] + g * filt[1] + b * filt[2] + filt[4] * 255
    g = g * filt[6] + filt[9] * 255
    b = b * filt[12] + filt[14] * 255

    filtered_mat = np.dstack([r, g, b])
    filtered_mat = np.clip(filtered_mat, 0, 255).astype(np.uint8)

    return filtered_mat


def get_filter_matrix(mat):
    """Calculate color correction filter matrix.

    Args:
        mat: Input RGB matrix

    Returns:
        Filter matrix for color correction
    """
    mat = cv2.resize(mat, (256, 256))

    # Get average values of RGB
    avg_mat = np.array(cv2.mean(mat)[:3], dtype=np.uint8)

    # Find hue shift so that average red reaches MIN_AVG_RED
    new_avg_r = avg_mat[0]
    hue_shift = 0
    while new_avg_r < MIN_AVG_RED:
        shifted = hue_shift_red(avg_mat, hue_shift)
        new_avg_r = np.sum(shifted)
        hue_shift += 1
        if hue_shift > MAX_HUE_SHIFT:
            new_avg_r = MIN_AVG_RED

    # Apply hue shift to whole image and replace red channel
    shifted_mat = hue_shift_red(mat, hue_shift)
    new_r_channel = np.sum(shifted_mat, axis=2)
    new_r_channel = np.clip(new_r_channel, 0, 255)
    mat[..., 0] = new_r_channel

    # Get histogram of all channels
    hist_r = cv2.calcHist([mat], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([mat], [1], None, [256], [0, 256])
    hist_b = cv2.calcHist([mat], [2], None, [256], [0, 256])

    normalize_mat = np.zeros((256, 3))
    threshold_level = (mat.shape[0] * mat.shape[1]) / THRESHOLD_RATIO
    for x in range(256):
        if hist_r[x] < threshold_level:
            normalize_mat[x][0] = x
        if hist_g[x] < threshold_level:
            normalize_mat[x][1] = x
        if hist_b[x] < threshold_level:
            normalize_mat[x][2] = x

    normalize_mat[255][0] = 255
    normalize_mat[255][1] = 255
    normalize_mat[255][2] = 255

    adjust_r_low, adjust_r_high = normalizing_interval(normalize_mat[..., 0])
    adjust_g_low, adjust_g_high = normalizing_interval(normalize_mat[..., 1])
    adjust_b_low, adjust_b_high = normalizing_interval(normalize_mat[..., 2])

    shifted = hue_shift_red(np.array([1, 1, 1]), hue_shift)
    shifted_r, shifted_g, shifted_b = shifted[0][0]

    red_gain = 256 / (adjust_r_high - adjust_r_low)
    green_gain = 256 / (adjust_g_high - adjust_g_low)
    blue_gain = 256 / (adjust_b_high - adjust_b_low)

    red_offset = (-adjust_r_low / 256) * red_gain
    green_offset = (-adjust_g_low / 256) * green_gain
    blue_offset = (-adjust_b_low / 256) * blue_gain

    adjust_red = shifted_r * red_gain
    adjust_red_green = shifted_g * red_gain
    adjust_red_blue = shifted_b * red_gain * BLUE_MAGIC_VALUE

    return np.array([
        adjust_red, adjust_red_green, adjust_red_blue, 0, red_offset,
        0, green_gain, 0, 0, green_offset,
        0, 0, blue_gain, 0, blue_offset,
        0, 0, 0, 1, 0,
    ])
