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

    def isoformat(self):
        # TODO test me
        periods = ['year', 'month',  'day',
                   'hour',  'minute', 'second', 'microsecond']
        fstring = ['%d',   '-%02d', '-%02d',
                   'T%02d', ':%02d',  ':%02d',  '.%06d']
        builder = []
        for p, f in zip(periods, fstring):
            if p in self:
                builder.append(f % self[p])
            else:
                # TODO better error message - has skipped periods!
                assert len(builder) == len(self) - int('tzinfo' in self)
        if 'tzinfo' in self:
            # TODO better error message - timezone but no time!
            assert len(builder) > 3  # has an hour
            builder.append(datetime.time(tzinfo=self['tzinfo']).strftime("%z"))
        return ''.join(builder)


def as_date(s, default=None, **kwargs):
    if default is None:
        default = fakedate()
    return dateutil.parser.parse(s, default=default, **kwargs)
