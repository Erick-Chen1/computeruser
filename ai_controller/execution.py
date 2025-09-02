"""Execution module translating decisions into concrete actions."""
from __future__ import annotations

import time

try:  # optional dependency for controlling the mouse/keyboard
    import pyautogui  # type: ignore
except Exception:  # pragma: no cover - optional
    pyautogui = None  # type: ignore

from .types import Decision, Perception
from . import perception


def execute_action(decision: Decision) -> Perception:
    """Execute the provided decision and return the new perception."""

    try:
        if decision.action == "click" and decision.coordinates and pyautogui:
            x, y = decision.coordinates
            pyautogui.click(x, y)
        elif decision.action == "type" and decision.target and pyautogui:
            pyautogui.write(decision.target)
        # small delay to let the action take effect
        time.sleep(0.2)
    except Exception:  # pragma: no cover - environment may not allow GUI control
        pass

    # Capture the environment after executing the action
    return perception.capture_environment()

