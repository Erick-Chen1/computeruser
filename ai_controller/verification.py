"""Verification module confirming action results."""
from .types import Perception, UserInstruction, VerificationResult


def verify_action(instruction: UserInstruction, before: Perception, after: Perception) -> VerificationResult:
    """Verify that the action satisfied the user's instruction.

    This placeholder always reports success.
    """
    return VerificationResult(success=True, message="verified")
