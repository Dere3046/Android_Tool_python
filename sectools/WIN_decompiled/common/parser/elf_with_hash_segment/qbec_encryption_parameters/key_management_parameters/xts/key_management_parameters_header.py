
from binascii import hexlify
from typing import Any, Dict, List, Tuple, Union
from common.data.defines import PAD_BYTE_0
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import KEY_MANAGEMENT_SCHEME_ID_ECDH_P384_HKDF_SIV_XTS, KEY_MANAGEMENT_SCHEME_ID_TO_DESCRIPTION, XTS_ENCRYPTION_LABEL
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.key_management_parameters_header_common import KeyManagementParametersHeaderCommon

class KeyManagementParametersHeaderXTS(KeyManagementParametersHeaderCommon):
    LABEL_SIZE = 64
    NONCE_SIZE = 64
    CLASS_TYPE_STRING = 'QBEC ECDH P384 HKDF SIV XTS Key Management Parameters'
    num_wrapped_keys: int = KEY_MANAGEMENT_SCHEME_ID_ECDH_P384_HKDF_SIV_XTS
    
    def get_fields(cls = None):
        fields = super().get_fields() + [
            'label',
            'nonce',
            'public_key_x',
            'public_key_y',
            'num_wrapped_keys']
        return fields

    get_fields = None(get_fields)
    
    def get_field_defaults(cls = None):
        return {
            'key_management_scheme_id': cls.CLASS_KEY_MANAGEMENT_SCHEME_ID,
            'label': XTS_ENCRYPTION_LABEL,
            'nonce': PAD_BYTE_0 * cls.NONCE_SIZE,
            'public_key_x': PAD_BYTE_0 * cls.X_Y_SIZE,
            'public_key_y': PAD_BYTE_0 * cls.X_Y_SIZE,
            'num_wrapped_keys': 0 }

    get_field_defaults = None(get_field_defaults)
    
    def get_format(cls = None):
        return super().get_format() + f'''{cls.LABEL_SIZE}s{cls.NONCE_SIZE}s{cls.X_Y_SIZE}s{cls.X_Y_SIZE}sI'''

    get_format = None(get_format)
    
    def validate_critical_fields(self = None):
        super().validate_critical_fields()
        if not self.label.decode().startswith(XTS_ENCRYPTION_LABEL.decode()):
            raise RuntimeError(f'''{self.class_type_string()} contain invalid Label: {self.label.decode()}.''')
        if None.key_management_scheme_id != self.CLASS_KEY_MANAGEMENT_SCHEME_ID:
            raise RuntimeError(f'''{self.class_type_string()} contain invalid Scheme ID: {self.key_management_scheme_id}.''')

    
    def validate_before_operation(self = None, **_):
        if self.nonce and len(self.nonce) > self.NONCE_SIZE:
            raise RuntimeError(f'''{self.class_type_string()} contain Nonce of invalid length: {len(self.nonce)}.''')
        if None.public_key_x and len(self.public_key_x) != self.X_Y_SIZE:
            raise RuntimeError(f'''{self.class_type_string()} contain Public Key X of invalid length: {len(self.public_key_x)}.''')
        if None.public_key_y or len(self.public_key_y) != self.X_Y_SIZE:
            raise RuntimeError(f'''{{self.class_type_string()}} contain Public Key Y of invalid length: {len(self.public_key_y)}.''')
        return None

    
    def get_properties(self = None):
        return [
            ('Key Management Scheme ID:', KEY_MANAGEMENT_SCHEME_ID_TO_DESCRIPTION.get(self.key_management_scheme_id, self.key_management_scheme_id)),
            ('Label:', f'''{self.label.decode()[:len(XTS_ENCRYPTION_LABEL)]}'''),
            ('Nonce:', f'''0x{hexlify(self.nonce).decode()}'''),
            ('Public Key X:', f'''0x{hexlify(self.public_key_x).decode()}'''),
            ('Public Key Y:', f'''0x{hexlify(self.public_key_y).decode()}'''),
            ('Number of Wrapped Keys:', self.num_wrapped_keys)]

    __classcell__ = None

