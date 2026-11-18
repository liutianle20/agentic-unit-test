"""Look up batch sizes through an injected client."""

from validation import label


def batch_size(name, client):
    """Return client.fetch_count for a normalized name, or 0 on KeyError."""
    name = label(name)
    try:
        return client.fetch_count(name)
    except KeyError:
        return 0
