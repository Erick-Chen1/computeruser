"""Perception module capturing the current environment."""
from __future__ import annotations

import os
import tempfile
from typing import Dict, Any

try:  # soft dependency for screenshots
    import pyautogui  # type: ignore
except Exception:  # pragma: no cover - optional
    pyautogui = None  # type: ignore

try:  # soft dependency for OCR-based UI extraction
    from PIL import Image
    import pytesseract  # type: ignore
except Exception:  # pragma: no cover - optional
    Image = None  # type: ignore
    pytesseract = None  # type: ignore

from .types import Perception


def _save_screenshot() -> str:
    """Capture a screenshot to a temporary PNG file.

    Falls back to a 1x1 black image when screenshot capture fails. The path to
    the saved image is returned.
    """

    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    try:
        if pyautogui is None:
            raise RuntimeError("pyautogui unavailable")
        img = pyautogui.screenshot()
        img.save(path)
    except Exception:  # pragma: no cover - environment without display
        if Image is not None:
            Image.new("RGB", (1, 1), color=(0, 0, 0)).save(path)
        else:
            with open(path, "wb") as f:
                f.write(b"")
    return path


def _omni_parse(image_path: str) -> Dict[str, Any]:
    """Generate a simple UI tree using OCR data.

    This acts as a lightweight stand-in for the OmniParser component by
    extracting text and bounding boxes from the screenshot with Tesseract. If
    pytesseract is not available, an empty tree is returned.
    """

    if pytesseract is None or Image is None:
        return {"elements": []}

    image = Image.open(image_path)
    data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
    elements = []
    for i, text in enumerate(data.get("text", [])):
        text = text.strip()
        if not text:
            continue
        bbox = {
            "left": int(data["left"][i]),
            "top": int(data["top"][i]),
            "width": int(data["width"][i]),
            "height": int(data["height"][i]),
        }
        elements.append({"text": text, "bbox": bbox})
    return {"elements": elements}


def capture_environment() -> Perception:
    """Capture current screen and derive a UI tree."""

    path = _save_screenshot()
    ui_tree = _omni_parse(path)
    return Perception(screenshot=path, ui_tree=ui_tree)

