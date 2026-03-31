
from typing import List
from common.data.binary_struct import StructBase
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import QBEC_MAG, QBEC_VERSIONS

class QBECHeaderCommon(StructBase):
    version: int = 'QBECHeaderCommon'
    
    def get_fields(cls = None):
        return [
            'magic',
            'version']

    get_fields = None(get_fields)
    
    def get_format(cls = None):
        return '<4sI'

    get_format = None(get_format)
    
    def validate_critical_fields(self = None):
        if self.magic != QBEC_MAG:
            raise RuntimeError(f'''{self.class_type_string()} has invalid Magic: {self.magic.decode()}.''')
        if None.version not in QBEC_VERSIONS:
            raise RuntimeError(f'''{self.class_type_string()} has invalid version: {self.version}.''')

    
    def class_type_string(cls = None):
        return 'QBEC Encryption Parameters Header'

    class_type_string = None(class_type_string)

