
from typing import Type
from common.data.base_parser import BaseParserGenerator
from common.data.data import hex_val
from common.data.defines import PAD_BYTE_0
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import KEY_MANAGEMENT_FEATURE_ID_MODEM_IMAGE, KEY_MANAGEMENT_FEATURE_ID_MODEM_IMAGE_KPV4, KEY_MANAGEMENT_FEATURE_ID_TENX_IMAGE, KEY_MANAGEMENT_FEATURE_ID_TO_DESCRIPTION, KEY_MANAGEMENT_SCHEME_ID_TO_DESCRIPTION
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.gcm.key_management_parameters_header import KeyManagementParametersHeaderGCM
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.key_management_parameters_common import KeyManagementParametersCommon

class KeyManagementParametersGCM(KeyManagementParametersCommon, BaseParserGenerator):
    HEADER_CLASS: Type[KeyManagementParametersHeaderGCM] = KeyManagementParametersHeaderGCM
    FEATURE_ID_TO_POLICY: dict[(int, str)] = {
        KEY_MANAGEMENT_FEATURE_ID_MODEM_IMAGE_KPV4: '201C16100A421000',
        KEY_MANAGEMENT_FEATURE_ID_TENX_IMAGE: '201C16120A301000',
        KEY_MANAGEMENT_FEATURE_ID_MODEM_IMAGE: '201C16120A301000' }
    
    def create_default(self = None, key_management_feature_id = None, public_key_x = None, public_key_y = (KEY_MANAGEMENT_FEATURE_ID_MODEM_IMAGE, b'', b'', (b'',)), wrapped_keys = ('key_management_feature_id', int, 'public_key_x', bytes, 'public_key_y', bytes, 'wrapped_keys', tuple[(bytes, ...)], 'return', None), **_):
        self.header = self.HEADER_CLASS.from_fields(key_management_feature_id, public_key_x.rjust(self.HEADER_CLASS.X_Y_SIZE, PAD_BYTE_0), public_key_y.rjust(self.HEADER_CLASS.X_Y_SIZE, PAD_BYTE_0), len(wrapped_keys), **('key_management_feature_id', 'public_key_x', 'public_key_y', 'num_wrapped_keys'))
        self.wrapped_keys = list(wrapped_keys)

    
    def check_is_valid_key_length(cls = None, key_length = None):
        return key_length == cls.WRAPPED_KEY_SIZE

    check_is_valid_key_length = None(check_is_valid_key_length)
    
    def get_key_policy(cls = None, feature_id = None):
        if policy = cls.FEATURE_ID_TO_POLICY.get(feature_id) is None:
            feature_id_description = KEY_MANAGEMENT_FEATURE_ID_TO_DESCRIPTION.get(feature_id, hex_val(feature_id, True, **('strip_leading_zeros',)))
            scheme_id_description = KEY_MANAGEMENT_SCHEME_ID_TO_DESCRIPTION[cls.HEADER_CLASS.CLASS_KEY_MANAGEMENT_SCHEME_ID]
            raise RuntimeError(f'''key_management_feature {feature_id_description} is invalid for key_management_scheme {scheme_id_description}.''')
        return cls.FEATURE_ID_TO_POLICY.get(feature_id)

    get_key_policy = None(get_key_policy)

