
from binascii import hexlify, unhexlify
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.ec import ECDH, EllipticCurvePrivateKey, EllipticCurvePublicKey, SECP384R1, generate_private_key
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cmd_line_interface.sectools.cmd_line_common.defines import INFILE
from cmd_line_interface.sectools.secure_image.defines import DEVICE_PUBLIC_KEY
from common.crypto.key_management.defines import BSVE, DIVERSIFIER_LABEL_LENGTH, KEY_LENGTH, PUBLIC_KEY_LENGTH, SALT
from common.data.defines import PAD_BYTE_0
from common.logging.logger import log_warning
from common.parser.hash_segment.defines import AUTHORITY_OEM
from core.profile_validator.validate import ERROR_STRING
from profile.schema import EncryptionFormat

def get_device_public_keys_with_hw_context(authority = None, encryption_format = None, device_public_keys = None):
    public_keys_hw_context = []
# WARNING: Decompyle incomplete


def generate_ecdsa_secp384r1_key_pair():
    private_key = generate_private_key(SECP384R1())
    return (private_key, private_key.public_key().public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo, **('encoding', 'format')))


def get_ecdh_shared_key(public_key = None, private_key = None):
    return private_key.exchange(ECDH(), EllipticCurvePublicKey.from_encoded_point(SECP384R1(), unhexlify('02' + public_key)))


def get_hkdf_key(inkey = None, diversifier_label = None, bsve = None, hw_context = ('inkey', bytes, 'diversifier_label', str, 'bsve', bytes, 'hw_context', bytes, 'return', bytes)):
    return HKDF(hashes.SHA256(), 64, SALT, bytes(diversifier_label, 'utf-8').ljust(DIVERSIFIER_LABEL_LENGTH, PAD_BYTE_0) + bsve + hw_context + KEY_LENGTH, **('algorithm', 'length', 'salt', 'info')).derive(inkey)

