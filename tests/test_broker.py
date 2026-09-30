import pytest

from pybroker.broker import Broker
from pybroker.messaging.message import Message


def test_broker_starts_without_queues() -> None:
    broker = Broker()

    assert broker.queue_count == 0


def test_create_queue() -> None:
    broker = Broker()

    queue = broker.create_queue("emails")

    assert queue.name == "emails"
    assert broker.queue_count == 1
    assert broker.queue_exists("emails") is True


def test_create_existing_queue_returns_same_queue() -> None:
    broker = Broker()

    first = broker.create_queue("emails")
    second = broker.create_queue("emails")

    assert first is second
    assert broker.queue_count == 1


def test_get_existing_queue() -> None:
    broker = Broker()

    created = broker.create_queue("emails")
    retrieved = broker.get_queue("emails")

    assert retrieved is created


def test_get_missing_queue_returns_none() -> None:
    broker = Broker()

    assert broker.get_queue("missing") is None


def test_queue_name_is_trimmed() -> None:
    broker = Broker()

    queue = broker.create_queue("  emails  ")

    assert queue.name == "emails"
    assert broker.queue_exists("emails") is True


def test_empty_queue_name_is_rejected() -> None:
    broker = Broker()

    with pytest.raises(
        ValueError,
        match="Queue name cannot be empty",
    ):
        broker.create_queue("   ")


def test_non_string_queue_name_is_rejected() -> None:
    broker = Broker()

    with pytest.raises(
        TypeError,
        match="Queue name must be a string",
    ):
        broker.create_queue(123)  # type: ignore[arg-type]


def test_publish_creates_queue_automatically() -> None:
    broker = Broker()
    message = Message(payload="hello")

    broker.publish("emails", message)

    assert broker.queue_exists("emails") is True
    assert broker.queue_count == 1


def test_publish_stores_message_in_queue() -> None:
    broker = Broker()
    message = Message(payload="hello")

    broker.publish("emails", message)

    queue = broker.get_queue("emails")

    assert queue is not None
    assert queue.size == 1
    assert queue.peek() == message


def test_publish_multiple_messages() -> None:
    broker = Broker()

    first = Message(payload="first")
    second = Message(payload="second")

    broker.publish("emails", first)
    broker.publish("emails", second)

    queue = broker.get_queue("emails")

    assert queue is not None
    assert queue.size == 2
    assert queue.peek() == first


def test_publish_rejects_non_message_object() -> None:
    broker = Broker()

    with pytest.raises(
        TypeError,
        match="Broker can only publish Message instances",
    ):
        broker.publish(
            "emails",
            "hello",  # type: ignore[arg-type]
        )


def test_consume_returns_message() -> None:
    broker = Broker()
    message = Message(payload="hello")

    broker.publish("emails", message)

    result = broker.consume("emails")

    assert result == message


def test_consume_removes_message_from_queue() -> None:
    broker = Broker()
    message = Message(payload="hello")

    broker.publish("emails", message)

    broker.consume("emails")

    queue = broker.get_queue("emails")

    assert queue is not None
    assert queue.size == 0


def test_consume_respects_fifo_order() -> None:
    broker = Broker()

    first = Message(payload="first")
    second = Message(payload="second")
    third = Message(payload="third")

    broker.publish("emails", first)
    broker.publish("emails", second)
    broker.publish("emails", third)

    assert broker.consume("emails") == first
    assert broker.consume("emails") == second
    assert broker.consume("emails") == third


def test_consume_empty_queue_returns_none() -> None:
    broker = Broker()

    broker.create_queue("emails")

    assert broker.consume("emails") is None


def test_consume_missing_queue_returns_none() -> None:
    broker = Broker()

    assert broker.consume("missing") is None