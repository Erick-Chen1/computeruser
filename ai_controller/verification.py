"""Verification module confirming action results."""
from .types import Perception, UserInstruction, VerificationResult


def verify_action(instruction: UserInstruction, before: Perception, after: Perception) -> VerificationResult:
    """Verify that the action satisfied the user's instruction.

    Verification succeeds when the after-state records an action matching the
    instruction and differs from the before-state.
    """
    expected = instruction.command.strip().lower()
    before_action = (before.ui_tree.get("last_action") or "").lower()
    after_action = (after.ui_tree.get("last_action") or "").lower()
    if after_action == before_action:
        return VerificationResult(success=False, message="no change detected")
    if after_action != expected:
        return VerificationResult(success=False, message="mismatch")
    return VerificationResult(success=True, message="verified")
