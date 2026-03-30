
from cmd_line_interface.sectools.cmd_line_common.base_defines import ROOT_KEY
from cmd_line_interface.sectools.cmd_line_common.defines import CA_CERTIFICATE, CA_KEY, ROOT_CERTIFICATE
from common.crypto.openssl.defines import ALGORITHM_ECDSA, ALGORITHM_RSA, CURVE_ASN1_TO_NORMALIZED_ASN1_NIST, OPENSSL_TO_USER_ALGORITHM_NAMES, SignatureDescription
from common.crypto.openssl.openssl import certificate_key_pair_match, extract_signature_format, extract_signature_format_from_key, generate_attestation_certificate, generate_signature, get_text_from_certificate, get_text_from_key
from common.parser.hash_segment.defines import ATTESTATION, CA, ROOT
from common.parser.hash_segment.hash_segment_common import HashTableSegmentCommon
from common.parser.hash_segment.hash_segment_utils import use_mrc_3_0
from core.base_device_restrictions import BaseDeviceRestrictions
from core.secure_image.signer.base_signer import BaseSigner
from core.secure_image.signer.utils import verify_certificate_signature_format_supported, verify_key_signature_format_supported
from profile.profile_core import SecurityProfile

class LocalSigner(BaseSigner):
    
    def __init__(self = None, image = None, security_profile = None, device_restrictions = None, authority = None, outfile = None, root_certificates = None, root_key = None, ca_certificate = None, ca_key = None, subject = None):
        super().__init__(image, security_profile, device_restrictions, authority, outfile, subject)
        self.root_certificates = root_certificates
        self.root_key = root_key
        self.ca_certificate = ca_certificate
        self.ca_key = ca_key
        self.subject = subject
        self.signature_algorithm = ''
        self.hash_algorithm = ''
        self.ecdsa_curve = ''
        self.rsa_key_size = 0
        self.rsa_exponent = 0
        self.rsa_padding = ''
        self.root_certificate_index = device_restrictions.root_certificate_index
        self.set_signature_format()

    
    def sign(self = None):
        (hash_to_sign, _, subject) = self.get_image_assets(self.hash_algorithm)
        if self.ca_certificate:
            parent_certificate = self.ca_certificate
            parent_certificate_key = self.ca_key
        else:
            parent_certificate = self.root_certificates[self.root_certificate_index]
            parent_certificate_key = self.root_key
        (attestation_certificate, attestation_private_key) = generate_attestation_certificate(parent_certificate, parent_certificate_key, self.hash_algorithm, self.signature_algorithm.lower(), self.ecdsa_curve, self.rsa_key_size, self.rsa_exponent, self.rsa_padding, subject)
        signature = generate_signature(hash_to_sign, attestation_private_key, self.hash_algorithm, self.signature_algorithm.lower(), self.rsa_padding)
        certificate_chain = [
            [],
            [],
            []]
        certificate_chain[ATTESTATION] = [
            attestation_certificate]
        if self.ca_certificate:
            certificate_chain[CA].append(self.ca_certificate)
        for root_certificate in self.root_certificates:
            certificate_chain[ROOT].append(root_certificate)
        return (signature, certificate_chain)

    
    def get_number_of_certificates(self = None):
        if self.ca_certificate:
            return len(self.root_certificates) + 2
        return None + len(self.root_certificates)

    
    def get_signature_algorithm(self = None):
        signature_algorithm = OPENSSL_TO_USER_ALGORITHM_NAMES[self.signature_algorithm]
        if self.signature_algorithm == ALGORITHM_RSA:
            return SignatureDescription(signature_algorithm, self.rsa_key_size)
        if None.signature_algorithm == ALGORITHM_ECDSA:
            return SignatureDescription(signature_algorithm, self.ecdsa_curve.upper())
        return None(signature_algorithm, None)

    
    def get_number_of_root_certificates(self = None):
        return len(self.root_certificates)

    
    def set_signature_format(self = None):
        root_certificates_text = []
        for root_certificate in self.root_certificates:
            root_certificate_text = get_text_from_certificate(root_certificate)
            if not root_certificate_text.startswith('Certificate:'):
                raise RuntimeError(f'''Root certificate provided via {ROOT_CERTIFICATE} is not a certificate.''')
            None.append(root_certificate_text)
        certificate_signature_format = extract_signature_format(root_certificates_text[self.root_certificate_index])
        (self.signature_algorithm, self.hash_algorithm, self.ecdsa_curve, self.rsa_key_size, self.rsa_exponent, self.rsa_padding) = certificate_signature_format
        verify_certificate_signature_format_supported(certificate_signature_format, 'Root', self.root_certificate_index if len(self.root_certificates) > 1 else None)
        if not use_mrc_3_0(len(self.root_certificates)):
            for idx, root_certificate_text in enumerate(root_certificates_text):
                if idx != self.root_certificate_index:
                    certificate_signature_format = extract_signature_format(root_certificate_text)
                    verify_certificate_signature_format_supported(certificate_signature_format, 'Root', idx)
                    if tuple(certificate_signature_format) != (self.signature_algorithm, self.hash_algorithm, self.ecdsa_curve, self.rsa_key_size, self.rsa_exponent, self.rsa_padding):
                        raise RuntimeError('The provided Root certificates have mismatching signature algorithms.')
                    if self.ca_certificate:
                        ca_certificate_text = get_text_from_certificate(self.ca_certificate)
                        if not ca_certificate_text.startswith('Certificate:'):
                            raise RuntimeError(f'''CA certificate provided via {CA_CERTIFICATE} is not a certificate.''')
                        certificate_signature_format = None(ca_certificate_text)
                        verify_certificate_signature_format_supported(certificate_signature_format, 'CA')
                        if tuple(certificate_signature_format) != (self.signature_algorithm, self.hash_algorithm, self.ecdsa_curve, self.rsa_key_size, self.rsa_exponent, self.rsa_padding):
                            certificate_string = 'certificates' if len(self.root_certificates) > 1 else 'certificate'
                            raise RuntimeError(f'''The provided CA certificate and Root {certificate_string} have mismatching signature algorithms.''')
                        for certificate, key, certificate_type, key_type, certificate_arg, key_arg in ((None.root_certificates[self.device_restrictions.root_certificate_index], self.root_key, 'Root certificate', 'Root key', ROOT_CERTIFICATE, ROOT_KEY), (self.ca_certificate, self.ca_key, 'CA certificate', 'CA key', CA_CERTIFICATE, CA_KEY)):
                            if key:
                                key_text = get_text_from_key(key)
                                if 'Private-Key' not in key_text and 'private key' not in key_text:
                                    raise RuntimeError(f'''{key_type} provided via {key_arg} is not a key.''')
                                (curve, key_size, exponent) = None(key)
                                normalized_curve = CURVE_ASN1_TO_NORMALIZED_ASN1_NIST.get(curve, None)
                                verify_key_signature_format_supported(normalized_curve.normalized_asn1 if normalized_curve else normalized_curve, key_size, exponent, key_type)
                                if (normalized_curve.normalized_asn1 if normalized_curve else normalized_curve, key_size, exponent) != (self.ecdsa_curve, self.rsa_key_size, self.rsa_exponent):
                                    certificate_string = 'certificates' if len(self.root_certificates) + 1 if self.ca_certificate else 0 > 1 else 'certificate'
                                    raise RuntimeError(f'''The algorithm of the {key_type} mismatches the provided {certificate_string}.''')
                                if not None(certificate, key):
                                    raise RuntimeError(f'''{certificate_type} provided via {certificate_arg} and {key_type} provided via {key_arg} are incompatible.''')
                                return None

    __classcell__ = None

