import dateutil.parser
import datetime


class fakedate(dict):
    def __nonzero__(self):
        return True

    def replace(self, **kwargs):
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
        for i, p in enumerate(periods):
            if p in self:
                builder.append(fstring[i] % self[p])
            else:
                assert len(builder) == len(self) - int('tzinfo' in self)
                # TODO better error message - has skipped periods!
        if 'tzinfo' in self:
            assert len(builder) > 3  # has an hour
            # TODO better error message - timezone but no time!
            builder.append(datetime.time(tzinfo=self['tzinfo']).strftime("%z"))
        return ''.join(builder)


def parsedate(s, default=None, **kwargs):
    if default is None:
        default = fakedate()
    return dateutil.parser.parse(s, default=default, **kwargs)

f = parsedate("2013 jan 01 11:22 +0200")
print f
print f.isoformat()
exit()
print f['month']
f = dateutil.parser.parse("01 jan 2001", default=fakedate())
print f
print f.date()

#parsedate(s) # good name?


print f.date()
print f.time()  # TODO: enforce requiring "enough" data (hours?min?sec?)
              # TODO: allow enforcing a default (ie. assume 01-Jan-XXXX)
print f.month
print f.year
