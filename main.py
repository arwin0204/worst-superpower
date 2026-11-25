#!/usr/bin/env python3
"""Worst Superpower — make.fun bounty u-suroto-worst-superpower-461dcdbe.

Writes one line (at most 140 characters) inventing the most useless
superpower to ``entry.txt`` in the grader's output directory.

Output contract (program/v1): the output directory comes from the
``MAKEFUN_OUTPUT_DIR`` environment variable, falling back to ``/output``
inside the grader container. This program writes ONLY there — never into
the repository directory, which the grader mounts read-only.

Deterministic, standard library only, no network, no randomness, no clock.
"""

import os
import sys

# The entry: a power that works exactly as advertised and still achieves
# nothing — reading any book by touch, but only ever the copyright page.
ENTRY = "I can read any book just by touching it, but only the copyright page."

MAX_CHARS = 140


def resolve_output_dir() -> str:
    """Return the grader's output directory for this run."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def _is_inside(path: str, parent: str) -> bool:
    return os.path.commonpath(
        [os.path.abspath(path), os.path.abspath(parent)]
    ) == os.path.abspath(parent)


def main() -> int:
    entry = ENTRY
    if not entry.strip():
        print("error: entry is blank", file=sys.stderr)
        return 1
    if len(entry) > MAX_CHARS:
        print(
            "error: entry is %d characters, over the %d limit"
            % (len(entry), MAX_CHARS),
            file=sys.stderr,
        )
        return 1

    output_dir = resolve_output_dir()
    # Hard guard: never write into the repository tree. The grader mounts
    # the repo read-only, so writing there fails the run; the output dir
    # must be the harness-provided directory (or /output in the grader).
    repo_dir = os.path.dirname(os.path.abspath(__file__))
    if _is_inside(output_dir, repo_dir):
        print(
            "error: output dir %r is inside the repository %r; refusing"
            % (output_dir, repo_dir),
            file=sys.stderr,
        )
        return 1

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    # No trailing newline: the file holds exactly the one line, nothing else.
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(entry)
    # Read back and confirm the file on disk is byte-for-byte the entry.
    with open(path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != entry:
        print("error: read-back mismatch in %s" % path, file=sys.stderr)
        return 1
    print("wrote %s (%d characters)" % (path, len(entry)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
