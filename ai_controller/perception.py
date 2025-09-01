"""Perception module capturing environment state."""
from .types import Perception


def capture_environment() -> Perception:
    """Capture current screen and UI tree.

    This placeholder returns empty data structures for demonstration.
    """
    screenshot = "before.png"  # In a real system, path to captured screenshot.
    ui_tree = {"elements": []}  # Placeholder for parsed UI tree.
    return Perception(screenshot=screenshot, ui_tree=ui_tree)
