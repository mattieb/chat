import typing

import mdformat

from message import Message


def build_buffer(buffer_file: typing.IO, messages: list[Message]):
    first = True
    for message in messages:
        if not first:
            buffer_file.write("====\n")

        first = False

        if message.id is not None:
            buffer_file.write(f"Id: {message.id}\n")

        if message.role is not None:
            buffer_file.write(f"Role: {message.role}\n")

        buffer_file.write("\n")

        if message.text is not None:
            buffer_file.write(mdformat.text(message.text, options={"wrap": 72}))

        buffer_file.write("\n")
