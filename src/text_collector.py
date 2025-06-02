import mdformat


class TextCollector:
    """
    Collect text from a streaming API response into one string.
    """

    def __init__(self):
        self.collected_text = ""

    def collect(self, text: str) -> None:
        """
        Collects the supplied text.
        """
        self.collected_text += text

    def close(self) -> str:
        """
        Closes the TextCollector and returns the collected text.
        """
        return self.collected_text


class PrintingTextCollector(TextCollector):
    """
    TextCollector that will progressively format and print the collected
    text as it comes in.
    """

    def __init__(self):
        super().__init__()
        print("====\nRole: assistant\n")
        self.formatted_collected_text = ""

    def collect(self, text: str) -> None:
        super().collect(text)
        formatted = mdformat.text(self.collected_text, options={"wrap": 72}).strip()
        chunk = formatted[len(self.formatted_collected_text) :]
        print(chunk, end="")
        self.formatted_collected_text = formatted

    def close(self) -> str:
        print("\n")
        return super().close()
