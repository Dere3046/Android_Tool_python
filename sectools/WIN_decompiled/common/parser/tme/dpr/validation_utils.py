
from contextlib import suppress
from itertools import chain
from typing import Any
from cmd_line_interface.sectools.metadata import CONSUMES, NA
from cmd_line_interface.sectools.tme_secure_debug.defines import defines
from cmd_line_interface.sectools.tme_secure_debug.defines.defines import ASSERT_QTI_OWNERSHIP
from common.data.data import comma_separated_string, plural_s, unhexlify2
from common.parser.tme.tme_parser.tme import TME, validate_tag_grammar

class NothingToCheck(RuntimeError):
    '''Indicates that we can skip checking.'''
    pass


def get_disjoint_bit_indices(bit_mask = None, bits = None):
    '''
    The function treats arguments as bit arrays. Arguments have to be integers.
    The bit_mask argument defines the scope - the bit set we care about. The function returns a list of bit indexes
    for bits argument that have no elements in common with the bit_mask argument.
    '''
    unfit = (bit_mask | bits) ^ bits
    return (lambda .0 = None: [ i for i in .0 if unfit >> i & 1 ])(range(unfit.bit_length()))


def get_disjoint_bit_indices_for_little_endian_hex_string(what = None, where = None):
    (a, b) = map((lambda x: if x:
int.from_bytes(unhexlify2(x), 'little', False, **('byteorder', 'signed'))), (what, where))
    return get_disjoint_bit_indices(a, b)


def common_verify_and_get(dpr = None, dp_pointer = None, dec_pointer = None, note = ('dpr', TME, 'dp_pointer', str, 'dec_pointer', str, 'note', str, 'return', tuple[(Any, Any)])):
    pass
# WARNING: Decompyle incomplete


def verify_bit_array(dpr = None, dp_pointer = None, dec_pointer = None, note = ('dpr', TME, 'dp_pointer', str, 'dec_pointer', str, 'note', str, 'return', None)):
    '''Bit array verification, tags like AuthorizedDebugVector, AuthorizedTestSignedImageVector.'''
    pass
# WARNING: Decompyle incomplete


def verify_array(dpr = None, dp_pointer = None, dec_pointer = None, note = ('dpr', TME, 'dp_pointer', str, 'dec_pointer', str, 'note', str, 'return', None)):
    '''Array verification, DebugOptions.'''
    pass
# WARNING: Decompyle incomplete


def verify_debug_options_for_qti(dpr = None, dp_pointer = None, dec_pointer = None, note = ('dpr', TME, 'dp_pointer', str, 'dec_pointer', str, 'note', str, 'return', None)):
    '''A special sub-case for verify_array for better ASSERT_QTI_OWNERSHIP error message.'''
    pass
# WARNING: Decompyle incomplete


def get_cmd_arg_by_consumed_tme_tag_name(tag_name = None):
    '''
    Return cmd line argument names list or an empty list if no match found.
    Special case. The tag_name = None can be used to list all the cmd args consumed by TME object tags.
    '''
    ret = []
# WARNING: Decompyle incomplete

