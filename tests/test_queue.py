import pytest

from pybroker.messaging.message import Message
from pybroker.messaging.queue import InMemoryQueue


def test_queue_can_be_created() -> None:
    queue = InMemoryQueue("emails")

    assert queue.name == "emails"
    assert queue.size == 0
    assert queue.is_empty is True


def test_queue_rejects_empty_name() -> None:
    with pytest.raises(
        ValueError,
        match="Queue name cannot be empty",
    ):
        InMemoryQueue("")


def test_queue_rejects_whitespace_name() -> None:
    with pytest.raises(
        ValueError,
        match="Queue name cannot be empty",
    ):
        InMemoryQueue("   ")


def test_publish_adds_message() -> None:
    queue = InMemoryQueue("emails")
    message = Message(payload="hello")

    queue.publish(message)

    assert queue.size == 1
    assert queue.is_empty is False


def test_publish_rejects_non_message_object() -> None:
    queue = InMemoryQueue("emails")

    with pytest.raises(
        TypeError,
        match="Only Message instances can be published",
    ):
        queue.publish("hello")  # type: ignore[arg-type]


def test_consume_returns_message() -> None:
    queue = InMemoryQueue("emails")
    message = Message(payload="hello")

    queue.publish(message)

    result = queue.consume()

    assert result == message
    assert queue.size == 0


def test_consume_empty_queue_returns_none() -> None:
    queue = InMemoryQueue("emails")

    assert queue.consume() is None


def test_queue_is_fifo() -> None:
    queue = InMemoryQueue("emails")

    first = Message(payload="first")
    second = Message(payload="second")
    third = Message(payload="third")

    queue.publish(first)
    queue.publish(second)
    queue.publish(third)

    assert queue.consume() == first
    assert queue.consume() == second
    assert queue.consume() == third


def test_peek_does_not_remove_message() -> None:
    queue = InMemoryQueue("emails")
    message = Message(payload="hello")

    queue.publish(message)

    result = queue.peek()

    assert result == message
    assert queue.size == 1


def test_clear_removes_all_messages() -> None:
    queue = InMemoryQueue("emails")

    queue.publish(Message(payload="first"))
    queue.publish(Message(payload="second"))

    queue.clear()

    assert queue.size == 0
    assert queue.is_empty is True


def test_len_returns_queue_size() -> None:
    queue = InMemoryQueue("emails")

    queue.publish(Message(payload="first"))
    queue.publish(Message(payload="second"))

    assert len(queue) == 2


def test_repr_contains_queue_information() -> None:
    queue = InMemoryQueue("emails")
    queue.publish(Message(payload="hello"))

    representation = repr(queue)

    assert "emails" in representation
    assert "size=1" in representation