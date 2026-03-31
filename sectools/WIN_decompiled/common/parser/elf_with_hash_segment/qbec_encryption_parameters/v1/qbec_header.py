
from typing import Any
from common.data.data import reverse
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import ENCRYPTED_THEN_SIGNED, ENCRYPTING_ENTITY_DESCRIPTION, QBEC_MAG, QBEC_VERSION_1, QTI
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec_header import QBECHeaderCommon

class QBECHeaderV1(QBECHeaderCommon):
    encryption_order: int = QBEC_VERSION_1
    
    def get_fields(cls = None):
        return super().get_fields() + [
            'total_size',
            'key_management_parameters_size',
            'data_encryption_parameters_size',
            'encrypting_entity']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'magic': QBEC_MAG,
            'version': cls.VERSION,
            'total_size': cls.get_size(),
            'key_management_parameters_size': 0,
            'data_encryption_parameters_size': 0,
            'encrypting_entity': QTI }

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return '<4sIIIII'

    get_format = None(get_format)
    
    def unpack_post_process(self = None):
        self.encryption_order = ENCRYPTED_THEN_SIGNED

    
    def validate_before_operation(self = None, **_):
        self.validate_critical_fields()
        if self.version != self.VERSION:
            raise RuntimeError(f'''{self.class_type_string()} has invalid Version: {self.version}.''')
        if None.total_size != self.get_size() + self.key_management_parameters_size + self.data_encryption_parameters_size:
            raise RuntimeError(f'''{self.class_type_string()} has invalid Size: {self.total_size}.''')
        if None.encrypting_entity not in ENCRYPTING_ENTITY_DESCRIPTION:
            raise RuntimeError(f'''{self.class_type_string()} has invalid Encrypting Entity: {self.encrypting_entity}.''')

    
    def validate(self = None):
        self.validate_critical_fields()

    
    def get_properties(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def class_type_string(cls = None):
        return f'''{super().class_type_string()} v{cls.VERSION}'''

    class_type_string = None(class_type_string)
    __classcell__ = None

