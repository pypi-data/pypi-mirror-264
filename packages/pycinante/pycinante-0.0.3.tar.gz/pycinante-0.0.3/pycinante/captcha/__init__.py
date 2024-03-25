"""The module provides functionality for captcha recognition.
"""
from __future__ import annotations
from PIL import Image
import numpy as np
from typing import Sequence
from pycinante.image import scale
from pycinante.pytorch import load_onnxruntime
from pycinante.file import load_json

__all__ = [
    'ocr_captcha'
]

def ocr_captcha(image: Image.Image,
                onnx: str | bytes = None,
                charset: str | Sequence[str] = None,
                device_id: int = -1) -> str:
    """Identifies the given captcha PIL image and returns the text in the identified
    captcha. The default identification onnx model and the source character set from
    `https://github.com/sml2h3/ddddocr`.

    Args:
        image (PIL Image): Captcha image to be OCR.
        onnx (str, optional): Path to onnx model or onnx model bytes.
        charset (str, optional): Path to charset file or charset sequence.
        device_id (int): Device to run onnx model on.
    """
    image = scale(image, height=64).convert('L')
    image = np.array(image).astype(np.float32)
    image = np.expand_dims(image, axis=0) / 255.
    image = (image - 0.5) / 0.5
    image = {'input1': np.array([image]).astype(np.float32)}
    model = load_onnxruntime(onnx or 'ocr.onnx', device_id)
    prediction = model.run(None, image)[0][0]
    charset = charset or 'charset.json'
    charset = (isinstance(charset, str) and load_json(charset)) or charset
    return ''.join([charset[i] for i in prediction if i != 0])
