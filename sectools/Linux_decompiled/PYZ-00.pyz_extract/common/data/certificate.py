
import struct
import profile
from cmd_line_interface.sectools.cmd_line_common.defines import SECURITY_PROFILE
from common.crypto.openssl.openssl import get_authority_and_subject_key_identifiers, get_text_from_certificate, verify_certificate
from common.data.binary_struct import StructBase
from common.data.data import non_empty_strings_match, non_empty_strings_mismatch, plural_s
from common.data.defines import PAD_BYTE_1, SHA_DESCRIPTION_TO_FUNCTION, SHA_DESCRIPTION_TO_SIZE, SHA_SIZE_TO_DESCRIPTION
from profile.schema import MRCSpecs

class ASN1SequenceHeader(StructBase):
    SEQUENCE = 48
    SEQUENCE_SIZE_MASK = 128
    
    def __init__(self = None, data = None, check_is_type = None, bypass_validation = None):
        self.total_size = 0
        self.sequence_size = 0
        self.tag = 0
        super().__init__(data, check_is_type, bypass_validation, **('data', 'check_is_type', 'bypass_validation'))

    
    def get_fields(cls):
        return [
            'tag',
            'sequence_size']

    get_fields = classmethod(get_fields)
    
    def get_format(cls):
        return '<BB'

    get_format = classmethod(get_format)
    
    def unpack_post_process(self):
        if not self.sequence_size & ASN1SequenceHeader.SEQUENCE_SIZE_MASK:
            self.total_size = self.sequence_size + self.get_size()
            return None
        num_bytes_containing_size = None.sequence_size & 127
        data_containing_size = self.data[self.get_size():self.get_size() + num_bytes_containing_size]
        sequence_size = 0
        offset = 0
        for _ in range(num_bytes_containing_size):
            end = offset + 1
            byte = data_containing_size[offset:end]
            sequence_size = sequence_size * 256 + struct.unpack_from('<B', byte, 0)[0]
            offset = end
        self.total_size = self.get_size() + num_bytes_containing_size + sequence_size

    
    def validate(self):
        if self.tag != self.SEQUENCE:
            raise RuntimeError('Certificate does not contain valid ASN.1 tag.')
        if None.total_size == 0:
            raise RuntimeError("Certificate's ASN.1-encoded size is invalid.")

    __classcell__ = None


def classify_mrc_2_0_certificates(certificate_chain = None, attestation_certificates = None):
    ca_certificates = []
    root_certificates = []
    key_identifiers_list = list(map(get_authority_and_subject_key_identifiers, certificate_chain))
    candidate_ca_certificate = certificate_chain[1]
    (_, attestation_authority_key_id) = key_identifiers_list[0]
    (candidate_ca_subject_key_id, candidate_ca_authority_key_id) = key_identifiers_list[1]
    if len(certificate_chain) > 2:
        if non_empty_strings_mismatch(attestation_authority_key_id, candidate_ca_subject_key_id):
            root_certificates = certificate_chain[1:]
            return (ca_certificates, root_certificates)
        if None(attestation_authority_key_id, candidate_ca_subject_key_id):
            for root_subject_key_id, _ in enumerate(key_identifiers_list[2:], 2, **('start',)):
                if root_subject_key_id:
                    if root_subject_key_id == candidate_ca_authority_key_id:
                        ca_certificates = [
                            certificate_chain[1]]
                        root_certificates = certificate_chain[2:]
                    
                if verify_certificate(candidate_ca_certificate, certificate_chain[idx]):
                    ca_certificates = [
                        certificate_chain[1]]
                    root_certificates = certificate_chain[2:]
                
                root_certificates = certificate_chain[1:]
                return (ca_certificates, root_certificates)
                attestation_signed_by_candidate_ca = verify_certificate(candidate_ca_certificate, attestation_certificates[0])
                candidate_ca_signed_by_root = None((lambda .0 = None: for root_cert in .0:
verify_certificate(root_cert, candidate_ca_certificate))(certificate_chain[2:]))
                if attestation_signed_by_candidate_ca and candidate_ca_signed_by_root:
                    ca_certificates = [
                        candidate_ca_certificate]
                    root_certificates = certificate_chain[2:]
                    return (ca_certificates, root_certificates)
                root_certificates = None[1:]
                return (ca_certificates, root_certificates)
                root_certificates = [
                    candidate_ca_certificate]
                return (ca_certificates, root_certificates)


def classify_mrc_3_0_certificates(certificate_chain = None, number_of_roots_as_hash = None):
    ca_certificates = []
    if number_of_roots_as_hash == len(certificate_chain) - 3:
        ca_certificates = [
            certificate_chain[1]]
        root_certificates = certificate_chain[2:]
        return (ca_certificates, root_certificates)
    root_certificates = None[1:]
    return (ca_certificates, root_certificates)


def split_certificate_chain_der(data = None):
    ''' Returns an array of DER-encoded certificates given a concatenated sequence of DER-encoded certificates. '''
    certificate_chain = []
    root_certificates = []
    ca_certificates = []
    attestation_certificates = []
    offset = 0
    if offset < len(data):
        pass
    return (lambda .0: [ list(map(memoryview, certificates)) for certificates in .0 ])((attestation_certificates, ca_certificates, root_certificates))


def validate_certificate_chain_depth(certificate_chain = None, allowed_certificate_chain_depths = None):
    certificate_chain_depth = sum((lambda .0: for level in .0:
passcontinue1[0])(certificate_chain))
    if certificate_chain_depth not in allowed_certificate_chain_depths:
        raise RuntimeError(f'''A certificate chain depth of {certificate_chain_depth} is not supported by {SECURITY_PROFILE}.''')


def validate_root_certificate_count_against_mrc_spec(root_certificate_count = None, mrc_specs = None):
    max_roots = 1
    if mrc_specs:
        max_roots = mrc_specs.max_root_certificate_count
    if root_certificate_count > max_roots:
        raise RuntimeError(f'''The root certificate count, {root_certificate_count}, exceeds the maximum of {max_roots} root certificate{plural_s(max_roots)} supported by the Security Profile provided via {SECURITY_PROFILE}.''')


def get_certificate_chain_list_text(certificate_chain_list = None):
    certificate_chain_text = [
        [],
        [],
        []]
    for certificate_level, certificates in enumerate(certificate_chain_list):
        for certificate in certificates:
            if certificate:
                certificate_chain_text[certificate_level].append(get_text_from_certificate(certificate))
    return certificate_chain_text


def get_certificate_sequence_size(certificate = None):
    return ASN1SequenceHeader(certificate).sequence_size


def is_inactive_mrc_3_0_certificate(certificate_size = None):
    return certificate_size in SHA_SIZE_TO_DESCRIPTION


def get_mrc_3_0_root_certificates(root_certificates = None, mrc_index = None):
    mrc_3_0_roots_certificates = []
# WARNING: Decompyle incomplete

