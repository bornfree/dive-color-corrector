"""Constants used throughout the application."""

# Supported image formats
IMAGE_FORMATS = {
    ".png": "PNG Image",
    ".jpg": "JPEG Image",
    ".jpeg": "JPEG Image",
    ".bmp": "Bitmap Image",
    ".tiff": "Tagged Image File Format",
    ".webp": "WebP Image",
}

# Supported video formats
VIDEO_FORMATS = {
    ".mp4": "MPEG-4 Video",
    ".mkv": "Matroska Video",
    ".avi": "Audio Video Interleave",
    ".mov": "QuickTime Movie",
    ".wmv": "Windows Media Video",
    ".flv": "Flash Video",
    ".webm": "WebM Video",
}

# Combined formats for file type checking
SUPPORTED_FORMATS = {
    **IMAGE_FORMATS,
    **VIDEO_FORMATS,
}

# Color correction constants
THRESHOLD_RATIO = 2000
MIN_AVG_RED = 60
MAX_HUE_SHIFT = 120
BLUE_MAGIC_VALUE = 1.2
SAMPLE_SECONDS = 2  # Extracts color correction from every N seconds

# Preview settings
PREVIEW_WIDTH = 960
PREVIEW_HEIGHT = 540

# Video codec settings
VIDEO_CODEC = "mp4v"
