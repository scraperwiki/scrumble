def replacer(s):
    new = []
    for i in str(s):
        if i in '0123456789.,()':
            new.append(i)
        else:
            new.append(' ')
    return ''.join(new)


def is_int(s, strict=False):
    return None


def is_float(s, strict=False):
    return None


def as_int(s, strict=False):
    return int(s)
    #return int(str(as_float(s)))

def as_float(s, strict=False):
    #r = replacer(s)
    return float(s)

