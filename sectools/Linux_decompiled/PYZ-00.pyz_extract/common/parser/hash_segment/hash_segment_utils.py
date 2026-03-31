
from binascii import hexlify
from collections import defaultdict
from re import IGNORECASE, search
from typing import Any
import profile
from cmd_line_interface.sectools.cmd_line_common.base_defines import SECURITY_PROFILE, SIGN
from common.crypto.openssl.defines import SHA_DESCRIPTION_TO_CERTIFICATE_HASH_SIZE, SIGNATURE_DESCRIPTION_TO_SIZE, SignatureDescription, OPENSSL_TO_USER_ALGORITHM_NAMES
from common.crypto.openssl.openssl import RS, SignatureFormat, get_text_from_certificate
from common.data.certificate import get_certificate_sequence_size, is_inactive_mrc_3_0_certificate
from common.data.data import and_separated, are_or_is, plural_noun, plural_s
from common.data.defines import SHA_SIZE_TO_DESCRIPTION
from common.parser.hash_segment.defines import MRC_3_0
from core.secure_image.signer.defines import OU_SN, OU_SOC_VERS

def get_ou_fields_dict_from_strings(ou_field_strings = None):
    ou_fields = { }
    for ou_field in ou_field_strings:
        match = search('ou[ ]*=[ ]*[0-9][0-9] ([0-9a-f]+[ [0-9a-f]+]*) (.+)', ou_field, IGNORECASE)
        if match:
            ou_name = match.group(2).upper()
            val_lst = (lambda .0: [ '0x' + item for item in .0 ])(match.group(1).split(' '))
            if ou_name in (OU_SOC_VERS, OU_SN):
                ou_fields.setdefault(ou_name, [])
                ou_fields[ou_name] += (lambda .0: [ item for item in .0 if int(item, 16) ])(val_lst)
                continue
            ou_fields.setdefault(ou_name, val_lst[0])
    return ou_fields


def get_ou_fields(attestation_certificate = None):
    subject = []
# WARNING: Decompyle incomplete


def get_signature_properties(r_and_s = None, signature_properties = None, extended_key_usage = None, is_signature = ('', True, ''), certificate_index_string = ('r_and_s', RS, 'signature_properties', SignatureFormat, 'extended_key_usage', str, 'is_signature', bool, 'certificate_index_string', str, 'return', list[tuple[(str, Any)]])):
    properties = []
    if extended_key_usage:
        properties += [
            ('Extended Key Usage:', extended_key_usage)]
    if signature_properties.signature_algorithm:
        property_string = 'Algorithm:' if is_signature else f'''{certificate_index_string}Signature Algorithm:'''
        algorithm = OPENSSL_TO_USER_ALGORITHM_NAMES.get(signature_properties.signature_algorithm, signature_properties.signature_algorithm.upper())
        properties += [
            (property_string, algorithm)]
    if signature_properties.hash_algorithm:
        properties += [
            (f'''{certificate_index_string}Hash Algorithm:''', signature_properties.hash_algorithm)]
    if signature_properties.curve:
        properties += [
            (f'''{certificate_index_string}Curve:''', signature_properties.curve)]
    if r_and_s.r and r_and_s.s:
        properties += [
            (f'''{certificate_index_string}R Size:''', f'''{r_and_s.r_size} (bytes)'''),
            (f'''{certificate_index_string}S Size:''', f'''{r_and_s.s_size} (bytes)'''),
            (f'''{certificate_index_string}R:''', '0x' + r_and_s.r.lower()),
            (f'''{certificate_index_string}S:''', '0x' + r_and_s.s.lower())]
    if signature_properties.key_size:
        properties += [
            (f'''{certificate_index_string}Key Size:''', signature_properties.key_size)]
    if signature_properties.exponent:
        properties += [
            (f'''{certificate_index_string}Exponent:''', signature_properties.exponent)]
    if signature_properties.padding:
        properties += [
            (f'''{certificate_index_string}Padding:''', signature_properties.padding.upper())]
    return properties


def get_mrc_3_0_certificate_properties(size = None, certificate = None, certificate_index_string = None):
    return [
        (f'''{certificate_index_string}Hash ({SHA_SIZE_TO_DESCRIPTION.get(size, 'Unknown Hash Algorithm')}):''', '0x' + hexlify(bytes(certificate)[2:]).decode())]


def get_max_signature_and_certificate_chain_size(current_operation = None, number_of_certificates = None, number_of_root_certificates = None, signature_algorithm = ('current_operation', str, 'number_of_certificates', int, 'number_of_root_certificates', int, 'signature_algorithm', SignatureDescription | None, 'return', tuple[(int, int)])):
    pass
# WARNING: Decompyle incomplete


def validate_software_id(image_software_id = None, security_profile_software_id = None, image_type = None):
    if image_software_id != security_profile_software_id:
        raise RuntimeError(f'''Software ID, {hex(image_software_id)}, of {image_type} does not match the value, {hex(security_profile_software_id)}, defined in {SECURITY_PROFILE}.''')


def use_mrc_3_0(root_certificate_count = None):
    if root_certificate_count > 1:
        pass
    return profile.SECURITY_PROFILE.default_mrc_spec == MRC_3_0


def get_inactive_rch_algorithms(root_certificates = None):
    inactive_rch_algorithms = defaultdict(list)
    for idx, certificate in enumerate(root_certificates):
        certificate_size = get_certificate_sequence_size(certificate)
        if is_inactive_mrc_3_0_certificate(certificate_size):
            inactive_rch_algorithms[SHA_SIZE_TO_DESCRIPTION[certificate_size]].append(idx)
    return inactive_rch_algorithms


def check_rch_algorithm_uniformity(inactive_rch_algorithms = None):
    rch_mismatch_string = ''
    if len(inactive_rch_algorithms) > 1:
        rch_mismatch_string = 'Inactive root certificates are hashed with different algorithms.'
        for hash_algorithm, indices in sorted(inactive_rch_algorithms.items()):
            rch_mismatch_string += f''' Root{plural_s(indices)} at {plural_noun('index', len(indices))} {and_separated(indices)} {are_or_is(indices)} hashed using {hash_algorithm}.'''
    return rch_mismatch_string

