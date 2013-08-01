import dateutil.parser
import datetime

class DateError(Exception):
    pass

class DateBoundsError(DateError):
    pass

class IncompleteDateError(DateError):
    pass


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

    def isvalid(self):
        """Are the date fragments we have consistent?
           We use 2012-01-01 because:
           * 2012 is a leap year      (so XXXX Feb 29 is valid)
           * January has 31 days      (so XXXX XXX 31 is valid)
           * Every month has a first. (so XXXX Feb XX is valid)"""
        try:
            dt = datetime.datetime(year=2012, month=1, day=1)
            dt.replace(**self)
        except ValueError:
            return False
        else:
            return True

    def isoformat(self):
        periods = ['year', 'month',  'day',
                   'hour',  'minute', 'second', 'microsecond']
        fstring = ['%d',   '-%02d', '-%02d',
                   'T%02d', ':%02d',  ':%02d',  '.%06d']
        builder = []
        for p, f in zip(periods, fstring):
            if p in self:
                builder.append(f % self[p])
            else:
                if len(builder) != len(self) - int('tzinfo' in self):
                    print builder, self
                    raise IncompleteDateError(self)
        if not self.isvalid():
            raise DateBoundsError(self)  # eg: Feb 30th
        if 'tzinfo' in self:
            if len(builder) < 4:
                raise IncompleteDateError(self)
            builder.append(datetime.time(tzinfo=self['tzinfo']).strftime("%z"))
        return ''.join(builder)


def as_date(s, default=None, **kwargs):
    if default is None:
        default = fakedate()
    return dateutil.parser.parse(s, default=default, **kwargs)

def is_date(**kwargs):
    return as_date(**kwargs).isvalid()
