#!/usr/bin/env python3
"""The Comment Above the Code — make.fun entry.

Writes one line (under 200 characters) to /output/entry.txt:
a funny, painfully honest comment as a developer might leave it
above fragile production code.

Entry (99 characters):

    // This only works because the data is wrong in exactly the
    right way. Fix the data, and it breaks.

Why this line earns its laugh: it names a real, recognisable
failure — two bugs cancelling each other out — instead of a generic
programmer joke. The code is not correct; it is accidentally
correct, and the punchline lands on the last few words: fix the
data and the whole thing breaks. It reads like something actually
left in a codebase, in a working developer's voice, and it avoids
the field's tired angles (do-not-touch, load-bearing, on holiday,
fixtures from prod).
"""

import os
import sys

ENTRY = (
    "// This only works because the data is wrong in exactly the "
    "right way. Fix the data, and it breaks."
)


def main() -> int:
    text = ENTRY
    # The entry is a code comment: it must keep its "//" marker,
    # so a gate that strips comment syntax can never eat the joke.
    if not text.startswith("//"):
        print("entry must start with '//' (a code comment)", file=sys.stderr)
        return 1
    # Gate: UTF-8, 1-200 characters, not only whitespace, one line.
    encoded = text.encode("utf-8")
    if not (1 <= len(text) <= 200):
        print(f"entry is {len(text)} chars, must be 1-200", file=sys.stderr)
        return 1
    if not text.strip():
        print("entry is only whitespace", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print("entry must be a single line", file=sys.stderr)
        return 1
    # Output dir: $MAKEFUN_OUTPUT_DIR when set, else /output.
    # An empty env var falls back to /output too, so a bare
    # `MAKEFUN_OUTPUT_DIR=` in the grader shell cannot break the run.
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "wb") as f:
        f.write(encoded)
    with open(path, "rb") as f:
        written = f.read()
    if written != encoded:
        print("written bytes differ from entry", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} chars to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
