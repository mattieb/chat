from typing import NamedTuple


class Message(NamedTuple):
    id: str | None
    role: str | None
    text: str | None
