import dateutil.parser
import datetime


class fakedate(dict):
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

    # TODO: decide if automatic datetime-ing is in, out, or optional
    def __getattr__(self, name):
        if name in self:
            return self[name]
        else:
            return getattr(self.datetime(), name)

    def datetime(self, default=None):
        if default:
            d = default.replace(**self)
            return datetime.datetime(d)
        else:
            return datetime.datetime(**self)

    def isvalid(self):
        try:
            dt = datetime.datetime(year=2013, month=1, day=1)
            dt.replace(**self)
        except ValueError:
            return False
        else:
            return True

    def isoformat(self):
        # TODO better error type: example 2013-02-29
        assert self.isvalid(), "Inappropriate values: %r" % self
        periods = ['year', 'month',  'day',
                   'hour',  'minute', 'second', 'microsecond']
        fstring = ['%d',   '-%02d', '-%02d',
                   'T%02d', ':%02d',  ':%02d',  '.%06d']
        builder = []
        for p, f in zip(periods, fstring):
            if p in self:
                builder.append(f % self[p])
            else:
                # TODO better error type
                assert len(builder) == len(self) - int('tzinfo' in self), \
                    "Skips time periods: %r" % self
        if 'tzinfo' in self:
            # TODO better error type
            assert len(builder) > 3, \
                "Has timezone but no time: %r" % self  # has an hour
            builder.append(datetime.time(tzinfo=self['tzinfo']).strftime("%z"))
        return ''.join(builder)


def as_date(s, default=None, **kwargs):
    if default is None:
        default = fakedate()
    return dateutil.parser.parse(s, default=default, **kwargs)
