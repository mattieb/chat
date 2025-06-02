import os
import shutil
import subprocess
import sys

from buffer_builder import build_buffer
from buffer_parser import parse_buffer
import claude
from message import Message
from text_collector import PrintingTextCollector


def get_editor():
    editor = os.environ.get("EDITOR")
    if editor is not None:
        return editor
    editor = shutil.which("vi")
    if editor is not None:
        return editor
    raise RuntimeError("EDITOR not set and fallback not found")


def count_lines(path: str) -> int:
    """
    Count the lines in the file at a supplied path.
    """
    line_count = 0
    with open(path, "r") as buffer_file:
        for _ in buffer_file:
            line_count += 1
    return line_count


def read_or_create_buffer(buffer_path: str) -> list[Message]:
    try:
        with open(buffer_path, "r") as buffer_file:
            messages = parse_buffer(buffer_file)

    except FileNotFoundError:
        messages = [Message(None, "user", None)]
        with open(buffer_path, "w") as buffer_file:
            build_buffer(buffer_file, messages)

    return messages


def main():
    editor = get_editor()
    buffer_path = sys.argv[1]
    client = claude.client()

    messages = read_or_create_buffer(buffer_path)

    build_buffer(sys.stdout, messages[:-1])

    while True:
        line_count = count_lines(buffer_path)
        subprocess.run([editor, f"+{line_count}", buffer_path], check=True)

        with open(buffer_path, "r") as buffer_file:
            messages = parse_buffer(buffer_file)

        if messages[-1].text is None:
            sys.exit(0)

        print("====")
        build_buffer(sys.stdout, messages[-1:])

        text_collector = PrintingTextCollector()

        new_message = claude.run(client, messages, text_collector)

        messages.append(new_message)

        with open(buffer_path, "w") as buffer_file:
            messages.append(Message(None, "user", None))
            build_buffer(buffer_file, messages)


if __name__ == "__main__":
    main()
