"""Decision module selecting actions from user instructions and UI state."""
from __future__ import annotations

import json
from typing import Any, Optional

from openai import OpenAI
from .config import LLM_MODEL
from .types import Decision, Perception, UserInstruction


def _find_coordinates(target: Optional[str], ui_tree: dict[str, Any]) -> Optional[tuple[int, int]]:
    """Locate the centre coordinates of a target element in the UI tree."""
    if not target:
        return None
    target_lower = target.lower()
    for element in ui_tree.get("elements", []):
        if element.get("text", "").lower() == target_lower:
            bbox = element.get("bbox") or {}
            x = int(bbox.get("left", 0) + bbox.get("width", 0) / 2)
            y = int(bbox.get("top", 0) + bbox.get("height", 0) / 2)
            return (x, y)
    return None
  
def plan_action(instruction: UserInstruction, perception: Perception) -> Decision:
    """Generate an action plan using an LLM."""
    client = OpenAI()
    prompt = (
        "You control a computer. Available UI elements are: "
        f"{perception.ui_tree}.\n"
        f"User instruction: {instruction.command}.\n"
        "Reply ONLY with a JSON object of the form {\"action\":\"click|type\",\"target\":<string>}"
    )
    resp = client.responses.create(model=LLM_MODEL, input=prompt)
    data = json.loads(resp.output_text)  # type: ignore[attr-defined]
    action = data.get("action", "noop").lower()
    target = data.get("target")
    coords = _find_coordinates(target, perception.ui_tree)
    if action not in {"click", "type"}:
        action = "noop"
        target = None
        coords = None
    return Decision(action=action, target=target, coordinates=coords)
