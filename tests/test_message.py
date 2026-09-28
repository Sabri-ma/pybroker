from datetime import datetime, timezone
from uuid import UUID

import pytest

from pybroker.messaging.message import Message


def test_message_can_be_created() -> None:
    message = Message(payload="hello")

    assert message.payload == "hello"


def test_message_generates_uuid() -> None:
    message = Message(payload="hello")

    assert isinstance(message.id, UUID)


def test_messages_have_different_ids() -> None:
    first = Message(payload="first")
    second = Message(payload="second")

    assert first.id != second.id


def test_message_has_creation_timestamp() -> None:
    before = datetime.now(timezone.utc)

    message = Message(payload="hello")

    after = datetime.now(timezone.utc)

    assert before <= message.created_at <= after


def test_message_accepts_dictionary_payload() -> None:
    payload = {
        "to": "user@example.com",
        "type": "welcome",
    }

    message = Message(payload=payload)

    assert message.payload == payload


def test_message_rejects_none_payload() -> None:
    with pytest.raises(
        ValueError,
        match="Message payload cannot be None",
    ):
        Message(payload=None)