"""Execution module translating decisions into actions."""
import os
import tempfile

from .types import Decision, Perception


def execute_action(decision: Decision) -> Perception:
    """Execute the provided decision.

    A new temporary screenshot file is created containing the action text and
    the resulting UI tree records the last action performed.
    """
    fd, path = tempfile.mkstemp(suffix=".png")
    os.close(fd)
    action_desc = decision.action if decision.target is None else f"{decision.action} {decision.target}"
    with open(path, "wb") as f:
        f.write(action_desc.encode())
    ui_tree = {"elements": [], "last_action": action_desc}
    return Perception(screenshot=path, ui_tree=ui_tree)
