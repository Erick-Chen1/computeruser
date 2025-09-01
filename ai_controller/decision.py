"""Decision module using simple rules to choose an action."""
from .types import Decision, Perception, UserInstruction


def plan_action(instruction: UserInstruction, perception: Perception) -> Decision:
    """Generate an action plan based on instruction and perception.

    Supports commands of the form ``click <target>`` or ``type <text>``.
    Unrecognised commands result in a ``noop`` action.
    """
    tokens = instruction.command.strip().split()
    if not tokens:
        return Decision(action="noop", target=None)
    action = tokens[0].lower()
    target = " ".join(tokens[1:]) or None
    if action in {"click", "type"}:
        return Decision(action=action, target=target)
    return Decision(action="noop", target=None)
