
"""Verification module confirming that an action achieved the goal."""
from __future__ import annotations

import json

try:  # optional dependency for VLM verification
    from openai import OpenAI  # type: ignore
except Exception:  # pragma: no cover - optional
    OpenAI = None  # type: ignore

from .types import Perception, UserInstruction, VerificationResult


def _vlm_verify(instruction: str, before: Perception, after: Perception) -> VerificationResult:
    """Use a vision-language model to verify success."""

    if OpenAI is None:
        raise RuntimeError("OpenAI library not available")

    client = OpenAI()
    with open(before.screenshot, "rb") as b_img, open(after.screenshot, "rb") as a_img:
        prompt = (
            "Given the user's instruction and before/after screenshots, determine "
            "whether the instruction was completed. Respond with a JSON object "
            "{\"success\": bool, \"message\": str}.\n"
            f"Instruction: {instruction}"
        )
        resp = client.responses.create(
            model="gpt-4o-mini",
            input=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {"type": "image", "image": b_img},
                        {"type": "image", "image": a_img},
                    ],
                }
            ],
        )
    data = json.loads(resp.output_text)  # type: ignore[attr-defined]
    return VerificationResult(success=bool(data.get("success")), message=data.get("message", ""))


def verify_action(instruction: UserInstruction, before: Perception, after: Perception) -> VerificationResult:
    """Verify that the action satisfied the user's instruction."""

    try:
        return _vlm_verify(instruction.command, before, after)
    except Exception:
        # Simple heuristic: check if the screenshots differ
        changed = True
        try:
            with open(before.screenshot, "rb") as f1, open(after.screenshot, "rb") as f2:
                changed = f1.read() != f2.read()
        except Exception:
            pass
        if changed:
            return VerificationResult(success=True, message="change detected (unverified)")
        return VerificationResult(success=False, message="no change detected")

