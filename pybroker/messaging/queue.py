from __future__ import annotations

from collections import deque
from typing import Deque

from .message import Message


class InMemoryQueue:
    """
    FIFO message queue stored entirely in memory.

    Messages are delivered in the same order in which they
    were published.
    """

    def __init__(self, name: str) -> None:
        if not name or not name.strip():
            raise ValueError("Queue name cannot be empty.")

        self.name = name
        self._messages: Deque[Message] = deque()

    def publish(self, message: Message) -> None:
        """
        Add a message to the end of the queue.
        """

        if not isinstance(message, Message):
            raise TypeError("Only Message instances can be published.")

        self._messages.append(message)

    def consume(self) -> Message | None:
        """
        Remove and return the oldest message.

        Returns None when the queue is empty.
        """

        if not self._messages:
            return None

        return self._messages.popleft()

    def peek(self) -> Message | None:
        """
        Return the oldest message without removing it.
        """

        if not self._messages:
            return None

        return self._messages[0]

    def clear(self) -> None:
        """
        Remove all messages from the queue.
        """

        self._messages.clear()

    @property
    def size(self) -> int:
        """
        Number of messages currently waiting in the queue.
        """

        return len(self._messages)

    @property
    def is_empty(self) -> bool:
        """
        Return True when the queue contains no messages.
        """

        return not self._messages

    def __len__(self) -> int:
        return self.size

    def __repr__(self) -> str:
        return (
            f"InMemoryQueue(name={self.name!r}, "
            f"size={self.size})"
        )