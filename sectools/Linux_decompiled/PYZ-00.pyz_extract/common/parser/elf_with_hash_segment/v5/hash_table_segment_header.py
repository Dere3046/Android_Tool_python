
from typing import Any
from common.parser.elf_with_hash_segment.hash_table_segment_header import HashTableSegmentHeaderCommon
from common.parser.elf_with_hash_segment.hash_table_segment_header_getters_interface import HashTableSegmentHeaderGettersInterface
from common.parser.elf_with_hash_segment.hash_table_segment_header_signed_interface import HashTableSegmentHeaderSignedInterface
from common.parser.elf_with_hash_segment.v3.binding_implementation_ou_fields import BindingImplementationOUFields
from common.parser.hash_segment.defines import HASH_SEGMENT_V5

class HashTableSegmentHeaderV5Spec(HashTableSegmentHeaderSignedInterface, HashTableSegmentHeaderCommon):
    oem_certificate_chain_size: int = HASH_SEGMENT_V5
    
    def get_fields(cls = None):
        return super().get_fields() + [
            'qti_signature_size',
            'qti_certificate_chain_size',
            'image_size',
            cls.FIELD_6,
            'reserved4',
            'oem_signature_size',
            'reserved5',
            'oem_certificate_chain_size']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'oem_certificate_chain_size': 0,
            'reserved5': 0,
            'oem_signature_size': 0,
            'reserved4': 0,
            cls.FIELD_6: 0,
            'image_size': 0,
            'qti_certificate_chain_size': 0,
            'qti_signature_size': 0,
            'version': HASH_SEGMENT_V5,
            'reserved': 0 }

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return super().get_format() + 'IIIIIIII'

    get_format = None(get_format)
    
    def validate_critical_fields(self = None):
        if self.version != self.VERSION:
            raise RuntimeError(f'''{self.HEADER_STR} has invalid version: {self.version}.''')

    
    def validate(self = None):
        self.validate_critical_fields()

    
    def get_properties(self, qti_signature = None, qti_certificate_chain = None, oem_signature = None, oem_certificate_chain = ('qti_signature', memoryview, 'qti_certificate_chain', memoryview, 'oem_signature', memoryview, 'oem_certificate_chain', memoryview, 'return', list[tuple[(str, Any)]])):
        qti_sig_size_str = HashTableSegmentHeaderCommon.format_size_string('QTI Signature Size', self.qti_signature_size, qti_signature)
        qti_certificate_chain_str = HashTableSegmentHeaderCommon.format_size_string('QTI Certificate Chain Size', self.qti_certificate_chain_size, qti_certificate_chain)
        oem_sig_size_str = HashTableSegmentHeaderCommon.format_size_string('OEM Signature Size', self.oem_signature_size, oem_signature)
        oem_certificate_chain_str = HashTableSegmentHeaderCommon.format_size_string('OEM Certificate Chain Size', self.oem_certificate_chain_size, oem_certificate_chain)
        return [
            ('Version:', self.version),
            (qti_sig_size_str, f'''{self.qti_signature_size} (bytes)'''),
            (qti_certificate_chain_str, f'''{self.qti_certificate_chain_size} (bytes)'''),
            ('Image Size:', f'''{self.image_size}{self.IMAGE_SIZE_STR}'''),
            (self.FIELD_6_STR, f'''{getattr(self, self.FIELD_6)} (bytes)'''),
            (oem_sig_size_str, f'''{self.oem_signature_size} (bytes)'''),
            (oem_certificate_chain_str, f'''{self.oem_certificate_chain_size} (bytes)''')]

    
    def is_unsigned(self = None):
        if not (self.oem_signature_size):
            pass
        return bool(not (self.qti_signature_size))

    
    def is_oem_exclusive_signed(self = None, contains_padding = None):
        if self.oem_signature_size:
            pass
        if bool(not (self.qti_signature_size)):
            pass
        return not contains_padding

    
    def is_qti_exclusive_signed(self = None, contains_padding = None):
        if self.qti_signature_size:
            pass
        if bool(not (self.oem_signature_size)):
            pass
        return not contains_padding

    
    def is_oem_signed_double_signable(self = None, contains_padding = None):
        if self.oem_signature_size:
            pass
        if bool(not (self.qti_signature_size)):
            pass
        return contains_padding

    
    def is_qti_signed_double_signable(self = None, contains_padding = None):
        if self.qti_signature_size:
            pass
        if bool(not (self.oem_signature_size)):
            pass
        return contains_padding

    
    def is_double_signed(self = None):
        if self.oem_signature_size:
            pass
        return bool(self.qti_signature_size)

    __classcell__ = None


class HashTableSegmentHeaderV5(HashTableSegmentHeaderGettersInterface, BindingImplementationOUFields, HashTableSegmentHeaderV5Spec):
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = (None, False, False)):
        BindingImplementationOUFields.__init__(self)
        HashTableSegmentHeaderV5Spec.__init__(self, data, check_is_type, bypass_validation)


