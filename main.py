"""One-sentence apology entry for make.fun.

Reads the apology from entry.txt next to this file, validates it
against the competition gate (1-200 UTF-8 characters, one sentence),
writes it to /output/entry.txt and prints it.
"""

from pathlib import Path

MAX_CHARS = 200
MIN_CHARS = 1
OUTPUT_PATH = Path("/output/entry.txt")


def load_sentence() -> str:
    """Read the apology line from entry.txt beside this file."""
    raw = Path(__file__).with_name("entry.txt").read_text(encoding="utf-8")
    return raw.strip()


def validate_sentence(sentence: str) -> None:
    """Enforce the competition gate: 1-200 chars, one clean sentence."""
    if not sentence or sentence.strip() != sentence:
        raise SystemExit("entry must be non-empty text with no surrounding whitespace")
    if not MIN_CHARS <= len(sentence) <= MAX_CHARS:
        raise SystemExit("sentence must be 1-200 characters")
    if "\n" in sentence or "\r" in sentence:
        raise SystemExit("entry must be a single line")
    if any(ord(ch) < 0x20 for ch in sentence):
        raise SystemExit("entry must not contain control characters")
    if sentence.count(".") != 1 or not sentence.endswith("."):
        raise SystemExit("entry must be exactly one sentence")


def emit(sentence: str) -> None:
    """Write the sentence to /output/entry.txt and echo it to stdout.

    The write is verified by reading the file back: the grader runs
    the program twice and the two runs must agree byte for byte, so a
    mismatch here is a hard failure rather than a silent bad gate.
    """
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(sentence, encoding="utf-8")
    written = OUTPUT_PATH.read_text(encoding="utf-8")
    if written != sentence:
        raise SystemExit("output round-trip mismatch")
    print(sentence)


def main() -> None:
    sentence = load_sentence()
    validate_sentence(sentence)
    emit(sentence)


if __name__ == "__main__":
    main()
