#!/usr/bin/env python3
"""Entry program for news-image-20261126.

Copies the repository's entry.png — a one-image summary of the world
news of Thursday 26 November 2026 — into the output directory the
grader names.  Standard library only, no network, deterministic:
every run writes exactly the same bytes.
"""

import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")

    with open(SOURCE, "rb") as fh:
        data = fh.read()
    if not data.startswith(PNG_MAGIC):
        print("entry.png is not a PNG", file=sys.stderr)
        return 1
    if len(data) > MAX_BYTES:
        print("entry.png exceeds the 1 MiB limit", file=sys.stderr)
        return 1

    with open(dest, "wb") as fh:
        fh.write(data)

    # Read the copy back and prove it is byte-identical to the source,
    # so a truncated or corrupted write can never pass silently.
    with open(dest, "rb") as fh:
        written = fh.read()
    if hashlib.sha256(written).digest() != hashlib.sha256(data).digest():
        print("written file does not match entry.png", file=sys.stderr)
        return 1
    print(f"wrote {dest} ({len(data)} bytes, sha256 verified)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
