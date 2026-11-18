"""Parse records encoded as name:count."""

from validation import label


def parse_record(line):
    """Return (stripped name, count). Count must be a nonnegative integer."""
    name, separator, count = line.partition(":")
    if not separator or ":" in count:
        raise ValueError("expected one separator")
    name = label(name)
    count = int(count)
    if count < 0:
        raise ValueError("negative count")
    return name, count
