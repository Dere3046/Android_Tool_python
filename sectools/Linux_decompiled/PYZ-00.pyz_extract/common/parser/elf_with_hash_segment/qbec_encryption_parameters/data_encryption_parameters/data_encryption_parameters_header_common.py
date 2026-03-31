
from typing import List
from common.data.binary_struct import StructBase
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import DATA_ENCRYPTION_SCHEME_IDS

class DataEncryptionParametersHeaderCommon(StructBase):
    data_encryption_scheme_id: int = 'DataEncryptionParametersHeaderCommon'
    
    def get_fields(cls = None):
        return [
            'data_encryption_scheme_id']

    get_fields = None(get_fields)
    
    def get_format(cls = None):
        return '<I'

    get_format = None(get_format)
    
    def validate_critical_fields(self = None):
        if self.data_encryption_scheme_id not in DATA_ENCRYPTION_SCHEME_IDS:
            raise RuntimeError(f'''QBEC Data Encryption Parameters contain invalid Scheme ID: {self.data_encryption_scheme_id}.''')

    
    def validate(self = None):
        self.validate_critical_fields()


