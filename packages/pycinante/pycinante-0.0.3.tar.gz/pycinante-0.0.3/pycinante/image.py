"""This module provides functions to access and manipulate images.
"""
from __future__ import annotations
import glob
import warnings
from typing import AnyStr, Union, Callable

__all__ = [
    'cv2_rgb_loader',
    'cv2_gray_loader',
    'pil_rgb_loader',
    'pil_gray_loader',
    'load_image',
    'scale'
]

# noinspection PyUnresolvedReferences
def cv2_rgb_loader(pathname: AnyStr) -> 'np.ndarray':
    """OpenCV RGB image loader for loading a rgb image from a given pathname."""
    import cv2
    image = cv2.imread(pathname, cv2.IMREAD_COLOR)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# noinspection PyUnresolvedReferences
def cv2_gray_loader(pathname: AnyStr) -> 'np.ndarray':
    """OpenCV gray image loader for loading a gray image from a given pathname."""
    import cv2
    image = cv2.imread(pathname, cv2.IMREAD_GRAYSCALE)
    image = image[:, :, None]
    return image

# noinspection PyUnresolvedReferences
def pil_rgb_loader(filename) -> 'Image.Image':
    """Pillow RGB image loader for loading a rgb image from a given pathname."""
    from PIL import Image
    return Image.open(filename).convert('RGB')

# noinspection PyUnresolvedReferences
def pil_gray_loader(filename) -> 'Image.Image':
    from PIL import Image
    """Pillow gray image loader for loading a gray image from a given pathname."""
    return Image.open(filename).convert('L')

# noinspection PyUnresolvedReferences
def load_image(
    pathname: AnyStr,
    loader: Callable[[AnyStr], Union['Image.Image', 'np.ndarray']] = cv2_rgb_loader
) -> Union['Image.Image', 'np.ndarray']:
    """Load an image from a given pathname with a given image loader."""
    if any([e in pathname for e in ['*', '?']]):
        filelist = glob.glob(pathname)
        if len(filelist) == 0:
            raise FileNotFoundError(pathname)
        if len(filelist) > 1:
            warnings.warn('multiple images found in {}'.format(pathname))
        pathname = filelist[0]
    return loader(pathname)

# noinspection PyUnresolvedReferences
def scale(
    image: 'Image.Image',
    width: int | None = None,
    height: int | None = None,
    resample: Union['Image.Resampling', None] = None
) -> 'Image.Image':
    """Scale the given PIL image. Given `width` or `height`, calculate another value in
    proportion; If both `width` and `height` are given, then scale to the specified size
    (not necessarily to maintain the scale, depending on the parameter).
    """
    from PIL import Image
    assert width or height, 'width and height cannot both be None'
    height = (not height and int(image.size[1] * width / image.size[0])) or height
    width = (not width and int(image.size[0] * height / image.size[1])) or width
    resample = resample or getattr(Image, 'ANTIALIAS', getattr(Image, 'LANCZOS'))
    return image.resize((width, height), resample=resample)
