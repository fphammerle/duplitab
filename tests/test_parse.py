import pytest

import datetime
import duplitab

@pytest.mark.parametrize(('duplicity_timestamp', 'expected'), [
    ['Tue Oct 11 11:02:01 2016', datetime.datetime(2016, 10, 11, 11, 2, 1)],
])
def test_parse_duplicity_timestamp(duplicity_timestamp, expected):
    assert expected == duplitab._parse_duplicity_timestamp(duplicity_timestamp)
