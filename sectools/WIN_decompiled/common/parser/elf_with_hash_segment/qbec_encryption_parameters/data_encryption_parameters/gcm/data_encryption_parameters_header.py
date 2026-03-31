
from typing import Any, Dict, List, Tuple
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.data_encryption_parameters.data_encryption_parameters_header_common import DataEncryptionParametersHeaderCommon
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import DATA_ENCRYPTION_SCHEME_ID_ELF_SEGMENT_AES_GCM, DATA_ENCRYPTION_SCHEME_ID_TO_DESCRIPTION

class DataEncryptionParametersHeaderGCM(DataEncryptionParametersHeaderCommon):
    num_iv_auth_tags: int = 'DataEncryptionParametersHeaderGCM'
    
    def get_fields(cls = None):
        return super().get_fields() + [
            'segment_bitmask_size',
            'num_iv_auth_tags']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'data_encryption_scheme_id': DATA_ENCRYPTION_SCHEME_ID_ELF_SEGMENT_AES_GCM,
            'segment_bitmask_size': 0,
            'num_iv_auth_tags': 0 }

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return super().get_format() + 'II'

    get_format = None(get_format)
    
    def class_type_string(cls = None):
        return 'QBEC ELF Segment AES GCM Data Encryption Parameters'

    class_type_string = None(class_type_string)
    
    def validate_critical_fields(self = None):
        super().validate_critical_fields()
        if self.data_encryption_scheme_id != DATA_ENCRYPTION_SCHEME_ID_ELF_SEGMENT_AES_GCM:
            raise RuntimeError(f'''{self.class_type_string()} contain invalid Scheme ID: {self.data_encryption_scheme_id}.''')

    
    def validate_before_operation(self = None, **_):
        if self.segment_bitmask_size or self.segment_bitmask_size % 4:
            raise RuntimeError(f'''{self.class_type_string()} Segment Bitmask Size must be a multiple of 4.''')

    
    def get_properties(self = None):
        return [
            ('Data Encryption Scheme ID:', DATA_ENCRYPTION_SCHEME_ID_TO_DESCRIPTION.get(self.data_encryption_scheme_id, self.data_encryption_scheme_id)),
            ('Segment Bitmask Size:', f'''{self.segment_bitmask_size} (bytes)'''),
            ('Number of IV and Auth Tags:', self.num_iv_auth_tags)]

    __classcell__ = None

