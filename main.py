#!/usr/bin/env python3
"""One Star for Monday — writes one one-star review of Monday, written as
though Monday were a restaurant, to /output/entry.txt.

The line is a diner's complaint with a real arc: the server took the order,
brought the wrong dish (five days of work), and forgot the weekend — the
joke only Monday can tell, since Monday opens the five-day work stretch and
ends the weekend.

Why this line, over the other candidates drafted for the brief:
- It keeps the full restaurant arc (server, order, wrong dish, missing
  item) instead of only one complaint detail, so it reads as a genuine
  one-star review rather than a caption about Monday.
- It carries two Monday-only anchors at once: "five days of work" (the
  stretch Monday opens) and "forgot the weekend" (the weekend Monday
  ends), so the joke could not be about any other day of the week.
- At 17 words it is short enough to retype into a group chat without
  trimming a word, which is what the weary-office-worker judge keeps.

Stdlib only, deterministic, no network, no randomness.
"""
import hashlib
import os
import sys

ENTRY = ("The server took my order, brought me five days of work, "
         "and forgot the weekend. One star.")

MAX_CHARS = 180
MAX_WORDS = 25


def validate(text):
    """Enforce the competition gate: 1-180 chars, not only whitespace,
    and the task's own cap of at most 25 words on a single line."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if len(text) == 0:
        raise ValueError("entry is empty (gate needs 1-180 characters)")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the 180-character gate"
        )
    if len(text.split()) > MAX_WORDS:
        raise ValueError(
            f"entry is {len(text.split())} words, over the 25-word cap"
        )
    if text.strip() == "":
        raise ValueError("entry is only whitespace")
    if text != text.strip():
        raise ValueError("entry has leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    return text


def self_test():
    """Exercise validate() against the gate's rejection cases."""
    cases = [
        ("", "empty"),
        (" ", "whitespace-only"),
        ("x" * 181, "181 chars"),
        ("word " * 25 + "word", "26 words"),
        ("a\nb", "multi-line"),
        ("trailing ", "trailing whitespace"),
        (" leading", "leading whitespace"),
    ]
    for text, label in cases:
        try:
            validate(text)
        except ValueError as exc:
            print(f"self-test ok: rejected {label}: {exc}")
        else:
            raise SystemExit(f"self-test FAIL: {label} was accepted")
    # boundary: exactly 180 chars must pass
    validate("y" * 180)
    print("self-test ok: 180-char boundary accepted")
    print("self-test: all cases passed")
    return 0


def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--self-test":
        return self_test()
    if len(sys.argv) > 1:
        print("usage: main.py [--self-test]", file=sys.stderr)
        return 2
    out_path = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")
    text = validate(ENTRY)
    data = text.encode("utf-8")
    parent = os.path.dirname(out_path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(out_path, "wb") as fh:
        fh.write(data)  # no trailing newline: the file is exactly the line
    with open(out_path, "rb") as fh:
        roundtrip = fh.read()
    if roundtrip != data:
        raise SystemExit("round-trip mismatch: file does not match entry")
    print(f"wrote {out_path}: {len(text)} chars, {len(text.split())} words, "
          f"sha256 {hashlib.sha256(data).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
