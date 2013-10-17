import dateutil.parser
import datetime

class DateError(Exception):
    pass

class DateBoundsError(DateError):
    pass

class IncompleteDateError(DateError):
    pass

PERIODS = ['year', 'month',  'day',
           'hour',  'minute', 'second', 'microsecond']

class PartialDate(dict):
    touched = False

    def __nonzero__(self):
        """needed because dateutil checks 'if default',
           instead of 'if default is None'"""
        if not self.touched:
            return True
        else:
            return bool(dict(self))

    def replace(self, **kwargs):
        """replicates datetime behaviour;
           resets nonzero to ensure minimal surprise"""
        self.touched = True
        self.update(dict(kwargs))
        return self

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError("fakedate doesn't contain a %r" % name)

    def datetime(self, default=None):
        if default:
            d = default.replace(**self)
            return datetime.datetime(d)
        else:
            return datetime.datetime(**self)

    def is_contiguously_specified(self, require_year=False):
        """
        A date is contiguously specified if there is no gap between
        time periods: e.g. if there is a year and a day, there must be a month.
        """

        if require_year and "year" not in self:
            return False

        no_further = seen_period = False

        for p in PERIODS:
            if p in self:
                if no_further:
                    # There aren't supposed to be any other periods specified.
                    # The date isn't contiguous.
                    return False

                # We've encountered a period
                seen_period = True

            elif seen_period:
                # We've seen a period, and now also a gap. There shouldn't be
                # further date fragments.
                no_further = True

        return True

    def is_valid(self):
        """
        Is the date represented by self a valid date on the gregorian calendar?

        Are the date fragments we have consistent?
        We use 2012-01-01 because:
        * 2012 is a leap year      (so XXXX Feb 29 is valid)
        * January has 31 days      (so XXXX XXX 31 is valid)
        * Every month has a first. (so XXXX Feb XX is valid)
        """
        try:
            dt = datetime.datetime(year=2012, month=1, day=1)
            dt.replace(**self)
        except ValueError:
            return False
        else:
            return True

    def isoformat(self):
        """
        Return this PartialDate as a valid partial ISO8601 formatted string.
        e.g, 1234, 1234-05-06, 1234-05-06T07:08
        """
        fstring = ['%d',   '-%02d', '-%02d',
                   'T%02d', ':%02d',  ':%02d',  '.%06d']
        builder = []

        if not self.is_contiguously_specified(require_year=True):
            raise IncompleteDateError(self)

        for p, f in zip(PERIODS, fstring):
            if p in self:
                builder.append(f % self[p])

        if not self.is_valid():
            raise DateBoundsError(self)  # eg: Feb 30th

        if 'tzinfo' in self:
            # If a tzinfo is present, it doesn't make sense to be missing an
            # hour:
            if "hour" not in self:
                raise IncompleteDateError(self)

            builder.append(datetime.time(tzinfo=self['tzinfo']).strftime("%z"))

        return ''.join(builder)


def as_date(inputstring, default=None, fallback=Exception, **kwargs):
    """
    Attempts to return an inputstring as a partial date.

    Currently implemented using dateutil.parser.parse.

    Valid kwargs:

        parserinfo (a dateutil.parser.parserinfo instance)
        default: a template for the returned value; datetime-like, must
                 implement replace and be truthy
        ignoretz (parse): don't interpret timezone
        tzinfos (parse): datetime.tzinfo instance
        dayfirst (_parse): hint that that day is probably first
        yearfirst (_parse): hint that the year is probably first
        fuzzy (_parse): tolerate more malformed strings
    """
    if default is None:
        default = PartialDate()
    try:
        return dateutil.parser.parse(inputstring, default=default, **kwargs)
    except Exception:
        if fallback == Exception: raise
        return fallback

def is_date(inputstring, **kwargs):
    try:
        d = as_date(inputstring, **kwargs)
    except ValueError:  # dateutil hated the string.
        return False
    if not d.is_contiguously_specified():
        return False
    return d.is_valid()
