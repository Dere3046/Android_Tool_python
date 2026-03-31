
from typing import Any
from colorama import Fore
from common.data.data import color_string
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import ENCRYPTED_THEN_SIGNED, ENCRYPTION_ORDER_DESCRIPTION, QBEC_VERSION_2
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.v1.qbec_header import QBECHeaderV1

class QBECHeaderV2(QBECHeaderV1):
    VERSION = QBEC_VERSION_2
    
    def get_fields(cls = None):
        return super().get_fields() + [
            'encryption_order']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        pass
    # WARNING: Decompyle incomplete

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return super().get_format() + 'I'

    get_format = None(get_format)
    
    def unpack_post_process(self = None):
        pass

    
    def validate_before_operation(self = None, **_):
        super().validate_before_operation()
        if self.encryption_order not in ENCRYPTION_ORDER_DESCRIPTION:
            raise RuntimeError(f'''{self.class_type_string()} has invalid Encryption Order: {self.encryption_order}.''')

    
    def get_properties(self = None):
        if self.encryption_order in ENCRYPTION_ORDER_DESCRIPTION:
            printed_encryption_order = f'''{ENCRYPTION_ORDER_DESCRIPTION[self.encryption_order]} (if signed)'''
        else:
            printed_encryption_order = color_string(str(self.encryption_order), Fore.YELLOW)
        return super().get_properties() + [
            ('Encryption Order:', printed_encryption_order)]

    __classcell__ = None

