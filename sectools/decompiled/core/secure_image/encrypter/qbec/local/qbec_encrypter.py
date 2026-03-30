
from abc import ABC
from typing import Any
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey
from common.crypto.key_management.key_management_utils import generate_ecdsa_secp384r1_key_pair, get_device_public_keys_with_hw_context, get_ecdh_shared_key, get_hkdf_key
from common.crypto.openssl.openssl import get_x_y_from_ecdsa_public_key2
from common.data.data import reverse
from common.parser.elf_with_hash_segment.elf_with_hash_segment import ELFWithHashTableSegment
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import KEY_MANAGEMENT_SCHEME_DESCRIPTION_TO_ID, KEY_MANAGEMENT_SCHEME_ID_ECDH_P384_HKDF_SIV_CMAC_GCM, KEY_MANAGEMENT_SCHEME_ID_ECDH_P384_HKDF_SIV_GCM, KEY_MANAGEMENT_SCHEME_ID_TO_DIVERSIFIER_LABEL
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec import KEY_MANAGEMENT_PARAMETER_CLASSES
from core.secure_image.encrypter.base_encrypter import BaseEncrypter
from profile.profile_core import SecurityProfile
from profile.schema import EncryptionFormat

class QBECEncrypter(ABC, BaseEncrypter):
    
    def __init__(self = None, parsed_image = None, security_profile = None, encrypting_entity = None, key_management_feature_id = None, device_public_keys = None, device_private_key = None, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def _get_wrapped_data_encryption_keys(self = None, private_key = None):
        wrapped_keys = []
        policy = self.key_management_parameter_class.get_key_policy(self.key_management_feature_id)
    # WARNING: Decompyle incomplete

    
    def set_key_management_wrapped_keys(self = None):
        (private_key, public_key) = generate_ecdsa_secp384r1_key_pair()
        public_key_xy = get_x_y_from_ecdsa_public_key2(public_key)
        self.public_key_x = public_key_xy.x
        self.public_key_y = public_key_xy.y
        self.wrapped_keys = self._get_wrapped_data_encryption_keys(private_key)
        self.data_encryption_key = self.key_management_parameter_class.process_data_encryption_key(self.data_encryption_key)

    __classcell__ = None

