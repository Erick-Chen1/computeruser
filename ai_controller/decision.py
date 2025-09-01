
"""Decision module selecting actions from user instructions and UI state."""
from __future__ import annotations

import json
from typing import Any, Optional

try:  # optional dependency for LLM planning
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover - optional
    OpenAI = None  # type: ignore

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


def _llm_plan(instruction: str, ui_tree: dict[str, Any]) -> Decision:
    """Use an LLM to transform instructions into concrete actions.

    The model is expected to return a JSON object like
    ``{"action": "click", "target": "OK"}``. If the call fails, an
    exception is raised so the caller can fall back to rule-based planning.
    """

    if OpenAI is None:
        raise RuntimeError("OpenAI library not available")

    client = OpenAI()
    prompt = (
        "You control a computer. Available UI elements are: "
        f"{ui_tree}.\n"
        f"User instruction: {instruction}.\n"
        "Reply ONLY with a JSON object of the form {\"action\":\"click|type\",\"target\":<string>}"
    )
    resp = client.responses.create(model="gpt-4o-mini", input=prompt)
    data = json.loads(resp.output_text)  # type: ignore[attr-defined]
    action = data.get("action", "noop").lower()
    target = data.get("target")
    coords = _find_coordinates(target, ui_tree)
    return Decision(action=action, target=target, coordinates=coords)


def plan_action(instruction: UserInstruction, perception: Perception) -> Decision:
    """Generate an action plan based on instruction and perception."""

    try:
        decision = _llm_plan(instruction.command, perception.ui_tree)
    except Exception:
        # Fall back to simple rule-based parsing
        tokens = instruction.command.strip().split()
        if tokens:
            action = tokens[0].lower()
            target = " ".join(tokens[1:]) or None
        else:
            action = "noop"
            target = None
        coords = _find_coordinates(target, perception.ui_tree)
        decision = Decision(action=action, target=target, coordinates=coords)

    if decision.action not in {"click", "type"}:
        decision = Decision(action="noop", target=None, coordinates=None)
    return decision

