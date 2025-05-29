import typing
from message import Message


def parse_buffer(buffer_file: typing.IO):
    id: str | None = None
    role: str | None = None
    text: str | None = None
    reading_header: bool = True
    messages: list[Message] = []

    def append(id: str | None, role: str | None, text: str | None):
        if text is not None:
            text = text.strip()
        if text == "":
            text = None
        messages.append(Message(id, role, text))

    for line in buffer_file:
        line = line.strip()
        if reading_header:
            if len(line) == 0:
                reading_header = False
                continue

            name, value = line.split(": ")
            if name == "Id":
                id = value
            elif name == "Role":
                role = value
            else:
                raise ValueError(f"unknown header {repr(name)}")
            continue

        else:
            if line == "====":
                append(id, role, text)
                id: str | None = None
                role: str | None = None
                text: str | None = None
                reading_header: bool = True
                continue

            if text is None:
                text = ""

            text = text + line + "\n"
            continue

    append(id, role, text)
    return messages
