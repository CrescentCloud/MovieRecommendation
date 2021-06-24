import pytest

from pandas import Index, Series
import pandas._testing as tm


class TestSeriesDelItem:
    def test_delitem(self):
        # GH#5542
        # should delete the item inplace
        s = Series(range(5))
        del s[0]

        expected = Series(range(1, 5), index=range(1, 5))
        tm.assert_series_equal(s, expected)

        del s[1]
        expected = Series(range(2, 5), index=range(2, 5))
        tm.assert_series_equal(s, expected)

        # only 1 left, del, add, del
        s = Series(1)
        del s[0]
        tm.assert_series_equal(s, Series(dtype="int64", index=Index([], dtype="int64")))
        s[0] = 1
        tm.assert_series_equal(s, Series(1))
        del s[0]
        tm.assert_series_equal(s, Series(dtype="int64", index=Index([], dtype="int64")))

    def test_delitem_object_index(self):
        # Index(dtype=object)
        s = Series(1, index=["a"])
        del s["a"]
        tm.assert_series_equal(
            s, Series(dtype="int64", index=Index([], dtype="object"))
        )
        s["a"] = 1
        tm.assert_series_equal(s, Series(1, index=["a"]))
        del s["a"]
        tm.assert_series_equal(
            s, Series(dtype="int64", index=Index([], dtype="object"))
        )

    def test_delitem_missing_key(self):
        # empty
        s = Series(dtype=object)

        with pytest.raises(KeyError, match=r"^0$"):
            del s[0]
