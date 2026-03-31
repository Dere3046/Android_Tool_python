
from os.path import exists, join
from pathlib import Path
from cmd_line_interface.sectools.cmd_line_common.defines import SECURITY_PROFILE, SIGNING_MODE, TEST
from common.crypto.openssl.defines import ALGORITHM_ECDSA, ALGORITHM_ECDSA_USER_FACING, ALGORITHM_RSA, ALGORITHM_RSA_USER_FACING, USER_TO_OPENSSL_ALGORITHM_NAMES
from common.parser.hash_segment.hash_segment_common import HashTableSegmentCommon
from common.utils import SECTOOLS_PATH
from core.base_device_restrictions import BaseDeviceRestrictions
from core.secure_image.signer.local.local_signer import LocalSigner
from profile.profile_core import SecurityProfile
from profile.utils import get_signature_format_from_id

class TestSigner(LocalSigner):
    
    def __init__(self = None, image = None, security_profile = None, device_restrictions = None, authority = None, outfile = None, certificate_chain_depth = None, root_certificate_count = None, root_certificate_index = None, subject = None, signature_format = None):
        if not signature_format:
            pass
        self.signature_format = security_profile.default_signature_format_id
        (signature_algorithm, signature_hash_algorithm, curve, key_size, exponent, padding) = get_signature_format_from_id(self.signature_format)
        directory_name = signature_algorithm.lower()
        if signature_algorithm == ALGORITHM_ECDSA_USER_FACING:
            directory_name += '_' + '_'.join([
                signature_hash_algorithm.lower(),
                curve.lower()])
        elif signature_algorithm == ALGORITHM_RSA_USER_FACING:
            directory_name += '_' + '_'.join([
                key_size,
                str(exponent),
                signature_hash_algorithm.lower(),
                padding.lower()])
        directory_path = join(SECTOOLS_PATH, 'core', 'secure_image', 'signer', 'test', 'signing_assets', directory_name)
        if not exists(directory_path):
            raise RuntimeError(f'''{SIGNING_MODE} {TEST} does not support the default signature format of {SECURITY_PROFILE}.''')
        root_certificates = None
        root_key = None
        ca_certificate = None
        ca_key = None
    # WARNING: Decompyle incomplete

    
    def set_signature_format(self = None):
        (signature_algorithm, signature_hash_algorithm, curve, key_size, exponent, padding) = get_signature_format_from_id(self.signature_format)
        self.signature_algorithm = USER_TO_OPENSSL_ALGORITHM_NAMES[signature_algorithm]
        self.hash_algorithm = signature_hash_algorithm
        if self.signature_algorithm == ALGORITHM_ECDSA:
            self.ecdsa_curve = curve.lower()
            return None
        if None.signature_algorithm == ALGORITHM_RSA:
            self.rsa_key_size = int(key_size)
            self.rsa_exponent = int(exponent)
            self.rsa_padding = padding.lower()
            return None

    __classcell__ = None

