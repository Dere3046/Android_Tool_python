
from binascii import hexlify
from typing import Any, Dict, List, Tuple
from common.data.defines import PAD_BYTE_0
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.data_encryption_parameters.data_encryption_parameters_header_common import DataEncryptionParametersHeaderCommon
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import DATA_ENCRYPTION_SCHEME_ID_AES_128_XTS, DATA_ENCRYPTION_SCHEME_ID_TO_DESCRIPTION

class DataEncryptionParametersHeaderXTS(DataEncryptionParametersHeaderCommon):
    seed: bytes = 16
    
    def get_fields(cls = None):
        return super().get_fields() + [
            'seed']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'data_encryption_scheme_id': DATA_ENCRYPTION_SCHEME_ID_AES_128_XTS,
            'seed': PAD_BYTE_0 * cls.SEED_SIZE }

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return super().get_format() + f'''{cls.SEED_SIZE}s'''

    get_format = None(get_format)
    
    def validate_critical_fields(self = None):
        super().validate_critical_fields()
        if self.data_encryption_scheme_id != DATA_ENCRYPTION_SCHEME_ID_AES_128_XTS:
            raise RuntimeError(f'''{self.class_type_string()} contain invalid Scheme ID: {self.data_encryption_scheme_id}.''')

    
    def validate_before_operation(self = None, **kwargs):
        if self.seed or len(self.seed) != self.SEED_SIZE:
            raise RuntimeError(f'''{self.class_type_string()} contain Seed of invalid length: {len(self.seed)}.''')
        return None

    
    def get_properties(self = None):
        return [
            ('Data Encryption Scheme ID:', DATA_ENCRYPTION_SCHEME_ID_TO_DESCRIPTION.get(self.data_encryption_scheme_id, self.data_encryption_scheme_id)),
            ('Seed:', f'''0x{hexlify(self.seed).decode()}''')]

    
    def class_type_string(cls = None):
        return 'QBEC AES 128 XTS Encryption Parameters'

    class_type_string = None(class_type_string)
    __classcell__ = None

