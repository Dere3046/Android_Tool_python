
from typing import Any
from common.data.data import hex_val
from common.parser.elf_with_hash_segment.hash_table_segment_header import HashTableSegmentHeaderCommon
from common.parser.elf_with_hash_segment.hash_table_segment_header_getters_interface import HashTableSegmentHeaderGettersInterface
from common.parser.elf_with_hash_segment.hash_table_segment_header_signed_interface import HashTableSegmentHeaderSignedInterface
from common.parser.elf_with_hash_segment.v3.binding_implementation_ou_fields import BindingImplementationOUFields
from common.parser.hash_segment.defines import HASH_SEGMENT_V3

class HashTableSegmentHeaderV3Spec(HashTableSegmentHeaderSignedInterface, HashTableSegmentHeaderCommon):
    VERSION = HASH_SEGMENT_V3
    oem_certificate_chain_size: int = '_hash_table_size'
    
    def get_fields(cls = None):
        return [
            'boot_image_id',
            'version',
            'reserved',
            '_image_dest_ptr',
            'image_size',
            cls.FIELD_6,
            '_oem_signature_ptr',
            '_oem_signature_size',
            '_oem_certificate_chain_ptr',
            'oem_certificate_chain_size']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'oem_certificate_chain_size': 0,
            '_oem_certificate_chain_ptr': 0,
            '_oem_signature_size': 0,
            '_oem_signature_ptr': 0,
            cls.FIELD_6: 0,
            'image_size': 0,
            '_image_dest_ptr': 0,
            'reserved': 0,
            'version': HASH_SEGMENT_V3,
            'boot_image_id': 0 }

    get_field_defaults = None(get_field_defaults)
    
    def hash_table_size(self = None):
        return self._hash_table_size

    hash_table_size = None(hash_table_size)
    
    def hash_table_size(self = None, size = None):
        self._hash_table_size = size
        self.update_oem_signature_ptr()
        self.update_oem_certificate_chain_ptr()

    hash_table_size = None(hash_table_size)
    
    def image_dest_ptr(self = None):
        return self._image_dest_ptr

    image_dest_ptr = None(image_dest_ptr)
    
    def image_dest_ptr(self = None, ptr = None):
        self._image_dest_ptr = ptr
        self.update_oem_signature_ptr()
        self.update_oem_certificate_chain_ptr()

    image_dest_ptr = None(image_dest_ptr)
    
    def oem_signature_size(self = None):
        return self._oem_signature_size

    oem_signature_size = None(oem_signature_size)
    
    def oem_signature_size(self = None, size = None):
        self._oem_signature_size = size
        self.update_oem_certificate_chain_ptr()

    oem_signature_size = None(oem_signature_size)
    
    def oem_signature_ptr(self = None):
        return self._oem_signature_ptr

    oem_signature_ptr = None(oem_signature_ptr)
    
    def oem_certificate_chain_ptr(self = None):
        return self._oem_certificate_chain_ptr

    oem_certificate_chain_ptr = None(oem_certificate_chain_ptr)
    
    def update_oem_signature_ptr(self = None):
        self._oem_signature_ptr = self._image_dest_ptr + getattr(self, self.FIELD_6, 0)

    
    def update_oem_certificate_chain_ptr(self = None):
        self._oem_certificate_chain_ptr = self._image_dest_ptr + getattr(self, self.FIELD_6, 0) + self._oem_signature_size

    
    def get_format(cls = None):
        return super().get_format() + 'IIIIIIII'

    get_format = None(get_format)
    
    def validate_critical_fields(self = None):
        if self.version != self.VERSION:
            raise RuntimeError(f'''{self.HEADER_STR} has invalid version: {self.version}.''')

    
    def validate(self = None):
        self.validate_critical_fields()

    
    def get_properties(self, _ = None, __ = None, oem_signature = None, oem_certificate_chain = ('oem_signature', memoryview, 'oem_certificate_chain', memoryview, 'return', list[tuple[(str, Any)]])):
        oem_sig_size_str = HashTableSegmentHeaderCommon.format_size_string('OEM Signature Size', self.oem_signature_size, oem_signature)
        oem_certificate_chain_str = HashTableSegmentHeaderCommon.format_size_string('OEM Certificate Chain Size', self.oem_certificate_chain_size, oem_certificate_chain)
        return [
            ('Boot Image ID:', hex_val(self.boot_image_id, True, **('strip_leading_zeros',))),
            ('Version:', self.version),
            ('Image Destination Pointer:', hex_val(self.image_dest_ptr)),
            ('Image Size:', f'''{self.image_size}{self.IMAGE_SIZE_STR}'''),
            (self.FIELD_6_STR, f'''{getattr(self, self.FIELD_6)} (bytes)'''),
            ('OEM Signature Pointer:', hex_val(self.oem_signature_ptr)),
            (oem_sig_size_str, f'''{self.oem_signature_size} (bytes)'''),
            ('OEM Certificate Chain Pointer:', hex_val(self.oem_certificate_chain_ptr)),
            (oem_certificate_chain_str, f'''{self.oem_certificate_chain_size} (bytes)''')]

    
    def is_unsigned(self = None):
        return bool(not (self.oem_signature_size))

    
    def is_oem_exclusive_signed(self = None, _ = None):
        return bool(self.oem_signature_size)

    
    def is_qti_exclusive_signed(self = None, _ = None):
        return False

    
    def is_oem_signed_double_signable(self = None, _ = None):
        return False

    
    def is_qti_signed_double_signable(self = None, _ = None):
        return False

    
    def is_double_signed(self = None):
        return False

    __classcell__ = None


class HashTableSegmentHeaderV3(HashTableSegmentHeaderGettersInterface, BindingImplementationOUFields, HashTableSegmentHeaderV3Spec):
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = (None, False, False)):
        BindingImplementationOUFields.__init__(self)
        HashTableSegmentHeaderV3Spec.__init__(self, data, check_is_type, bypass_validation)


