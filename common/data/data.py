"""
Data utility functions
Based on decompiled analysis
"""

import binascii
from copy import deepcopy
from math import ceil
from string import hexdigits
from textwrap import wrap
from typing import Any, Collection, Iterable, Optional, Sequence, Sized, TypeVar

# Type variables
Reversible = TypeVar('Reversible', Sequence, bytes)


def reverse(val):
    """Reverse sequence"""
    return val[::-1]


def non_empty_strings_match(val1, val2):
    """Check if two non-empty strings match"""
    if val1 and val2:
        return val1 == val2
    return False


def non_empty_strings_mismatch(val1, val2):
    """Check if two non-empty strings mismatch"""
    if val1 and val2:
        return val1 != val2
    return False


def get_lsb(data):
    """Return index of least significant bit (enabled bit)"""
    if data == 0:
        return -1
    bin_rep = bin(data)[2:]  # Remove '0b' prefix
    lsb_index = bin_rep.rfind('1')
    return len(bin_rep) - lsb_index - 1


def extract_data_or_fail(data, size, offset=0):
    """Extract specified size from data, fail if insufficient"""
    if data is None:
        if size > 0:
            raise RuntimeError('Data must be provided.')
        return memoryview(b'')

    if offset + size > len(data):
        raise RuntimeError('Data is shorter than expected.')

    return memoryview(data[offset:offset + size])


def get_enabled_bit_indices_from_byte(byte, offset=0):
    """Get list of enabled bit indices from byte"""
    indices = []
    for i in range(8):
        if byte & (1 << i):
            indices.append(i + offset)
    return indices


def remove_list_items_and_retain_duplicates(input_list, items_to_remove):
    """Remove specified items from list, retain duplicates"""
    if input_list is None:
        return []

    if not items_to_remove:
        return input_list

    return [x for x in input_list if x not in items_to_remove]


def plural_s(val):
    """Return plural 's' suffix based on value"""
    if isinstance(val, int):
        return 's' if val > 1 else ''
    elif isinstance(val, (list, tuple, set)):
        return 's' if len(val) > 1 else ''
    return ''


def a_or_an(val):
    """Return appropriate article 'a' or 'an'"""
    if not val:
        return 'a'

    val_str = str(val)
    first_char = val_str[0].lower()

    # Use 'an' for words starting with vowel sounds
    vowels = ('a', 'e', 'i', 'o', 'u')
    if first_char in vowels:
        return 'an'
    return 'a'


def and_separated(input_list):
    """Join list items with 'and'"""
    if not input_list:
        return ''

    if len(input_list) == 1:
        return str(input_list[0])

    if len(input_list) == 2:
        return f"{input_list[0]} and {input_list[1]}"

    return ', '.join(str(item) for item in input_list[:-1]) + f', and {input_list[-1]}'


def or_separated(input_list):
    """Join list items with 'or'"""
    if not input_list:
        return ''

    if len(input_list) == 1:
        return str(input_list[0])

    if len(input_list) == 2:
        return f"{input_list[0]} or {input_list[1]}"

    return ', '.join(str(item) for item in input_list[:-1]) + f', or {input_list[-1]}'


def ceil_to_multiple(value, multiple):
    """Round up to nearest multiple"""
    if multiple == 0:
        return value
    return ((value + multiple - 1) // multiple) * multiple


def floor_to_multiple(value, multiple):
    """Round down to nearest multiple"""
    if multiple == 0:
        return value
    return (value // multiple) * multiple


def align_to(value, alignment):
    """Align to specified boundary"""
    return ceil_to_multiple(value, alignment)


def numbered_string(items):
    """Add numbering to list items"""
    if not items:
        return ""

    result = []
    for i, item in enumerate(items, 1):
        result.append(f"{i}. {item}")

    return "\n".join(result)


def unhexlify2(hex_str):
    """Convert hex string to bytes, handle possible 0x prefix"""
    if hex_str.startswith('0x') or hex_str.startswith('0X'):
        hex_str = hex_str[2:]

    # Ensure even length
    if len(hex_str) % 2 != 0:
        hex_str = '0' + hex_str

    return binascii.unhexlify(hex_str)


def is_congruent(val1, val2, modulus):
    """Check if two values are congruent modulo a number"""
    if modulus == 0:
        return True
    return (val1 % modulus) == (val2 % modulus)


def hex_val(val, num_chars=None, prefix='0x'):
    """Convert value to hex string"""
    if val is None:
        return 'None'
    
    hex_str = hex(val)
    if hex_str.startswith('0x') or hex_str.startswith('0X'):
        hex_str = hex_str[2:]
    
    if num_chars is not None:
        hex_str = hex_str.zfill(num_chars)
    
    return f"{prefix}{hex_str}"


def properties_repr(obj, properties):
    """Generate string representation of object properties"""
    lines = []
    for prop in properties:
        if isinstance(prop, (list, tuple)):
            lines.append(f"{prop[0]}: {prop[1]}")
        else:
            name = prop
            value = getattr(obj, prop, None)
            lines.append(f"{name}: {value}")
    return '\n'.join(lines)


def wrap_text(text, width=80):
    """Wrap text to specified width"""
    return wrap(text, width=width)
