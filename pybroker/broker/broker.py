from __future__ import annotations

from pybroker.messaging.message import Message
from pybroker.messaging.queue import InMemoryQueue


class Broker:
    """
    Central message broker.

    Manages named queues and allows messages to be
    published and consumed.
    """

    def __init__(self) -> None:
        self._queues: dict[str, InMemoryQueue] = {}

    def create_queue(self, name: str) -> InMemoryQueue:
        """
        Create a new queue.

        If the queue already exists, return the existing one.
        """

        normalized_name = self._normalize_queue_name(name)

        if normalized_name not in self._queues:
            self._queues[normalized_name] = InMemoryQueue(
                normalized_name
            )

        return self._queues[normalized_name]

    def get_queue(self, name: str) -> InMemoryQueue | None:
        """
        Get an existing queue.

        Returns None if the queue doesn't exist.
        """

        normalized_name = self._normalize_queue_name(name)

        return self._queues.get(normalized_name)

    def queue_exists(self, name: str) -> bool:
        """
        Check whether a queue exists.
        """

        normalized_name = self._normalize_queue_name(name)

        return normalized_name in self._queues

    def delete_queue(self, name: str) -> bool:
        """
        Delete a queue.

        Returns True if the queue existed and was deleted.
        Returns False if the queue did not exist.
        """

        normalized_name = self._normalize_queue_name(name)

        if normalized_name not in self._queues:
            return False

        del self._queues[normalized_name]

        return True

    def publish(
        self,
        queue_name: str,
        message: Message,
    ) -> None:
        """
        Publish a message to a named queue.

        The queue is automatically created if it
        doesn't already exist.
        """

        if not isinstance(message, Message):
            raise TypeError(
                "Broker can only publish Message instances."
            )

        queue = self.create_queue(queue_name)
        queue.publish(message)

    def consume(self, queue_name: str) -> Message | None:
        """
        Consume the oldest message from a queue.

        Returns None if the queue does not exist
        or contains no messages.
        """

        queue = self.get_queue(queue_name)

        if queue is None:
            return None

        return queue.consume()
    def list_queues(self) -> list[str]:
        """
        Return the names of all registered queues.
        """

        return list(self._queues.keys())
    def queue_size(self, name: str) -> int:
        """
        Return the number of messages waiting in a queue.

        Returns 0 if the queue does not exist.
        """

        queue = self.get_queue(name)

        if queue is None:
            return 0

        return queue.size
    @property
    def queue_count(self) -> int:
        """
        Number of queues managed by the broker.
        """

        return len(self._queues)

    @staticmethod
    def _normalize_queue_name(name: str) -> str:
        """
        Validate and normalize a queue name.
        """

        if not isinstance(name, str):
            raise TypeError("Queue name must be a string.")

        normalized_name = name.strip()

        if not normalized_name:
            raise ValueError("Queue name cannot be empty.")

        return normalized_name
