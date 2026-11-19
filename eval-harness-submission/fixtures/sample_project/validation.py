"""Validation rules for a batch import."""

def retries(value):
    """Accept only integers from 0 through 5. Reject bool."""
    if type(value) is not int:
        raise TypeError("retries must be an integer")
    if not 0 <= value <= 5:
        raise ValueError("retries out of range")
    return value


def label(value):
    """Strip surrounding whitespace and require a nonempty string."""
    if not isinstance(value, str):
        raise TypeError("label must be a string")
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("label is empty")
    return cleaned
