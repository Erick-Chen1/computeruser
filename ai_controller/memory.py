"""Memory module recording interaction cycles."""
from typing import List

from .types import MemoryRecord, Decision, Perception, UserInstruction, VerificationResult


class Memory:
    """In-memory storage for interaction records."""

    def __init__(self) -> None:
        self.records: List[MemoryRecord] = []

    def add_record(
        self,
        instruction: UserInstruction,
        before: Perception,
        after: Perception,
        decision: Decision,
        verification: VerificationResult,
    ) -> MemoryRecord:
        """Store a new interaction record."""
        record = MemoryRecord(
            instruction=instruction,
            before=before,
            after=after,
            decision=decision,
            verification=verification,
        )
        self.records.append(record)
        return record
