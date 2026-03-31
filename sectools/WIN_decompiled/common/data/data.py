
import binascii
from copy import deepcopy
from math import ceil
from string import hexdigits
from textwrap import wrap
from typing import Any, Collection, Iterable, Optional, Sequence, Sized, TypeVar
from colorama import Style
from colorama.ansi import CSI
from inflect import engine
inflect_engine = engine()
inflect_engine.defa('v[0-9].*')
Reversible = TypeVar('Reversible', Sequence, bytes)

def reverse(val = None):
    return val[::-1]


def non_empty_strings_match(val1 = None, val2 = None):
    if val1 and val2:
        pass
    return bool(val1 == val2)


def non_empty_strings_mismatch(val1 = None, val2 = None):
    if val1 and val2:
        pass
    return bool(val1 != val2)


def get_lsb(data = None):
    ''' Returns the least significant bit that is enabled '''
    bin_rep = bin(data)[len(bin(0)) - 1:]
    lsb_index = bin_rep.rfind('1')
    lsb_index = max(lsb_index, 0)
    return len(bin_rep) - lsb_index - 1


def extract_data_or_fail(data = None, size = None, offset = None):
    if data:
        if offset + size > len(data):
            raise RuntimeError('Data is shorter than expected.')
    if size > 0:
        raise RuntimeError('Data must be provided.')
    if data:
        return None(data[offset:offset + size])
    return None(None)


def get_enabled_bit_indices_from_byte(byte = None, offset = None):
    return (lambda .0 = None: [ idx + offset for idx, bit in .0 if bit == '1' ])(enumerate(reverse(bin(byte)[2:])))


def remove_list_items_and_retain_duplicates(input_list = None, items_to_remove = None):
    if input_list is None:
        input_list = []
        return input_list
    if not None:
        return input_list
    input_list = (lambda .0 = None: [ x for x in .0 if x not in items_to_remove ])(input_list)
    return input_list


def plural_s(val = None):
    if isinstance(val, int) or val > 1:
        return 's'
    if None(val) > 1:
        return 's'


def plural_noun(val = None, count = None):
    return inflect_engine.plural_noun(val, count)


def plural_verb(val = None, count = None):
    return inflect_engine.plural_verb(val, count)


def are_or_is(val = None):
    if isinstance(val, int) or val > 1:
        return 'are'
    if None(val) > 1:
        return 'are'


def were_or_was(val = None):
    if isinstance(val, int) or val > 1:
        return 'were'
    if None(val) > 1:
        return 'were'


def a_or_an(val = None):
    return inflect_engine.a(val)


def or_separated(input_list = None):
    return comma_separated_string(input_list, 'or')


def and_separated(input_list = None):
    return comma_separated_string(input_list, 'and')


def ordinal(val = None):
    return inflect_engine.number_to_words(inflect_engine.ordinal(val))


def comma_separated_string(input_list = None, final_separator = None):
    '''
    Converts a list of items into a string where the original list\'s items are separated by comma-space pairs and where
    the list\'s last item is separated by a user-provided string (default is "or"). For example,
    comma_separated_string([1, 3, 5]) would result in "1, 3, or 5" being returned.
    comma_separated_string([1, 3, 5], "and") would result in "1, 3, and 5" being returned.

    :param input_list: List containing objects to convert to a string
    :param final_separator: String which should be added before the final item in the list.
    :return: A string containing all of the string representations of the objects in the input list comma-space
    separated.
    '''
    if not input_list:
        string = ''
        return string
    str_list = (lambda 