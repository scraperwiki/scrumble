# -*- coding: utf-8 -*-

from cleaner import NaN
import cleaner

def stitch(l):
    d={}
    for i in l:
        d.update(i)
    return d
    
strict_ints = {
    0: 0,
    -1: -1,
    1: 1,
    1.0: 1,
    -1.0: -1,
    1.5: NaN,
    "0": 0,
    "1": 1,
    "1.0": 1,
    "1.00000004": 1,
    "2.9999995": 3,
    "3.14159": NaN,
    "1020": 1020,
    "1,020": 1020,
    "-4": -4,
    "(14)": -14,
    "1,010,444.00": 1010444,
    "   \t\r\n\n\r2,021.00\r  \r\n\xa0": 2021,
    "1,01": NaN,
    "": None,
    "...": None,
    "NA": None,
    "12 14": NaN,
    "$1000": 1000
}

loose_ints = {
    "3 cats": 3,
    "2.0 cats": 2,
    "2.4 children": NaN,
    "-12 cats": -12,
    u"\U0001F4A9 42 ostrich": 42,
}

strict_floats = {
    1.5: 1.5,
    -1.5: -1.5,
    1.00001: 1.00001,
    "3.14159": 3.14159,
    "1,201.22": 1201.22,
    "99,999,999.999": 99999999.999,
    "£10101.22": 10101.22,
    "($5.4)": -5.4,
    "(3.1₱)": -3.1,
}

loose_floats = {
    "2.4 children": 2.4,
    "(3.1 BZ$)": -3.1,
    "[2.2]": 2.2,
}

int_strict = stitch([strict_ints])
int_loose = stitch([strict_ints, loose_ints])
float_strict = stitch([strict_ints, strict_floats])
float_loose = stitch([strict_ints, loose_ints, strict_floats, loose_floats])

ops = [
      [int_strict, cleaner.as_int, True],
      [int_loose, cleaner.as_int, False],
      [float_strict, cleaner.as_float, True],
      [float_loose, cleaner.as_float, False],
      ]
def alltests():
    
    for op in ops:
        testcases, function, strict = op
        for test in testcases:
            rval = function(test, strict=strict)
            if testcases[test] == NaN:
                assert isinstance(rval, NaN)
            else:
                assert function(test, strict=strict) == testcases[test]
    
