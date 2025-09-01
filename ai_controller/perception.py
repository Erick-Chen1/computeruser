"""Perception module capturing the current environment."""
from __future__ import annotations

import os
import tempfile
from typing import Dict, Any

try:  # soft dependency for screenshots
    import pyautogui  # type: ignore
except Exception:  # pragma: no cover - optional
    pyautogui = None  # type: ignore

try:  # soft dependency for image handling
    from PIL import Image
except Exception:  # pragma: no cover - optional
    Image = None  # type: ignore

try:  # optional dependency for OmniParser based UI extraction
    from omniparser import OmniParser  # type: ignore
except Exception:  # pragma: no cover - optional
    OmniParser = None  # type: ignore

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
    """Generate a UI tree using OmniParser if available.

    The real OmniParser project parses a screenshot into structured elements.
    Here we attempt to invoke it when installed; otherwise an empty tree is
    returned so the rest of the pipeline can continue.
    """

    if OmniParser is None or Image is None:
        return {"elements": []}

    try:
        parser = OmniParser()
        nodes = parser.parse(image_path)  # type: ignore[attr-defined]
    except Exception:
        return {"elements": []}

    elements = []
    for node in nodes if isinstance(nodes, list) else []:
        if not isinstance(node, dict):
            continue
        bbox_raw = node.get("bbox") or node.get("box") or [0, 0, 0, 0]
        try:
            left, top, right, bottom = [int(v) for v in bbox_raw]
        except Exception:
            left = top = 0
            right = bottom = 0
        bbox = {
            "left": left,
            "top": top,
            "width": max(0, right - left),
            "height": max(0, bottom - top),
        }
        text = str(node.get("text", ""))
        elements.append({"text": text, "bbox": bbox})
    return {"elements": elements}


def capture_environment() -> Perception:
    """Capture current screen and derive a UI tree."""

    path = _save_screenshot()
    ui_tree = _omni_parse(path)
    return Perception(screenshot=path, ui_tree=ui_tree)

