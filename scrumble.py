import re
EPSILON = 0.00001


class NaN(str):
    pass


class NaNError(Exception):
    pass


def keeper(s):
    if not(isinstance(s, basestring)):
        return s
    new = []
    for i in s:
        if i in '-0123456789.,()':
            new.append(i)
        else:
            new.append(' ')
    return ''.join(new).strip()


def brackets(s):
    """
    if there are brackets in a sensible place,
    remove them and slap a - before it all.
    """
    bracketted = re.findall('(.*)\((.*)\)(.*)', s)
    if len(bracketted) != 1:
        if "(" in s or ")" in s:
            raise NaNError(NaN(s))  # brackets, but not matching ones!
        else:
            return s  # do nothing
    before, middle, after = bracketted[0]
    if has_number(before) or has_number(after):
        raise NaNError(NaN(s))  # numbers outside of brackets!
    else:
        return "-" + middle


def has_number(s):
    return any(i in s for i in "0123456789")


def nocommas(s):
    # TODO: confirm in threes.
    bad_comma = any(m.start() for m in re.finditer(',(?!\d\d\d)', s))
    if bad_comma:
        raise NaNError(NaN(s))
    else:
        return s.replace(',', '')


def nospaceafterhyphen(s):
    return re.sub('-\s*', '-', s)


def is_int(s, strict=False):
    return not(isinstance(as_int(s, strict), NaN))


def is_float(s, strict=False):
    return not(isinstance(as_float(s, strict), NaN))


def float_to_int(f):
    r = int(round(f))
    if abs(r-f) < EPSILON:
        return r
    else:
        return NaN(str(f))


def as_int(s, strict=False):
    if not(isinstance(s, basestring)):
        print type(s)
        return float_to_int(s)
    f = as_float(s, strict)
    if f is None or isinstance(f, NaN):
        return f
    else:
        return float_to_int(f)


def as_float(s, strict=False):
    try:
        s_orig = s
        if not(isinstance(s, basestring)):
            return float(s)
        if not has_number(s):
            return None
        s = brackets(s)
        s = keeper(s)
        s = nocommas(s)
        s = nospaceafterhyphen(s)
        try:
            return float(s)
        except ValueError:
            return NaN(s_orig)
    except NaNError, e:
        return NaN(s_orig)
