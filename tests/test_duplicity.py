import pytest

import duplitab


def test_command_failure_msg():
    with pytest.raises(duplitab.DuplicityCommandFailedError) as exinfo:
        duplitab._duplicity(['--unsupported-duplitab-test-param'])
    assert '--unsupported-duplitab-test-param' in exinfo.value.msg
