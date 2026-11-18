from unittest.mock import Mock

from parsing import parse_record
from service import batch_size
from validation import label, retries


def test_accept_valid_batch_settings():
    assert retries(2) == 2
    assert label(" blue ") == "blue"


def test_parse_valid_record():
    assert parse_record("blue:3") == ("blue", 3)


def test_fetch_batch_size():
    client = Mock()
    client.fetch_count.return_value = 3
    assert batch_size("blue", client) == 3
