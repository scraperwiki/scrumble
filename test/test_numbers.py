import examples as e
import scrumble
from nose.tools import assert_equal


def test_all():
    for i in e.int_strict:
        yield cleaner_int, i, e.int_strict[i], True
    for i in e.int_loose:
        yield cleaner_int, i, e.int_loose[i], False
    for i in e.float_strict:
        yield cleaner_float, i, e.float_strict[i], True
    for i in e.float_loose:
        yield cleaner_float, i, e.float_loose[i], False

def test_things():
    assert not scrumble.is_int("<5", strict=True)


def cleaner_float(before, after, strict):
    print "FLOAT ", before, after, strict
    rval = scrumble.as_float(before, strict=strict)
    if after == scrumble.NaN:
        assert isinstance(rval, after), "got %r, isn't NaN"%rval
    else:
        assert_equal(rval, after)


def cleaner_int(before, after, strict):
    print "INT ", before, after, strict
    rval = scrumble.as_int(before, strict=strict)
    if after == scrumble.NaN:
        assert isinstance(rval, after), "got %r, isn't NaN"%rval
    else:
        assert_equal(rval, after)
