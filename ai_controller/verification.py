"""Verification module confirming that an action achieved the goal."""
from __future__ import annotations

import json

from openai import OpenAI

from .config import VLM_MODEL
from .types import Perception, UserInstruction, VerificationResult


def verify_action(instruction: UserInstruction, before: Perception, after: Perception) -> VerificationResult:
    """Verify success using a vision-language model."""
    client = OpenAI()
    with open(before.screenshot, "rb") as b_img, open(after.screenshot, "rb") as a_img:
        prompt = (
            "Given the user's instruction and before/after screenshots, determine "
            "whether the instruction was completed. Respond with a JSON object "
            "{\"success\": bool, \"message\": str}.\n"
            f"Instruction: {instruction.command}"
        )
        resp = client.responses.create(
            model=VLM_MODEL,
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
