
from typing import Type
from common.data.base_parser import BaseParserGenerator
from common.data.data import hex_val
from common.data.defines import PAD_BYTE_0
from common.logging.logger import log_warning
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import KEY_MANAGEMENT_FEATURE_ID_AUDIO_IMAGE, KEY_MANAGEMENT_FEATURE_ID_FLASH_BINARY, KEY_MANAGEMENT_FEATURE_ID_TO_DESCRIPTION, KEY_MANAGEMENT_SCHEME_ID_TO_DESCRIPTION, XTS_ENCRYPTION_LABEL
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.key_management_parameters_common import KeyManagementParametersCommon
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.xts.key_management_parameters_header import KeyManagementParametersHeaderXTS

class KeyManagementParametersXTS(KeyManagementParametersCommon, BaseParserGenerator):
    HEADER_CLASS: Type[KeyManagementParametersHeaderXTS] = KeyManagementParametersHeaderXTS
    FEATURE_ID_TO_POLICY: dict[(int | None, str)] = {
        None: '20CC930808300400',
        KEY_MANAGEMENT_FEATURE_ID_AUDIO_IMAGE: '20CC931008301000',
        KEY_MANAGEMENT_FEATURE_ID_FLASH_BINARY: '20CC930808300400' }
    
    def create_default(self, label = None, nonce = None, public_key_x = None, public_key_y = (XTS_ENCRYPTION_LABEL, b'', b'', b'', (b'',)), wrapped_keys = ('label', bytes, 'nonce', bytes, 'public_key_x', bytes, 'public_key_y', bytes, 'wrapped_keys', tuple[(bytes, ...)], 'return', None), **_):
        self.header = self.HEADER_CLASS.from_fields(label, nonce.rjust(self.HEADER_CLASS.NONCE_SIZE, PAD_BYTE_0), public_key_x.rjust(self.HEADER_CLASS.X_Y_SIZE, PAD_BYTE_0), public_key_y.rjust(self.HEADER_CLASS.X_Y_SIZE, PAD_BYTE_0), len(wrapped_keys), **('label', 'nonce', 'public_key_x', 'public_key_y', 'num_wrapped_keys'))
        self.wrapped_keys = list(wrapped_keys)

    
    def check_is_valid_key_length(cls = None, key_length = None):
        return key_length <= cls.WRAPPED_KEY_SIZE

    check_is_valid_key_length = None(check_is_valid_key_length)
    
    def get_key_policy(cls = None, feature_id = None):
        if policy = cls.FEATURE_ID_TO_POLICY.get(feature_id) is None:
            feature_id_description = KEY_MANAGEMENT_FEATURE_ID_TO_DESCRIPTION.get(feature_id, hex_val(feature_id, True, **('strip_leading_zeros',)))
            scheme_id_description = KEY_MANAGEMENT_SCHEME_ID_TO_DESCRIPTION[cls.HEADER_CLASS.CLASS_KEY_MANAGEMENT_SCHEME_ID]
            log_warning(f'''key_management_feature {feature_id_description}, for key_management_scheme {scheme_id_description} does not have a defined policy.''')
        return policy

    get_key_policy = None(get_key_policy)

