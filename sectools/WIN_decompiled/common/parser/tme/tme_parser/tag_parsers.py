
'''
Generic/parent parsers for TME format.
'''
from abc import ABC, abstractmethod
from collections import defaultdict
from contextlib import suppress
from functools import reduce
from itertools import filterfalse, groupby
from operator import add, itemgetter, or_
from struct import error, pack, unpack, unpack_from
from typing import Any, Dict, Iterable, List, Optional, Tuple, Union, cast
from common.data.data import comma_separated_string, hexlify2, unhexlify2
from common.parser.tme.tme_parser.defines import SharedState, Tag
from common.parser.tme.tme_parser.exceptions import NormalizationNotImplemented, ProtocolError, ProtocolErrorTagUnknown, ProtocolParsingError, ProtocolVersionError

class GenericParser:
    '''
    The TME parser. The ParserBase accepts multiple data types/formats and normalizes the data first.
    The normalized data is generically not identical to possible data representations (e.g., binary, JSON, etc.).
    '''
    
    def __init__(self = None, data = None, state = None):
        del state
        self.normalized_data = self.normalize_data(data)
        self.validate_normalized_data(self.normalized_data)

    
    def normalize_data(self = None, data = None):
        '''Normalize the data to a canonical (for the given class type) form.
        That method dispatches provided data to a proper parsing.'''
        if isinstance(data, int):
            ret = self.normalize_int(data)
            return ret
    # WARNING: Decompyle incomplete

    
    def validate_normalized_data(self = None, normalized_data = None):
        '''Verify canonical data integrity. Should throw on error.'''
        pass

    
    def normalize_int(self = None, int_data = None):
        '''Override for an appropriate integer (python object) normalization (decoding)'''
        raise NormalizationNotImplemented(f'''The int normalization is not implemented for `{self.__class__.__name__}`''')

    
    def normalize_str(self = None, str_data = None):
        '''Override for an appropriate string (python object) normalization (decoding)'''
        raise NormalizationNotImplemented(f'''The str normalization is not implemented for `{self.__class__.__name__}`''')

    
    def normalize_bytearray(self = None, bytearray_data = None):
        '''Override for an appropriate byte array normalization (decoding).'''
        raise NormalizationNotImplemented(f'''The byte array normalization is not implemented for `{self.__class__.__name__}`''')

    
    def normalize_bytes(self = None, bytes_data = None):
        '''Override for an appropriate bytes normalization (decoding).'''
        raise NormalizationNotImplemented(f'''The bytes normalization is not implemented for `{self.__class__.__name__}`''')

    
    def normalize_dict(self = None, dict_data = None):
        '''Override for an appropriate dictionary normalization (decoding).'''
        raise NormalizationNotImplemented(f'''The dictionary normalization is not implemented for `{self.__class__.__name__}`''')

    
    def normalize_list(self = None, list_data = None):
        '''Override for an appropriate list normalization (decoding).'''
        raise NormalizationNotImplemented(f'''The list normalization is not implemented for `{self.__class__.__name__}`''')

    
    def populate_self_with_sample_data(self = None):
        '''Allows default object construction as appropriate for a subclass.'''
        raise NormalizationNotImplemented(f'''The default normalization is not implemented for `{self.__class__.__name__}`''')

    
    def get_json(self = None):
        '''Override for an appropriate JSON (python object) representation.'''
        return self.normalized_data

    
    def get_byte_array(self = None):
        '''Override for an appropriate byte array (binary) representation.'''
        return self.normalized_data

    
    def order_check(source = None, template = None):
        """The source may miss items, however that should follow template's order"""
        source_grouped = list(map(itemgetter(0), groupby(source)))
        source_order = list(dict.fromkeys(source).keys())
        if source_order != source_grouped:
            raise ValueError('The source list contains ungrouped duplicates')
        return None == None(None((lambda x = None: x not in source_order), template))

    order_check = None(order_check)


class Int(ABC, GenericParser):
    '''The abstract class for integer TME tag data. Default data representation is Hex.'''
    LENGTH = 2
    
    def BYTE_SIZE(self = None):
        '''The integer type byte size.'''
        pass

    BYTE_SIZE = None(None(BYTE_SIZE))
    
    def normalize_int(self = None, int_data = None):
        return int_data

    
    def normalize_str(self = None, str_data = None):
        return int(str_data, 0, **('base',))

    
    def normalize_bytearray(self = None, bytearray_data = None):
        return int.from_bytes(bytearray_data[self.LENGTH:][:self.BYTE_SIZE], 'little', False, **('byteorder', 'signed'))

    
    def validate_normalized_data(self = None, normalized_data = None):
        super().validate_normalized_data(normalized_data)
    # WARNING: Decompyle incomplete

    
    def populate_self_with_sample_data(self = None):
        '''Generic dummy data generator for any integer type.'''
        return int(reduce(add, map((lambda x: hex(x)[-1]), range(2 * self.BYTE_SIZE))), 16, **('base',))

    
    def get_byte_array(self = None):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None


class IntHex(ABC, Int):
    '''The abstract class for TME tag data representation in hex.'''
    
    def get_json(self = None):
        return f'''0x{super().get_json()