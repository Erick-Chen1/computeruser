"""User interaction module."""
from .types import UserInstruction


def parse_user_command(raw_command: str) -> UserInstruction:
    """Validate and format a raw command string.

    Args:
        raw_command: Command provided by the user.

    Returns:
        UserInstruction: Structured command.
    """
    if not isinstance(raw_command, str):
        raise TypeError("Command must be a string")
    command = raw_command.strip()
    if not command:
        raise ValueError("Command cannot be empty")
    return UserInstruction(command=command)
