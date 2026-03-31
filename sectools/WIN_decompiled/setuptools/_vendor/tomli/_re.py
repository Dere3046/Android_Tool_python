
from __future__ import annotations
from datetime import date, datetime, time, timedelta, timezone, tzinfo
from functools import lru_cache
import re
from typing import Any
from _types import ParseFloat
_TIME_RE_STR = '([01][0-9]|2[0-3]):([0-5][0-9]):([0-5][0-9])(?:\\.([0-9]{1,6})[0-9]*)?'
RE_NUMBER = re.compile('\n0\n(?:\n    x[0-9A-Fa-f](?:_?[0-9A-Fa-f])*   # hex\n    |\n    b[01](?:_?[01])*                 # bin\n    |\n    o[0-7](?:_?[0-7])*               # oct\n)\n|\n[+-]?(?:0|[1-9](?:_?[0-9])*)         # dec, integer part\n(?P<floatpart>\n    (?:\\.[0-9](?:_?[0-9])*)?         # optional fractional part\n    (?:[eE][+-]?[0-9](?:_?[0-9])*)?  # optional exponent part\n)\n', re.VERBOSE, **('flags',))
RE_LOCALTIME = re.compile(_TIME_RE_STR)
RE_DATETIME = re.compile(f'''\n([0-9]{{4}})-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])  # date, e.g. 1988-10-27\n(?:\n    [Tt ]\n    {_TIME_RE_STR}\n    (?:([Zz])|([+-])([01][0-9]|2[0-3]):([0-5][0-9]))?  # optional time offset\n)?\n''', re.VERBOSE, **('flags',))

def match_to_datetime(match = None):
    '''Convert a `RE_DATETIME` match to `datetime.datetime` or `datetime.date`.

    Raises ValueError if the match does not correspond to a valid date
    or datetime.
    '''
    (year_str, month_str, day_str, hour_str, minute_str, sec_str, micros_str, zulu_time, offset_sign_str, offset_hour_str, offset_minute_str) = match.groups()
    year = int(year_str)
    month = int(month_str)
    day = int(day_str)
    if hour_str is None:
        return date(year, month, day)
    hour = None(hour_str)
    minute = int(minute_str)
    sec = int(sec_str)
    micros = int(micros_str.ljust(6, '0')) if micros_str else 0
    if offset_sign_str:
        tz = cached_tz(offset_hour_str, offset_minute_str, offset_sign_str)
    elif zulu_time:
        tz = timezone.utc
    else:
        tz = None
    return datetime(year, month, day, hour, minute, sec, micros, tz, **('tzinfo',))


def cached_tz(hour_str = None, minute_str = None, sign_str = lru_cache(None, **('maxsize',))):
    sign = 1 if sign_str == '+' else -1
    return timezone(timedelta(sign * int(hour_str), sign * int(minute_str), **('hours', 'minutes')))

cached_tz = None(cached_tz)

def match_to_localtime(match = None):
    (hour_str, minute_str, sec_str, micros_str) = match.groups()
    micros = int(micros_str.ljust(6, '0')) if micros_str else 0
    return time(int(hour_str), int(minute_str), int(sec_str), micros)


def match_to_number(match = None, parse_float = None):
    if match.group('floatpart'):
        return parse_float(match.group())
    return None(match.group(), 0)

