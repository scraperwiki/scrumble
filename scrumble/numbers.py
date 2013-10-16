import unicodedata
import re
EPSILON = 0.00001


class NaN(unicode):
    pass


class NaNError(Exception):
    pass


def keeper(s, strict=False):
    if not(isinstance(s, basestring)):
        return s
    new = []
    for i in s:
        if i in '-0123456789.,()':
            new.append(i)
        else:
            u = unicodedata.category(i)
            # Unicode Character Categories
            # http://www.fileformat.info/info/unicode/category/index.htm
            if strict and u not in ["Sc", "Pd", "Zs", "Cc"]:
                raise NaNError(NaN(""))
            new.append(' ')
    return ''.join(new).strip()


def brackets(s):
    """
    if there are brackets in a sensible place,
    remove them and slap a - before it all.
    """
    bracketted = re.findall('(.*)\((.*)\)(.*)', s, flags = re.S)
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
    bad_comma = any(m.start() for m in re.finditer(',(?!\d\d\d)', s))
    if bad_comma:
        raise NaNError(NaN(s))
    else:
        return s.replace(',', '')


def nospaceafterhyphen(s):
    return re.sub('-\s*', '-', s)


def remove_space_as_thousand_separator(s):
    return re.sub(r'[ ](\d{3})\b', r'\1', s)


def as_unicode(s):
    if isinstance(s, unicode):
        return s
    try:
        return s.decode('utf-8')
    except UnicodeDecodeError:
        return s.decode('latin-1')


def is_x(s, fun, strict = False, **kwargs):
    v = fun(s, strict)
    if v is None:
        return False
    else:
        return not(isinstance(v, NaN))


def is_int(s, strict=False):
    return is_x(s, as_int, strict=strict)


def is_float(s, strict=False):
    return is_x(s, as_float, strict=strict)


def float_to_int(f):
    r = int(round(f))
    if abs(r-f) < EPSILON:
        return r
    else:
        return NaN(str(f))


def as_int(s, strict=False):
    if not(isinstance(s, basestring)):
        return float_to_int(s)
    f = as_float(s, strict)
    if f is None or isinstance(f, NaN):
        return f
    else:
        return float_to_int(f)


def as_float(s, strict=False):
    try:
        if not(isinstance(s, basestring)):
            return float(s)
        su = as_unicode(s)
        su_orig = su
        if not has_number(su):
            return None
        su = brackets(su)
        su = keeper(su, strict=strict)
        su = nocommas(su)
        su = nospaceafterhyphen(su)
        su = remove_space_as_thousand_separator(su)
        try:
            return float(su)
        except ValueError:
            return NaN(su_orig)
    except NaNError:
        return NaN(su_orig)
