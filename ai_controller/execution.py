"""Execution module translating decisions into actions."""
from .types import Decision, Perception


def execute_action(decision: Decision) -> Perception:
    """Execute the provided decision.

    The placeholder does nothing and returns a dummy environment state.
    """
    screenshot = "after.png"
    ui_tree = {"elements": []}
    return Perception(screenshot=screenshot, ui_tree=ui_tree)
