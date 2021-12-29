from datetime import date

import pytest

from pondus.core import util


def test_str2date():
    result = util.str2date("2021-12-28")
    assert result == date(2021, 12, 28)

    with pytest.raises(ValueError):
        result = util.str2date("foo")

def test_nonemin():
    result = util.nonemin([1,2,3])
    assert result == 1

    result = util.nonemin([1,2,3, None])
    assert result == 1

    # TODO: Fix
    # result = util.nonemin([1,2,3, "asd"])
    # assert result is None
