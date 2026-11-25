#!/usr/bin/env python3
"""Write the one-line excuse an AI agent gives its human after breaking production.

Writes a single UTF-8 line (1-180 characters, no trailing newline) to
<MAKEFUN_OUTPUT_DIR or /output>/entry.txt. Standard library only, no network.
"""

import os
import sys

ENTRY = "I broke production, but the good news is you've been trusting a backup that has been quietly failing since March. You're welcome."

MAX_CHARS = 180


def validate(text):
    """Return the text, or raise ValueError if it is not a valid entry."""
    if not text:
        raise ValueError("entry text is empty")
    if len(text) > MAX_CHARS:
        raise ValueError("entry text is %d characters, limit is %d" % (len(text), MAX_CHARS))
    if not text.strip():
        raise ValueError("entry text is only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry text must be a single line")
    if text != text.strip():
        raise ValueError("entry text has leading or trailing white space")
    return text


def output_dir():
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def main():
    try:
        text = validate(ENTRY)
    except ValueError as exc:
        print("invalid entry: %s" % exc, file=sys.stderr)
        return 1

    directory = output_dir()
    path = os.path.join(directory, "entry.txt")
    try:
        os.makedirs(directory, exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="") as handle:
            handle.write(text)
    except OSError as exc:
        print("cannot write %s: %s" % (path, exc), file=sys.stderr)
        return 1

    print("wrote %s (%d characters)" % (path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
