
from typing import Type
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import KEY_MANAGEMENT_FEATURE_ID_GENERIC_TME_CE_IMAGE
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.gcm.key_management_parameters import KeyManagementParametersGCM
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.gcm2.key_management_parameters_header import KeyManagementParametersHeaderGCM2

class KeyManagementParametersGCM2(KeyManagementParametersGCM):
    HEADER_CLASS: Type[KeyManagementParametersHeaderGCM2] = KeyManagementParametersHeaderGCM2
    FEATURE_ID_TO_POLICY = {
        KEY_MANAGEMENT_FEATURE_ID_GENERIC_TME_CE_IMAGE: '201C160448400300' }

