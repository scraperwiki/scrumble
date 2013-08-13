from nose.tools import assert_equal, assert_not_equal, assert_false, assert_true

from dateutil.tz import tzoffset

import scrumble

class DateutilParseFailure:
    pass

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
    ["1234-05-06 CET",
     DateutilParseFailure,
     {'year': 1234, 'month': 5, 'day': 6},
    ],
]

def test_basic():
    for input_date, iso_output, raw_output in partial:
        x = yield do_check_dateutil_parsing, input_date, iso_output
        if not x:
            # Skip tests on inputs we know dateutil won't parse
            continue

        yield do_basic, input_date, iso_output, raw_output
        yield do_isoformat, input_date, iso_output, raw_output
        yield do_isdate, input_date, iso_output, raw_output


def do_check_dateutil_parsing(input_date, iso_output):

    try:
        scrumble.as_date(input_date)
    except ValueError:
        assert_equal(DateutilParseFailure, iso_output)
        return False
    else:
        assert_not_equal(DateutilParseFailure, iso_output)
        return True

def do_basic(input_date, iso_output, raw_output):
    return assert_equal(raw_output, dict(scrumble.as_date(input_date)))
 

def do_isoformat(input_date, iso_output, raw_output):
    try:
        iso = scrumble.as_date(input_date).isoformat()
    except scrumble.DateError:
        assert_equal(iso_output, None)
    else:
        assert_equal(iso_output, iso)


def do_isdate(input_date, iso_output, raw_output):

    if iso_output is None:
        # None is used to represent dates which aren't valid
        assert_false(scrumble.is_date(input_date), scrumble.as_date(input_date))
    else:
        assert_true(scrumble.is_date(input_date))