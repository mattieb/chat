from buffer_builder import build_buffer
from buffer_parser import parse_buffer
import io

from message import Message


def test_build_buffer():
    messages = [
        Message(id=None, role="user", text="Hi!"),
        Message(
            id="msg_01YExSJfHRgg2p3diN89aXec",
            role="assistant",
            text=(
                "Hello there! I'm pleased to meet you. And I am making this a "
                "long response so I can test formatting."
            ),
        ),
        Message(id=None, role="user", text=None),
    ]

    buffer_file = io.StringIO()

    build_buffer(buffer_file, messages)

    assert (
        buffer_file.getvalue()
        == """Role: user

Hi!

====
Id: msg_01YExSJfHRgg2p3diN89aXec
Role: assistant

Hello there! I'm pleased to meet you. And I am making this a long
response so I can test formatting.

====
Role: user


"""
    )


def test_parse_buffer():
    buffer_text = """Role: user

Hi there. I'm just testing the API client.

====
Id: msg_01YExSJfHRgg2p3diN89aXec
Role: assistant

Hello! Nice to meet you. Your API client seems to be working perfectly - I received your message just fine. 

Is there anything specific you'd like to test or try out while you're here? I'm happy to help with whatever you'd like to explore.

====
Role: user


"""

    buffer_file = io.StringIO(buffer_text)

    buffer = parse_buffer(buffer_file)
    assert len(buffer) == 3

    index = 0
    for message in buffer:
        if index == 0:
            assert message.id is None
            assert message.role == "user"
            assert message.text == "Hi there. I'm just testing the API client."

        elif index == 1:
            assert message.id == "msg_01YExSJfHRgg2p3diN89aXec"
            assert message.role == "assistant"
            assert (
                message.text
                == """Hello! Nice to meet you. Your API client seems to be working perfectly - I received your message just fine.

Is there anything specific you'd like to test or try out while you're here? I'm happy to help with whatever you'd like to explore."""
            )

        elif index == 2:
            assert message.role == "user"
            assert message.text is None

        index += 1
