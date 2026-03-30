
from typing import Type
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.gcm.key_management_parameters import KeyManagementParametersGCM
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.siv_64_gcm.key_management_parameters_header import KeyManagementParametersHeaderSIV64GCM

class KeyManagementParametersSIV64GCM(KeyManagementParametersGCM):
    HEADER_CLASS: Type[KeyManagementParametersHeaderSIV64GCM] = KeyManagementParametersHeaderSIV64GCM
    WRAPPED_KEY_SIZE = 64
    
    def pad_ciphertext(ciphertext = None):
        return ciphertext

    pad_ciphertext = None(pad_ciphertext)
    
    def get_key_policy(cls = None, feature_id = None):
        return '0000000000000000'

    get_key_policy = None(get_key_policy)

