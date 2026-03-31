
from abc import abstractmethod
from binascii import hexlify, unhexlify
from typing import Any, Type
from Cryptodome.Cipher import AES
from Cryptodome.Cipher._mode_siv import SivMode
from common.data.base_parser import BaseParser, DumpDict
from common.data.data import properties_repr, split_long_row
from common.data.defines import PAD_BYTE_0
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.defines import KeyManagementParametersHeader

class KeyManagementParametersCommon(BaseParser):
    HEADER_CLASS: Type[KeyManagementParametersHeader] | None = None
    WRAPPED_KEY_SIZE: int = 100
    
    def __init__(self = None, data = None, **_):
        self.header = None
        self.wrapped_keys = []
        super().__init__(data, **('data',))

    
    def unpack(self = None, data = None):
        data = memoryview(data)
    # WARNING: Decompyle incomplete

    
    def _unpack_wrapped_keys(self = None, data = None):
        offset = 0
        for _ in range(self.header.num_wrapped_keys):
            self.wrapped_keys.append(bytes(data[offset:offset + self.WRAPPED_KEY_SIZE]))
            offset += self.WRAPPED_KEY_SIZE

    
    def pack(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def _pack_wrapped_keys(self = None):
        data = bytearray()
        for wrapped_key in self.wrapped_keys:
            data += bytearray(wrapped_key).rjust(self.WRAPPED_KEY_SIZE, PAD_BYTE_0)
        return memoryview(data)

    
    def is_type(cls = None, data = None):
        pass
    # WARNING: Decompyle incomplete

    is_type = None(is_type)
    
    def validate(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def validate_before_operation(self = None, **_):
        pass
    # WARNING: Decompyle incomplete

    
    def get_size(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_variable_size(cls = None, num_keys = None):
        return num_keys * cls.WRAPPED_KEY_SIZE

    get_variable_size = None(get_variable_size)
    
    def get_dump_files(self = None, directory = None):
        pass
    # WARNING: Decompyle incomplete

    
    def __repr__(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def _get_wrapped_key_properties(self = None):
        properties = []
        for idx, wrapped_key in enumerate(self.wrapped_keys):
            properties += split_long_row((f'''Wrapped Key {idx}:''',) + (f'''0x{hexlify(wrapped_key).decode()}''',), 101)
        return properties

    
    def check_is_valid_key_length(cls = None, key_length = classmethod):
        pass

    check_is_valid_key_length = None(None(check_is_valid_key_length))
    
    def get_encryption_spec_size(cls = None, num_keys = None):
        pass
    # WARNING: Decompyle incomplete

    get_encryption_spec_size = None(get_encryption_spec_size)
    
    def get_key_policy(cls = None, feature_id = classmethod):
        pass

    get_key_policy = None(None(get_key_policy))
    
    def pad_ciphertext(ciphertext = None):
        return ciphertext.ljust(68, PAD_BYTE_0)

    pad_ciphertext = None(pad_ciphertext)
    
    def wrap_data_encryption_key(cls = None, hkdf_key = None, data_encryption_key = classmethod, policy = (None,)):
        sks_policy = unhexlify(policy) if policy else b''
        cipher = AES.new(hkdf_key, AES.MODE_SIV)
    # WARNING: Decompyle incomplete

    wrap_data_encryption_key = None(wrap_data_encryption_key)
    
    def process_data_encryption_key(cls = None, data_encryption_key = None):
        return data_encryption_key

    process_data_encryption_key = None(process_data_encryption_key)
    __classcell__ = None

