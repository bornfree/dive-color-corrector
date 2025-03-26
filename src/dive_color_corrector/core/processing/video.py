"""Video processing operations."""

import math

import cv2
import numpy as np

from dive_color_corrector.core.color.constants import SAMPLE_SECONDS
from dive_color_corrector.core.color.filter import apply_filter, get_filter_matrix
from dive_color_corrector.core.processing.image import correct
from dive_color_corrector.core.utils.constants import VIDEO_CODEC


def analyze_video(video_path, output_path):
    """Analyze video for color correction.

    Args:
        video_path: Path to input video
        output_path: Path to save corrected video

    Returns:
        Dictionary containing video data and frame count
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")

    # Get video properties
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Create output video writer
    fourcc = cv2.VideoWriter_fourcc(*VIDEO_CODEC)
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    return {
        "cap": cap,
        "out": out,
        "frame_count": frame_count,
        "fps": fps,
        "width": width,
        "height": height,
    }


def process_video(video_data, yield_preview=False, use_deep=False):
    """Process video frames with color correction.

    Args:
        video_data: Dictionary containing video data and frame count
        yield_preview: Whether to yield preview frames
        use_deep: Whether to use the deep learning model instead of simple correction

    Yields:
        Progress percentage and preview frame data if yield_preview is True
    """
    cap = video_data["cap"]
    out = video_data["out"]
    frame_count = video_data["frame_count"]
    count = 0

    while cap.isOpened():
        count += 1
        percent = 100 * count / frame_count
        print(f"{percent:.2f}", end=" % \r")
        ret, frame = cap.read()

        if not ret:
            # End video read if we have gone beyond reported frame count
            if count >= frame_count:
                break

            # Failsafe to prevent an infinite loop
            if count >= 1e6:
                break

            # Otherwise this is just a faulty frame read, try reading next
            continue

        # Convert to RGB and apply correction
        rgb_mat = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        corrected_mat = correct(rgb_mat, use_deep=use_deep)

        # Write corrected frame
        out.write(corrected_mat)

        if yield_preview:
            preview = frame.copy()
            width = preview.shape[1] // 2
            height = preview.shape[0] // 2
            preview[::, width:] = corrected_mat[::, width:]

            preview = cv2.resize(preview, (width, height))

            yield percent, cv2.imencode(".png", preview)[1].tobytes()
        else:
            yield None

    cap.release()
    out.release()
