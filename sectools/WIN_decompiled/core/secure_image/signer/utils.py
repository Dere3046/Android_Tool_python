
import profile
from cmd_line_interface.sectools.cmd_line_common.defines import SECURITY_PROFILE
from cmd_line_interface.sectools.defines import SECTOOLS_DESCRIPTION
from common.crypto.openssl.defines import ALGORITHM_ECDSA, ALGORITHM_ECDSA_USER_FACING, ALGORITHM_RSA, ALGORITHM_RSA_USER_FACING, CURVE_SECP256R1, CURVE_SECP384R1, KEY_SIZE_2048, KEY_SIZE_4096, OPENSSL_TO_USER_ALGORITHM_NAMES, PQC_SIGNATURE_ALGORITHMS, RSA_4K_SIGNATURE_SIZE, SIGNATURE_DESCRIPTION_TO_SIZE
from common.crypto.openssl.openssl import SignatureFormat, extract_r_and_s_from_signature, extract_signature_format, get_curve_names_without_rs_48_49
from common.data.certificate import get_certificate_chain_list_text
from common.logging.logger import log_debug
from common.parser.hash_segment.defines import ATTESTATION, CA, CERTIFICATE_LEVEL_DESCRIPTION, ROOT
from common.parser.hash_segment.hash_segment_utils import use_mrc_3_0

def verify_key_signature_format_supported(curve = None, key_size = None, exponent = None, key_type = ('curve', str, 'key_size', int, 'exponent', int, 'key_type', str, 'return', None)):
    pass
# WARNING: Decompyle incomplete


def verify_certificate_signature_format_supported(signature_format = None, certificate_type = None, idx = None):
    pass
# WARNING: Decompyle incomplete


def verify_signature_format_supported(signature = None, attestation_certificate_format = None):
    r_and_s = extract_r_and_s_from_signature(signature)
    if r_and_s.r and r_and_s.s:
        log_debug(f'''R and S values present. Verifying ECDSA format of signature against {CERTIFICATE_LEVEL_DESCRIPTION[ATTESTATION]} certificate.''')
        if attestation_certificate_format.signature_algorithm != ALGORITHM_ECDSA:
            raise RuntimeError(f'''Signature algorithm, {attestation_certificate_format.signature_algorithm.upper()}, of the {CERTIFICATE_LEVEL_DESCRIPTION[ATTESTATION]} certificate mismatches the expected algorithm, {ALGORITHM_ECDSA_USER_FACING}.''')
        certificate_curve = None.curve
        if {
            r_and_s.r_size,
            r_and_s.s_size}.issubset({
            32,
            33}) or certificate_curve != CURVE_SECP256R1 or {
            r_and_s.r_size,
            r_and_s.s_size}.issubset({
            48,
            49}) or certificate_curve != CURVE_SECP384R1:
            raise RuntimeError(f'''R and S sizes, {r_and_s.r_size} and {r_and_s.s_size}, of the signature are not compatible with the ECDSA curve, {certificate_curve}, of the {CERTIFICATE_LEVEL_DESCRIPTION[ATTESTATION]} certificate.''')
        return None
    return None
    if len(signature) <= RSA_4K_SIGNATURE_SIZE:
        log_debug(f'''Verifying RSA format of signature against {CERTIFICATE_LEVEL_DESCRIPTION[ATTESTATION]} certificate.''')
        if attestation_certificate_format.signature_algorithm != ALGORITHM_RSA:
            raise RuntimeError(f'''Signature algorithm, {attestation_certificate_format.signature_algorithm.upper()}, of the {CERTIFICATE_LEVEL_DESCRIPTION[ATTESTATION]} certificate mismatches the expected algorithm, {ALGORITHM_RSA_USER_FACING}.''')
        if None(signature) in (256, 512):
            if len(signature) == 256 or attestation_certificate_format.key_size != KEY_SIZE_2048 or len(signature) == 512 or attestation_certificate_format.key_size != KEY_SIZE_4096:
                raise RuntimeError(f'''Length of the signature, {len(signature)}, is not compatible with the RSA key size, {attestation_certificate_format.key_size}, of the {CERTIFICATE_LEVEL_DESCRIPTION[ATTESTATION]} certificate.''')
            return None
        return None
    raise None(f'''Length of the RSA signature, {len(signature)}, is not recognized by {SECTOOLS_DESCRIPTION}. Allowed lengths are 256 and 512.''')
    algorithm = OPENSSL_TO_USER_ALGORITHM_NAMES[attestation_certificate_format.signature_algorithm]
    log_debug(f'''Verifying that {algorithm} algorithm of signature matches that of the {CERTIFICATE_LEVEL_DESCRIPTION[ATTESTATION]} certificate.''')
    signature_size = SIGNATURE_DESCRIPTION_TO_SIZE[(algorithm, None)].max_signature_size
    if len(signature) != signature_size:
        raise RuntimeError(f'''Length of the {attestation_certificate_format.signature_algorithm}  signature, {len(signature)}, is not recognized by {SECTOOLS_DESCRIPTION}. Expected length is {signature_size}.''')


def validate_signature_and_certificate_format_supported(signature = None, certificate_chain = None, mrc_index = None):
    attestation_certificate_signature_format = None
    parsed_certificate_chain = get_certificate_chain_list_text(certificate_chain)
    mrc_3_0 = use_mrc_3_0(len(certificate_chain[ROOT]))
    for certificate_level, certificates in enumerate(parsed_certificate_chain):
        for idx, certificate in enumerate(certificates):
            if certificate:
                if certificate_level == ATTESTATION:
                    attestation_certificate_signature_format = extract_signature_format(certificate)
                sig_format_str = f'''signature format of {CERTIFICATE_LEVEL_DESCRIPTION[certificate_level]} certificate'''
                log_debug(f'''Extracting {sig_format_str}.''')
                certificate_signature_format = extract_signature_format(certificate)
                log_debug(f'''Extracted {sig_format_str}: {certificate_signature_format.get_format_string()}''')
                if (mrc_3_0 and certificate_level == CA or certificate_level == ROOT) and idx == mrc_index and attestation_certificate_signature_format != certificate_signature_format:
                    raise RuntimeError(f'''The signature algorithm of the {CERTIFICATE_LEVEL_DESCRIPTION[certificate_level]} and {CERTIFICATE_LEVEL_DESCRIPTION[ATTESTATION]} certificates mismatch.''')
                None(f'''{CERTIFICATE_LEVEL_DESCRIPTION[certificate_level]} certificate text present. Verifying certificate format.''')
                verify_certificate_signature_format_supported(certificate_signature_format, CERTIFICATE_LEVEL_DESCRIPTION[certificate_level])
    if attestation_certificate_signature_format:
        log_debug(f'''{CERTIFICATE_LEVEL_DESCRIPTION[ATTESTATION]} certificate text present. Verifying signature.''')
        verify_signature_format_supported(signature, attestation_certificate_signature_format)
        return None

