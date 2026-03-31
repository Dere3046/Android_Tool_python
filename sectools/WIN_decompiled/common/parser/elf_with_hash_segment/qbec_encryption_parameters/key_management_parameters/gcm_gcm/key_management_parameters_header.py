
from binascii import hexlify
from typing import Any
from common.data.defines import PAD_BYTE_0
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import KEY_MANAGEMENT_SCHEME_ID_GCM_GCM, KEY_MANAGEMENT_SCHEME_ID_TO_DESCRIPTION
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.key_management_parameters_header_common import KeyManagementParametersHeaderCommon
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.permissive_feature_id_handler import PermissiveFeatureIDHandler

class KeyManagementParametersHeaderGCMGCM(KeyManagementParametersHeaderCommon, PermissiveFeatureIDHandler):
    CLASS_KEY_MANAGEMENT_SCHEME_ID: int = KEY_MANAGEMENT_SCHEME_ID_GCM_GCM
    CLASS_TYPE_STRING = 'QBEC GCM GCM Key Management Parameters'
    num_wrapped_keys: int = 48
    
    def get_fields(cls = None):
        return super().get_fields() + [
            'key_management_feature_id',
            'nonce',
            'num_wrapped_keys']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'key_management_scheme_id': cls.CLASS_KEY_MANAGEMENT_SCHEME_ID,
            'key_management_feature_id': 0,
            'nonce': PAD_BYTE_0 * cls.NONCE_SIZE,
            'num_wrapped_keys': 0 }

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return super().get_format() + f'''I{cls.NONCE_SIZE}sI'''

    get_format = None(get_format)
    
    def validate_critical_fields(self = None):
        super().validate_critical_fields()
        if self.key_management_scheme_id != self.CLASS_KEY_MANAGEMENT_SCHEME_ID:
            raise RuntimeError(f'''{self.class_type_string()} contain invalid Scheme ID: {self.key_management_scheme_id}.''')

    
    def validate_before_operation(self = None, **kwargs):
        if self.nonce and len(self.nonce) != self.NONCE_SIZE:
            raise RuntimeError(f'''{self.class_type_string()} contain Nonce of invalid length: {len(self.nonce)}.''')
        None.validate_key_management_feature_id()

    
    def get_properties(self = None):
        return [
            ('Key Management Scheme ID:', KEY_MANAGEMENT_SCHEME_ID_TO_DESCRIPTION.get(self.key_management_scheme_id, self.key_management_scheme_id)),
            ('Key Management Feature ID:', self.get_properties_key_management_feature_id()),
            ('Nonce:', f'''0x{hexlify(self.nonce).decode()}'''),
            ('Number of Wrapped Keys:', self.num_wrapped_keys)]

    __classcell__ = None

