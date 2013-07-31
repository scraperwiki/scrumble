from nose.tools import assert_equal
import dates
from dateutil.tz import tzoffset

cases = [
         ["1/1990", {'year':1990, 'month':1}],
         ["31 January 2013", {'year': 2013, 'month':1, 'day':31}],
        ]


def test_basic():
    for p in cases:
        yield do_basic, p


def do_basic(p):
    return assert_equal(p[1], dict(dates.as_date(p[0])))
 
