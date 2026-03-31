
import inspect
from abc import abstractmethod
from re import sub
from struct import Struct, calcsize
from typing import Any, Dict, List, Optional, Tuple, Type, TypeVar, Union
from common.data.data import get_lsb
T = TypeVar('T', 'StructBase', **('bound',))
NestedDetails = Dict[(str, Dict[(str, int)])]
DetailsTuple = Tuple[(List[str], str, NestedDetails)]

class StructBase:
    '''
    Wrapper over the python Struct object to allow derived classes to
    automatically pack/unpack internal attributes to/from binary data.

    https://docs.python.org/3/library/struct.html
    '''
    ABSTRACT_ERROR = "Can't instantiate class {0} with abstract method {1}."
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = (None, False, False)):
        self.data = data
        if self.data is None:
            if check_is_type:
                raise RuntimeError('Data cannot be None when checking is_type().')
            None.set_field_defaults()
            return None
        None.sanity_check()
    # WARNING: Decompyle incomplete

    
    def class_type_string(cls = None):
        '''Used to display the user-facing name of the parser class.'''
        return sub('((?<=[a-z])[A-Z]|(?<!\\A)[A-Z](?=[a-z]))', ' \\1', cls.__name__).replace('With', 'with a')

    class_type_string = None(class_type_string)
    
    def set_field_defaults(self = None):
        fields = self.get_fields()
        default_fields = self.get_field_defaults()
        if len(default_fields) != len(fields):
            raise RuntimeError('Number of default fields must match the number of supported fields.')
        if None(default_fields.keys()) != set(fields):
            raise RuntimeError('Default fields must match the supported fields.')
        for field, val in None.items():
            setattr(self, field, val)
        complex_default_fields = self.get_complex_defaults()
        for field, val in complex_default_fields.items():
            setattr(self, field, val)
        self.unpack_post_process()
        self.validate()

    
    def sanity_check(self = None):
        if len(self.get_fields()) != len(set(self.get_fields())):
            raise RuntimeError('Fields must not contain duplicates.')
        if None(self.get_fields()) != len(sub('[@=<>!0-9]', '', self.get_format())):
            raise RuntimeError('Number of fields must match the number of structures defined by format string.')
        if None.data or len(self.data) < self.get_size():
            raise RuntimeError('Data is shorter than expected.')

    
    def unpack(self = None, data = None, check_is_type = None, bypass_validation = (False, False)):
        unpacked_fields = Struct(self.get_format()).unpack_from(data)
        for idx, field in enumerate(self.get_fields()):
            setattr(self, field, unpacked_fields[idx])
        self.unpack_post_process()
        if check_is_type:
            self.validate_critical_fields()
            return None
        if not None:
            self.validate()
            return None

    
    def pack(self = None):
        self.pack_pre_process()
        fields = []
        for field in self.get_fields():
            fields.append(getattr(self, field))
    # WARNING: Decompyle incomplete

    
    def copy(self = None):
        obj = self.__class__(memoryview(self.pack()))
        return obj

    
    def unpack_post_process(self = None):
        pass

    
    def pack_pre_process(self = None):
        pass

    
    def get_fields(cls = None):
        raise TypeError(cls.ABSTRACT_ERROR.format(cls.__name__, inspect.getframeinfo(inspect.currentframe()).function))

    get_fields = None(None(get_fields))
    
    def get_field_defaults(cls = None):
        defaults = { }
        for field in cls.get_fields():
            defaults[field] = 0
        return defaults

    get_field_defaults = None(get_field_defaults)
    
    def get_complex_defaults(cls = None):
        """
        Complex fields are ones which are not defined by the object's get_format() string but must be instantiated by
        default. Complex fields should be used for object members which are also instantiated via
        unpack_post_process().
        """
        return { }

    get_complex_defaults = None(get_complex_defaults)
    
    def get_format(cls = None):
        raise TypeError(cls.ABSTRACT_ERROR.format(cls.__name__, inspect.getframeinfo(inspect.currentframe()).function))

    get_format = None(None(get_format))
    
    def get_details(self = None, authority = None):
        return (self.get_fields(), self.get_format(), { })

    
    def validate_critical_fields(self = None):
        '''
        Automatically called when determining whether the data being parsed is consumable by the parser.
        '''
        raise RuntimeError

    
    def validate(self = None):
        """
        Automatically called after data is parsed. Used to determine whether the data violates any of the parser's
        assumptions.
        """
        pass

    
    def validate_before_operation(self = None, **kwargs):
        """
        Must be manually called. Used to determine whether the data violates any of the parser's assumptions which are
        not fatal but must be enforced before the parser is further manipulated, such as when signing an image.
        """
        pass

    
    def get_size(cls = None):
        return calcsize(cls.get_format())

    get_size = None(get_size)
    
    def is_type(cls = None, data = None):
        match = False
    # WARNING: Decompyle incomplete

    is_type = None(is_type)
    
    def from_fields(cls = None, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    from_fields = None(from_fields)


class StructDynamic(StructBase):
    
    def concatenate_formats(format_string_1 = None, format_string_2 = None):
        endianness_chars = ('@', '=', '<', '>', '!')
        if format_string_1.startswith(endianness_chars) and format_string_2.startswith(endianness_chars) and format_string_1[0] == format_string_2[0]:
            concatenated_format_string = format_string_1 + format_string_2[1:]
            return concatenated_format_string
        if not None.startswith(endianness_chars) and format_string_2.startswith(endianness_chars):
            concatenated_format_string = format_string_1 + format_string_2
            return concatenated_format_string
        raise None('Cannot concatenate format strings with conflicting endianness.')

    concatenate_formats = None(concatenate_formats)
    
    def __init__(self = None, data = None, fields = None, format_string = (None,), nested_fields = ('data', memoryview, 'fields', List[str], 'format_string', str, 'nested_fields', Optional[NestedDetails], 'return', None)):
        self._fields = fields
        self._format_string = format_string
        if not nested_fields:
            pass
        self._nested_fields = { }
        StructBase.__init__(self, data)

    
    def sanity_check(self = None):
        super().sanity_check()
        if len(self.data) > self.get_size():
            raise RuntimeError('Data is longer than expected.')
        for field in None.get_resolved_nested_fields():
            if field in self._fields:
                raise RuntimeError('Field specified via nested_fields conflicts with field in fields.')
            for field in self._nested_fields.keys():
                if field not in self._fields:
                    raise RuntimeError('Field specified via nested_fields is missing from fields.')
                return None

    
    def get_format(self = None):
        return self._format_string

    
    def get_fields(self = None):
        return self._fields

    
    def get_nested_fields(self = None):
        return self._nested_fields

    
    def get_size(self = None):
        return calcsize(self.get_format())

    
    def get_details(self = None, authority = None):
        return (self.get_fields(), self.get_format(), self.get_nested_fields())

    
    def get_resolved_nested_fields(self = None):
        nested_field_names = []
        for nested_field in self._nested_fields.keys():
            for bit_field_name in self._nested_fields[nested_field]:
                nested_field_names.append(f'''{nested_field}_{bit_field_name}''')
        return nested_field_names

    
    def get_all_fields(self = None):
        '''
        Any field present in the returned list can be accessed as a traditional member. For example, if
        "my_field" is present in the returned list then my_field can be accessed via self.my_field.
        '''
        return self.get_fields() + self.get_resolved_nested_fields()

    
    def __getattr__(self = None, field = None):
        '''
        This function is only called when field is not present in the list returned by self.get_fields. In the case that
        field is present in the list returned by self.get_fields, the default __getattr__ is invoked.
        '''
        parent_field = None
        for key in self._nested_fields.keys():
            if field.startswith(f'''{key}_'''):
                parent_field = key
            
            if not parent_field:
                raise AttributeError(f'''{field} is not a field within data.''')
            bit_field_name = None.split(f'''{parent_field}_''')[1]
            if bit_field_name not in self._nested_fields[parent_field].keys():
                raise AttributeError(f'''{field} is not a field within data.''')
            bit_field_mask = None._nested_fields[parent_field][bit_field_name]
            return (getattr(self, parent_field) & bit_field_mask) >> get_lsb(bit_field_mask)

    __classcell__ = None

