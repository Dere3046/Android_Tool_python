
from typing import List
from common.data.binary_struct import StructBase
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import KeyManagementSchemeIDs

class KeyManagementParametersHeaderCommon(StructBase):
    X_Y_SIZE = 48
    key_management_scheme_id: int = 'QBEC Key Management Parameters'
    
    def get_fields(cls = None):
        return [
            'key_management_scheme_id']

    get_fields = None(get_fields)
    
    def get_format(cls = None):
        return '<I'

    get_format = None(get_format)
    
    def validate_critical_fields(self = None):
        if self.key_management_scheme_id not in KeyManagementSchemeIDs:
            raise RuntimeError(f'''{self.class_type_string()} contain invalid Scheme ID: {self.key_management_scheme_id}.''')

    
    def validate(self = None):
        self.validate_critical_fields()

    
    def class_type_string(cls = None):
        return cls.CLASS_TYPE_STRING

    class_type_string = None(class_type_string)

