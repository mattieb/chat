import sys
import anthropic

from buffer_builder import build_buffer
from buffer_parser import parse_buffer
from message import Message


def to_claude_message(message: Message) -> dict:
    d = {}
    if message.role is not None:
        d["role"] = message.role
    if message.text is not None:
        d["content"] = message.text
    return d


def from_claude_message(claude_message) -> Message:
    text = "\n\n".join(
        map(lambda content_block: content_block.text, claude_message.content)
    )
    return Message(id=claude_message.id, role=claude_message.role, text=text)


def run_claude(client: anthropic.Anthropic, messages: list[Message]):
    claude_messages = list(map(to_claude_message, messages))
    return client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=10000, messages=claude_messages
    )


def main():
    with open("buffer.txt", "r") as buffer_file:
        messages = parse_buffer(buffer_file)

    client = anthropic.Anthropic()
    new_message = run_claude(client, messages)

    messages.append(from_claude_message(new_message))

    with open("buffer.txt", "w") as buffer_file:
        build_buffer(buffer_file, messages)
        buffer_file.write("====\nRole: user\n\n")


if __name__ == "__main__":
    main()
