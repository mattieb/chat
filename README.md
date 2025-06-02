# chat

An editor-driven client for text generators.

## Usage

Start out with buffer.txt looking something like this:

```
Role: user

Insert your text for the text generator here!
```

Then run:

```shell
uv run src/main.py
```

"buffer.txt" will be read, submitted to the text generator (currently
hardwired to Claude), text blocks reformatted, and rewritten.

When that's done, you'll be put back into your editor. Add a new
response if you wish and save to keep the conversation going.

If you're done, just quit the editor with no new text, and the loop
will exit.
