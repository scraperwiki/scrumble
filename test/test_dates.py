from nose.tools import assert_equal
import scrumble
from dateutil.tz import tzoffset

partial = [
          ["mar 1982",
           "1982-03",
              {'month': 3, 'year': 1982},
           ],
          ["mar 1082 11:19",
           None,
              {'month': 3, 'year': 1082,
               'hour': 11, 'minute': 19}

           ],
          ["mar 12:01:11.1234",
           None,
              {'month': 3,
               'hour': 12, 'minute': 1, 'second': 11, 'microsecond': 123400}
           ],
          ["01 mar 2100 12:01:11.1234",
           "2100-03-01T12:01:11.123400",
              {'month': 3, 'year': 2100, 'day': 1,
               'hour': 12, 'minute': 1, 'second': 11, 'microsecond': 123400}
           ],
          ["1234-05-06T07:08:09.101112+0300",
           "1234-05-06T07:08:09.101112+0300",
              {'year': 1234, 'month': 5, 'day': 6,
               'hour': 7, 'minute': 8, 'second': 9, 'microsecond': 101112,
               'tzinfo': tzoffset(None, 3*3600)}
           ],
          ["1234-05-06T07:08:09.101112 CET",
           "1234-05-06T07:08:09.101112",  # NOTE: silently transforms to naive!
              {'year': 1234, 'month': 5, 'day': 6,
               'hour': 7, 'minute': 8, 'second': 9, 'microsecond': 101112},
           ],
          

           ]


def test_basic():
    for p in partial:
        yield do_basic, p
        yield do_isoformat, p


def do_basic(p):
    return assert_equal(p[2], dict(scrumble.as_date(p[0])))
 

def do_isoformat(p):
    try:
        iso = scrumble.as_date(p[0]).isoformat()
    except AssertionError:
        assert_equal(p[1], None)
    else:
        assert_equal(p[1], iso)
