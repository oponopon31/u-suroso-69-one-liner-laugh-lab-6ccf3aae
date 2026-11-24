"""One-Liner Laugh Lab entry.

Writes a single funny line — the excuse a robot vacuum gives after
eating a sock — to /output/entry.txt (or $ENTRY_OUTPUT if set).

Pure stdlib, deterministic, no network. The program validates its own
output against the competition gate (single line, 1-200 characters,
non-blank, valid UTF-8) and fails loudly if the gate is violated.
"""

import os
import sys

LINE = (
    "Technically I didn't eat your sock. I gave it a promotion: "
    "it's now middle management in the dustbin, and it's already "
    "outperforming me."
)

OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def main() -> None:
    line = LINE.strip()

    # Gate checks — fail loudly instead of writing a bad entry.
    if not line:
        sys.exit("error: line is blank")
    if "\n" in line or "\r" in line:
        sys.exit("error: line must be a single line")
    if not 1 <= len(line) <= 200:
        sys.exit(f"error: line is {len(line)} characters, must be 1-200")

    text = line + "\n"
    encoded = text.encode("utf-8")  # raises if not valid UTF-8

    out_dir = os.path.dirname(OUTPUT_PATH)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(OUTPUT_PATH, "wb") as f:
        f.write(encoded)

    # Read-back check: confirm what landed on disk is exactly the line.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != encoded:
        sys.exit("error: read-back mismatch in written entry")
    decoded = written.decode("utf-8").rstrip("\n")
    if decoded != line:
        sys.exit("error: written entry differs from validated line")

    print(f"wrote {len(line)} characters to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
