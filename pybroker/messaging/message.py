from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
from uuid import UUID, uuid4


@dataclass(slots=True)
class Message:
    """
    Represents a message handled by PyBroker.

    Each message receives a unique identifier and creation timestamp
    automatically.
    """

    payload: Any
    id: UUID = field(default_factory=uuid4)
    created_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    def __post_init__(self) -> None:
        if self.payload is None:
            raise ValueError("Message payload cannot be None.")