import anthropic

from message import Message
from text_collector import TextCollector


def message_to_claude(message: Message) -> dict:
    """
    Convert our generic Message to a dict ready to submit to the Claude API.
    """

    d = {}
    if message.role is not None:
        d["role"] = message.role
    if message.text is not None:
        d["content"] = message.text
    return d


def client():
    """
    Create a Claude API client.
    """

    return anthropic.Anthropic()


def run(
    client: anthropic.Anthropic, messages: list[Message], text_collector: TextCollector
) -> Message:
    """
    Run inference on the supplied messages.

    :param client: a Claude API client

    :param messages: a list of Message objects containing the
    conversation thus far

    :param text_collector: an instantiated TextCollector responsible
    for collecting the streaming response
    """

    claude_messages = list(map(message_to_claude, messages))

    with client.messages.stream(
        model="claude-sonnet-4-20250514", max_tokens=10000, messages=claude_messages
    ) as stream:
        for text in stream.text_stream:
            text_collector.collect(text)

    text = text_collector.close()

    return Message(None, "assistant", text)
