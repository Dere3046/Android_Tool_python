
from binascii import hexlify
from typing import Any
from common.data.data import hex_val
from common.data.defines import PAD_BYTE_0
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import KEY_MANAGEMENT_FEATURE_IDS, KEY_MANAGEMENT_FEATURE_ID_MODEM_IMAGE, KEY_MANAGEMENT_FEATURE_ID_TO_DESCRIPTION, KEY_MANAGEMENT_SCHEME_ID_ECDH_P384_HKDF_SIV_GCM, KEY_MANAGEMENT_SCHEME_ID_TO_DESCRIPTION
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.key_management_parameters_header_common import KeyManagementParametersHeaderCommon

class KeyManagementParametersHeaderGCM(KeyManagementParametersHeaderCommon):
    CLASS_KEY_MANAGEMENT_SCHEME_ID: int = KEY_MANAGEMENT_SCHEME_ID_ECDH_P384_HKDF_SIV_GCM
    num_wrapped_keys: int = 'QBEC ECDH P384 HKDF SIV GCM Key Management Parameters'
    
    def get_fields(cls = None):
        return super().get_fields() + [
            'key_management_feature_id',
            'public_key_x',
            'public_key_y',
            'num_wrapped_keys']

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'key_management_scheme_id': cls.CLASS_KEY_MANAGEMENT_SCHEME_ID,
            'key_management_feature_id': KEY_MANAGEMENT_FEATURE_ID_MODEM_IMAGE,
            'public_key_x': PAD_BYTE_0 * cls.X_Y_SIZE,
            'public_key_y': PAD_BYTE_0 * cls.X_Y_SIZE,
            'num_wrapped_keys': 0 }

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return super().get_format() + f'''I{cls.X_Y_SIZE}s{cls.X_Y_SIZE}sI'''

    get_format = None(get_format)
    
    def validate_critical_fields(self = None):
        super().validate_critical_fields()
        if self.key_management_scheme_id != self.CLASS_KEY_MANAGEMENT_SCHEME_ID:
            raise RuntimeError(f'''{self.class_type_string()} contain invalid Scheme ID: {self.key_management_scheme_id}.''')
        None.validate_key_management_feature_id()

    
    def validate_before_operation(self = None, **kwargs):
        if self.public_key_x and len(self.public_key_x) != self.X_Y_SIZE:
            raise RuntimeError(f'''{self.class_type_string()} contain Public Key X of invalid length: {len(self.public_key_x)}.''')
        if None.public_key_y or len(self.public_key_y) != self.X_Y_SIZE:
            raise RuntimeError(f'''{self.class_type_string()} contain Public Key Y of invalid length: {len(self.public_key_y)}.''')
        return None

    
    def get_properties_key_management_feature_id(self = None):
        return KEY_MANAGEMENT_FEATURE_ID_TO_DESCRIPTION.get(self.key_management_feature_id, hex_val(self.key_management_feature_id, True, **('strip_leading_zeros',)))

    
    def get_properties(self = None):
        return [
            ('Key Management Scheme ID:', KEY_MANAGEMENT_SCHEME_ID_TO_DESCRIPTION.get(self.key_management_scheme_id, self.key_management_scheme_id)),
            ('Key Management Feature ID:', self.get_properties_key_management_feature_id()),
            ('Public Key X:', f'''0x{hexlify(self.public_key_x).decode()}'''),
            ('Public Key Y:', f'''0x{hexlify(self.public_key_y).decode()}'''),
            ('Number of Wrapped Keys:', self.num_wrapped_keys)]

    
    def validate_key_management_feature_id(self = None):
        if self.key_management_feature_id not in KEY_MANAGEMENT_FEATURE_IDS:
            raise RuntimeError(f'''{self.class_type_string()} contain invalid Feature ID: {hex_val(self.key_management_feature_id, True, **('strip_leading_zeros',))}.''')

    __classcell__ = None

