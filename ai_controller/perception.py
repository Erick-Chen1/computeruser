"""Perception module capturing environment state."""
import os
import tempfile

from .types import Perception


def capture_environment() -> Perception:
    """Capture current screen and UI tree.
    A temporary PNG file is created to represent a screenshot, and a minimal
    UI tree with no elements is returned.
    """
    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    # Write placeholder data so the file exists on disk
    with open(path, "wb") as f:
        f.write(b"")
    ui_tree = {"elements": [], "last_action": None}
    return Perception(screenshot=path, ui_tree=ui_tree)

