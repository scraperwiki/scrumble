import examples as e
import cleaner
from nose.tools import assert_equal, assert_raises


def test_all():
    for i in e.int_strict:
        yield cleaner_int, i, e.int_strict[i], True
    for i in e.int_loose:
        yield cleaner_int, i, e.int_loose[i], False
    for i in e.float_strict:
        yield cleaner_float, i, e.float_strict[i], True
    for i in e.float_loose:
        yield cleaner_float, i, e.float_loose[i], False
       
def cleaner_float(before, after, strict):
    if isinstance(after, Exception):
        assert_raises(cleaner.as_float(before, strict=strict))
    else:
        assert_equal(cleaner.as_float(before, strict=strict), after)

def cleaner_int(before, after, strict):
    if isinstance(after, Exception):
        assert_raises(cleaner.as_int(before, strict=strict))
    else:
        assert_equal(cleaner.as_int(before, strict=strict), after)
