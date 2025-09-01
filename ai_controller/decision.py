"""Decision module using an LLM to choose an action."""
from .types import Decision, Perception, UserInstruction


def plan_action(instruction: UserInstruction, perception: Perception) -> Decision:
    """Generate an action plan based on instruction and perception.

    This placeholder always returns a no-op action.
    """
    return Decision(action="noop", target=None)
