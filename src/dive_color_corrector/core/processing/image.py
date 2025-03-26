"""Image processing operations."""

import cv2

from dive_color_corrector.core.models.sesr import DeepSESR
from dive_color_corrector.core.utils.constants import PREVIEW_HEIGHT, PREVIEW_WIDTH
from dive_color_corrector.core.correction import correct as correct_simple


def correct(mat, use_deep=False):
    """Apply color correction to matrix.

    Args:
        mat: Input RGB matrix
        use_deep: Whether to use the deep learning model instead of simple correction

    Returns:
        Corrected BGR matrix
    """
    if use_deep:
        # Initialize Deep SESR model
        model = DeepSESR()
        
        # Enhance the image
        enhanced = model.enhance(mat)
        
        return enhanced
    else:
        # Use simple correction
        return correct_simple(mat)


def correct_image(input_path, output_path, use_deep=False):
    """Correct colors in a single image.

    Args:
        input_path: Path to input image
        output_path: Path to save corrected image
        use_deep: Whether to use the deep learning model instead of simple correction

    Returns:
        Preview image data as bytes
    """
    mat = cv2.imread(input_path)
    rgb_mat = cv2.cvtColor(mat, cv2.COLOR_BGR2RGB)

    corrected_mat = correct(rgb_mat, use_deep=use_deep)

    if output_path:
        cv2.imwrite(output_path, corrected_mat)

    preview = mat.copy()
    width = preview.shape[1] // 2
    preview[::, width:] = corrected_mat[::, width:]

    preview = cv2.resize(preview, (PREVIEW_WIDTH, PREVIEW_HEIGHT))

    return cv2.imencode(".png", preview)[1].tobytes()
