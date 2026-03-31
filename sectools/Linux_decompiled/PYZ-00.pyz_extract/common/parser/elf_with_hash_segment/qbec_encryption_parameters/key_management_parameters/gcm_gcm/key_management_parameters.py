
from binascii import hexlify, unhexlify
from os import urandom
from typing import Any, Type
from Cryptodome.Cipher import AES
from Cryptodome.Cipher._mode_gcm import GcmMode
import profile
from common.data.base_parser import BaseParserGenerator, DumpDict
from common.data.defines import PAD_BYTE_0
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import KEY_MANAGEMENT_FEATURE_ID_MODEM_IMAGE
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.gcm_gcm.key_management_parameters_header import KeyManagementParametersHeaderGCMGCM
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.key_management_parameters.key_management_parameters_common import KeyManagementParametersCommon

class KeyManagementParametersGCMGCM(KeyManagementParametersCommon, BaseParserGenerator):
    HEADER_CLASS: Type[KeyManagementParametersHeaderGCMGCM] = KeyManagementParametersHeaderGCMGCM
    WRAPPED_KEY_SIZE: int = 32
    WRAPPED_KEY_IV_SIZE: int = 12
    WRAPPED_KEY_AUTH_TAG_SIZE: int = 16
    WRAPPED_KEY_POLICY_SIZE: int = 8
    
    def __init__(self = None, data = None, **kwargs):
        self.wrapped_keys_ivs = []
        self.wrapped_keys_auth_tags = []
        self.wrapped_keys_policies = []
    # WARNING: Decompyle incomplete

    
    def create_default(self, key_management_feature_id, nonce = None, wrapped_keys = None, wrapped_keys_ivs = None, wrapped_keys_auth_tags = (KEY_MANAGEMENT_FEATURE_ID_MODEM_IMAGE, b'', (b'',), (b'',), (b'',), (b'',)), wrapped_keys_policies = ('key_management_feature_id', int, 'nonce', bytes, 'wrapped_keys', tuple[(bytes, ...)], 'wrapped_keys_ivs', tuple[(bytes, ...)], 'wrapped_keys_auth_tags', tuple[(bytes, ...)], 'wrapped_keys_policies', tuple[(bytes, ...)], 'return', None), **_):
        self.header = self.HEADER_CLASS.from_fields(key_management_feature_id, nonce.rjust(self.HEADER_CLASS.NONCE_SIZE, PAD_BYTE_0), len(wrapped_keys), **('key_management_feature_id', 'nonce', 'num_wrapped_keys'))
        self.wrapped_keys = list(wrapped_keys)
        self.wrapped_keys_ivs = list(wrapped_keys_ivs)
        self.wrapped_keys_auth_tags = list(wrapped_keys_auth_tags)
        self.wrapped_keys_policies = list(wrapped_keys_policies)

    
    def _unpack_wrapped_keys(self = None, data = None):
        offset = 0
        for _ in range(self.header.num_wrapped_keys):
            self.wrapped_keys.append(bytes(data[offset:offset + self.WRAPPED_KEY_SIZE]))
            offset += self.WRAPPED_KEY_SIZE
            self.wrapped_keys_ivs.append(bytes(data[offset:offset + self.WRAPPED_KEY_IV_SIZE]))
            offset += self.WRAPPED_KEY_IV_SIZE
            self.wrapped_keys_auth_tags.append(bytes(data[offset:offset + self.WRAPPED_KEY_AUTH_TAG_SIZE]))
            offset += self.WRAPPED_KEY_AUTH_TAG_SIZE
            self.wrapped_keys_policies.append(bytes(data[offset:offset + self.WRAPPED_KEY_POLICY_SIZE]))
            offset += self.WRAPPED_KEY_POLICY_SIZE

    
    def _pack_wrapped_keys(self = None):
        data = bytearray()
        for wrapped_key, wrapped_key_iv, wrapped_key_auth_tag, wrapped_key_policy in zip(self.wrapped_keys, self.wrapped_keys_ivs, self.wrapped_keys_auth_tags, self.wrapped_keys_policies):
            data += wrapped_key + wrapped_key_iv + wrapped_key_auth_tag + wrapped_key_policy
        return memoryview(data)

    
    def get_variable_size(cls = None, num_keys = None):
        return num_keys * (cls.WRAPPED_KEY_SIZE + cls.WRAPPED_KEY_IV_SIZE + cls.WRAPPED_KEY_AUTH_TAG_SIZE + cls.WRAPPED_KEY_POLICY_SIZE)

    get_variable_size = None(get_variable_size)
    
    def get_dump_files(self = None, directory = None):
        dump_files = super().get_dump_files(directory)
        for iv, auth_tag, policy in enumerate(zip(self.wrapped_keys_ivs, self.wrapped_keys_auth_tags, self.wrapped_keys_policies)):
            dump_files[f'''{directory}/wrapped_keys/wrapped_key_iv_{i}.bin'''] = iv
            dump_files[f'''{directory}/wrapped_keys/wrapped_key_auth_tag_{i}.bin'''] = auth_tag
            dump_files[f'''{directory}/wrapped_keys/wrapped_key_policy_{i}.bin'''] = policy
        return dump_files

    
    def _get_wrapped_key_properties(self = None):
        properties = []
        for wrapped_key, wrapped_key_iv, wrapped_key_auth_tag, wrapped_key_policy in enumerate(zip(self.wrapped_keys, self.wrapped_keys_ivs, self.wrapped_keys_auth_tags, self.wrapped_keys_policies)):
            properties += [
                (f'''Wrapped Key {idx}:''',) + (f'''0x{hexlify(wrapped_key).decode()}''',),
                (f'''IV {idx}:''',) + (f'''0x{hexlify(wrapped_key_iv).decode()}''',),
                (f'''Auth Tag {idx}:''',) + (f'''0x{hexlify(wrapped_key_auth_tag).decode()}''',),
                (f'''Policy {idx}:''',) + (f'''0x{hexlify(wrapped_key_policy).decode()}''',)]
        return properties

    
    def check_is_valid_key_length(cls = None, key_length = None):
        return key_length == cls.WRAPPED_KEY_SIZE

    check_is_valid_key_length = None(check_is_valid_key_length)
    
    def get_key_policy(cls = None, feature_id = None):
        return profile.SECURITY_PROFILE.encryption_format.key_management_scheme.wrapped_key_policy

    get_key_policy = None(get_key_policy)
    
    def wrap_data_encryption_key(cls = None, wrapping_key = None, data_encryption_key = classmethod, policy = (None,)):
        data_encryption_key_policy = unhexlify(policy) if policy else PAD_BYTE_0 * cls.WRAPPED_KEY_POLICY_SIZE
        iv = urandom(cls.WRAPPED_KEY_IV_SIZE)
        cipher = AES.new(wrapping_key, AES.MODE_GCM, iv, **('nonce',))
    # WARNING: Decompyle incomplete

    wrap_data_encryption_key = None(wrap_data_encryption_key)
    __classcell__ = None

