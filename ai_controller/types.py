"""Data structures for AI computer controller architecture."""
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class UserInstruction:
    """Structured representation of a user command."""
    command: str


@dataclass
class Perception:
    """Environment state consisting of screenshot path and UI tree."""
    screenshot: str
    ui_tree: Dict[str, Any]


@dataclass
class Decision:
    """Action chosen by the decision module."""
    action: str
    target: Optional[str]



@dataclass
class VerificationResult:
    """Outcome of the verification step."""
    success: bool
    message: str


@dataclass
class MemoryRecord:
    """Record of a single interaction cycle."""
    instruction: UserInstruction
    before: Perception
    after: Perception
    decision: Decision
    verification: VerificationResult
