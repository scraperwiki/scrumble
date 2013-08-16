from nose.tools import assert_equal
import scrumble

cases = [
    ["1/1990", {'year': 1990, 'month': 1}],
    ["31 January 2013", {'year': 2013, 'month': 1, 'day': 31}],
    ["2012 10", {'year': 2012, 'month': 10}],
    ["Mar 2012", {'year': 2012, 'month': 3}],
]


def test_basic():
    for p in cases:
        yield do_basic, p


def do_basic(p):
    return assert_equal(p[1], dict(scrumble.as_date(p[0])))
