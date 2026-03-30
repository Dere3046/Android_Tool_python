
from typing import Type
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.primitives.cmac import CMAC
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.gcm.key_management_parameters import KeyManagementParametersGCM
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.siv_cmac_gcm.key_management_parameters_header import KeyManagementParametersHeaderSIVCMACGCM

class KeyManagementParametersSIVCMACGCM(KeyManagementParametersGCM):
    HEADER_CLASS: Type[KeyManagementParametersHeaderSIVCMACGCM] = KeyManagementParametersHeaderSIVCMACGCM
    
    def get_key_policy(cls = None, feature_id = None):
        return '203c15081a410400'

    get_key_policy = None(get_key_policy)
    
    def process_data_encryption_key(cls = None, data_encryption_key = None):
        c1 = CMAC(algorithms.AES(data_encryption_key))
        c1.update(b'LLM IP Protection')
        c2 = CMAC(algorithms.AES(data_encryption_key))
        c2.update(b'Software Key')
        return c1.finalize() + c2.finalize()

    process_data_encryption_key = None(process_data_encryption_key)

