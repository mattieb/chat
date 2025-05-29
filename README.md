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

Now, edit "buffer.txt" again to add more text, and keep on keepin'
on just like that.
