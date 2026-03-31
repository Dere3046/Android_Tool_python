
import hashlib
from abc import abstractmethod
from functools import partial
from itertools import chain
from typing import Any, Type
from colorama import Fore
import profile
from cmd_line_interface.sectools.cmd_line_common.defines import HASH, INFILE, MEASUREMENT_REGISTER_TARGET, ROOT_CERTIFICATE_INDEX, SIGN, TRANSFER_ROOT
from cmd_line_interface.sectools.secure_image.defines import ENABLE, ENCRYPT, SECONDARY_SOFTWARE_ID
from common.crypto.openssl.defines import SignatureDescription
from common.crypto.openssl.openssl import extract_certificate_key_usage, extract_r_and_s_from_signature, get_signature_from_certificate_text, get_signature_without_padding
from common.data.base_parser import BaseParserGenerator, DumpDict
from common.data.binary_struct import DetailsTuple
from common.data.certificate import ASN1SequenceHeader, get_certificate_chain_list_text, get_certificate_sequence_size, get_mrc_3_0_root_certificates, is_inactive_mrc_3_0_certificate, split_certificate_chain_der
from common.data.data import a_or_an, ceil_to_multiple, color_string, comma_separated_string, hex_val, properties_repr, tuple_to_version_string, version_string_to_tuple
from common.data.defines import ONE_SHOT_HASH_ALGORITHMS, PAD_BYTE_0, PAD_BYTE_1, SHA256_DESCRIPTION, SHA384_DESCRIPTION, SHA_DESCRIPTION_TO_FUNCTION
from common.logging.logger import log_debug
from common.parser.elf_with_hash_segment.hash_table_segment_header import HashTableSegmentHeaderCommon
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import ENCRYPTED_THEN_SIGNED, ENCRYPTING_ENTITY_DESCRIPTION, QBEC_VERSION_1, QBEC_VERSION_2
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec import QBECEncryptionParametersCommon
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec_block_encryption_parameters import QBECBlockEncryptionParameters
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec_segment_encryption_parameters import QBECSegmentEncryptionParameters
from common.parser.elf_with_hash_segment.uie_encryption_parameters.uie_encryption_parameters import UIEEncryptionParameters
from common.parser.elf_with_hash_segment.v3.binding_implementation_ou_fields import BindingImplementationOUFields
from common.parser.elf_with_hash_segment.v3.hash_table_segment_header import HashTableSegmentHeaderV3
from common.parser.elf_with_hash_segment.v5.hash_table_segment_header import HashTableSegmentHeaderV5
from common.parser.elf_with_hash_segment.v6.hash_table_segment_header import HashTableSegmentHeaderV6
from common.parser.elf_with_hash_segment.v6.metadata.v0_0.metadata_0_0 import Metadata
from common.parser.elf_with_hash_segment.v7.hash_table_segment_header import HashTableSegmentHeaderV7
from common.parser.elf_with_hash_segment.v7.metadata.defines import MEASUREMENT_REGISTER_TARGETS_DESCRIPTION_TO_INT, MEASUREMENT_REGISTER_TARGETS_INT_TO_DESCRIPTION, NoMR
from common.parser.elf_with_hash_segment.v8.hash_table_segment_header import HashTableSegmentHeaderV8
from common.parser.hash_segment.defines import ATTESTATION, AUTHORITY_OEM, AUTHORITY_QTI, CA, CERTIFICATE_LEVEL_DESCRIPTION, HASH_SEGMENT_V3, HASH_SEGMENT_V6, HASH_SEGMENT_V7, HASH_SEGMENT_V8, PRODUCTION_ROOT_HASHES, ROOT, TEST_ROOT_HASHES
from common.parser.hash_segment.hash_segment_utils import check_rch_algorithm_uniformity, get_inactive_rch_algorithms, get_max_signature_and_certificate_chain_size, get_mrc_3_0_certificate_properties, get_ou_fields, get_signature_properties, use_mrc_3_0, validate_software_id
from common.parser.mbn.defines import HASH_TABLE_SEGMENT_HEADER_CLASSES
from common.parser.mbn.mbn_header import MBNHeader
from common.parser.mbn.v3.mbn_header import MBNHeaderV3
from common.parser.mbn.v5.mbn_header import MBNHeaderV5
from common.parser.mbn.v6.mbn_header import MBNHeaderV6
from common.parser.mbn.v7.mbn_header import MBNHeaderV7
from common.parser.mbn.v8.mbn_header import MBNHeaderV8
from core.base_device_restrictions import BaseDeviceRestrictions
from core.secure_image.signer.utils import extract_signature_format
from core.secure_image.validate.show_value_comparison_table import make_value_comparison_table
from profile.profile_core import SecurityProfile
from profile.schema import EncryptionFeatures

class HashTableSegmentCommon(BaseParserGenerator):
    
    def __init__(self = None, data = None, **kwargs):
        self.header = None
        self.qti_signature = memoryview(bytearray())
        self.qti_certificate_chain = memoryview(bytearray())
        self.qti_certificate_chain_list = [
            [],
            [],
            []]
        self.oem_signature = memoryview(bytearray())
        self.oem_certificate_chain = memoryview(bytearray())
        self.oem_certificate_chain_list = [
            [],
            [],
            []]
        self.encryption_parameters = None
        self.padding = memoryview(bytearray())
        self.image_prepped_for_encryption = False
        self.image_prepped_for_signing = False
    # WARNING: Decompyle incomplete

    
    def create_default(self = None, *, hash_table_segment_version, common_metadata_version, **_):
        pass
    # WARNING: Decompyle incomplete

    
    def unpack(self = None, data = None):
        self.unpack_header(data, HashTableSegmentHeaderCommon(data).version)
    # WARNING: Decompyle incomplete

    
    def unpack_header(self = None, data = None, version = abstractmethod):
        pass

    unpack_header = None(unpack_header)
    
    def unpack_encryption_parameters(self = None, remaining_data = None):
        pass

    unpack_encryption_parameters = None(unpack_encryption_parameters)
    
    def contains_encrypted_data(self = None):
        pass

    contains_encrypted_data = None(contains_encrypted_data)
    
    def unpack_hash_table_or_code(self = None, data = None):
        pass

    unpack_hash_table_or_code = None(unpack_hash_table_or_code)
    
    def pack_hash_table_or_code(self = None):
        pass

    pack_hash_table_or_code = None(pack_hash_table_or_code)
    
    def pack_encryption_parameters(self = None):
        pass

    pack_encryption_parameters = None(pack_encryption_parameters)
    
    def sanitize_certificate_chain(certificate_chain = None, mrc_index = None):
        mrc_3_0_roots = None
        if use_mrc_3_0(len(certificate_chain[ROOT])):
            mrc_3_0_roots = get_mrc_3_0_root_certificates(certificate_chain[ROOT], mrc_index)
        return (lambda .0 = None: for level, certificates in .0:
passcontinue(lambda .0: [ memoryview(certificate) for certificate in .0 ])[mrc_3_0_roots(certificates)]
)(enumerate(certificate_chain))

    sanitize_certificate_chain = None(sanitize_certificate_chain)
    
    def uses_mrc_3_0(self = None):
        root_certificates = self.oem_certificate_chain_list[ROOT]
        inactive_mrc_3_0_count = sum((lambda .0: for certificate in .0:
is_inactive_mrc_3_0_certificate(get_certificate_sequence_size(certificate)))(root_certificates))
        return inactive_mrc_3_0_count == len(root_certificates) - 1

    uses_mrc_3_0 = None(uses_mrc_3_0)
    
    def get_details_hash_table_or_code(self = None, authority = None, details = abstractmethod):
        pass

    get_details_hash_table_or_code = None(get_details_hash_table_or_code)
    
    def hash_segment_type(cls):
        pass

    hash_segment_type = classmethod(abstractmethod(hash_segment_type))
    
    def repr_hash_table_hashes(self = None):
        pass

    repr_hash_table_hashes = None(repr_hash_table_hashes)
    
    def repr_encryption_parameters(self = None):
        pass

    repr_encryption_parameters = None(repr_encryption_parameters)
    
    def repr_hash_table_algorithm(self = None):
        pass

    repr_hash_table_algorithm = None(repr_hash_table_algorithm)
    
    def add_one_shot_hash_phdr(self = None):
        raise RuntimeError(f'''Cannot add a one-shot hash to {a_or_an(self.image_type_string())} {self.image_type_string()}.''')

    
    def contains_one_shot_hash(self = None):
        return False

    
    def get_number_of_hashable_entries(self = None):
        return 0

    
    def get_segment_hash_algorithm(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def validate_before_operation(self = None, **kwargs):
        pass
    # WARNING: Decompyle incomplete

    
    def pack(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_root_certificate_hash(self = None, authority = None, hash_algorithm = None):
        root_certificate_hash = None
        if authority not in (AUTHORITY_QTI, AUTHORITY_OEM):
            raise RuntimeError(f'''Cannot get Root Certificate Hash for unknown authority: {authority}.''')
        if None not in SHA_DESCRIPTION_TO_FUNCTION:
            raise RuntimeError(f'''Cannot get Root Certificate Hash for unknown hash algorithm: {hash_algorithm}.''')
        root_certificates = None
        if authority == AUTHORITY_QTI and self.qti_certificate_chain_list:
            root_certificates = self.qti_certificate_chain_list[ROOT]
        elif authority == AUTHORITY_OEM and self.oem_certificate_chain_list:
            root_certificates = self.oem_certificate_chain_list[ROOT]
    # WARNING: Decompyle incomplete

    
    def include_qbec_encryption_parameters(self = None, authority = None):
        '''
        Include QBEC Encryption Parameters in the OEM data to sign when:
        1. The QBEC Encryption Parameters contain a v2 Header
            and
        2. The encryption_order in ENCRYPTED-THEN-SIGNED

        Include QBEC Encryption Parameters in the QTI data to sign when:
        1. The encrypting_entity of the Encryption Parameters is QTI (regardless of a V1 or V2 QBEC Header)
            and
        2. The encryption_order is ENCRYPTED-THEN-SIGNED (For QTI, there is no change in the order)
        '''
        if isinstance(self.encryption_parameters, QBECEncryptionParametersCommon) and self.encryption_parameters.header:
            if self.encryption_parameters.header.version == QBEC_VERSION_2 and self.encryption_parameters.header.encryption_order == ENCRYPTED_THEN_SIGNED:
                if authority == authority:
                    pass
                elif (authority == AUTHORITY_QTI or authority == AUTHORITY_OEM) and self.encryption_parameters.header.version == QBEC_VERSION_1:
                    if authority == authority:
                        return authority == AUTHORITY_QTI
                    authority == authority
        return authority

    
    def get_data_to_sign(self = None, authority = None):
        if authority not in (AUTHORITY_QTI, AUTHORITY_OEM):
            raise RuntimeError(f'''Cannot get data to sign for unknown authority: {authority}.''')
        data = None()
    # WARNING: Decompyle incomplete

    
    def get_details(self = None, authority = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_name_according_to_header_version_for_dump(self = None, name = None):
        if self.header.version == HASH_SEGMENT_V8:
            return f'''{name}_1'''

    
    def get_dump_files(self = None, directory = None):
        pass
    # WARNING: Decompyle incomplete

    
    def _repr_signature(self = None, authority = None, certificate_chain_text = None):
        string = ''
        signature = self.qti_signature if authority == AUTHORITY_QTI else self.oem_signature
        if signature and any((lambda .0: for certificates in .0:
for certificate in certificates:
certificate)(certificate_chain_text)):
            string += f'''\n\n{authority} Signature Properties:\n'''
            r_and_s = extract_r_and_s_from_signature(bytes(signature))
            signature_information = extract_signature_format(certificate_chain_text[ATTESTATION][0])
            signature_properties = get_signature_properties(r_and_s, signature_information)
            if signature_properties:
                string += properties_repr(signature_properties)
        return string

    
    def _repr_certificate_chain(self = None, authority = None, certificate_chain_text = None):
        string = ''
        rch_algorithm_mismatch_string = ''
        inactive_rch_algorithm = None
        certificate_chain = self.qti_certificate_chain_list if authority == AUTHORITY_QTI else self.oem_certificate_chain_list
    # WARNING: Decompyle incomplete

    
    def __repr__(self = None):
        properties = []
        string = ''
        qti_certificate_chain_text = [
            [],
            [],
            []]
        oem_certificate_chain_text = [
            [],
            [],
            []]
    # WARNING: Decompyle incomplete

    
    def get_size(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def recompute_image_size(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_largest_metadata_class():
        pass
    # WARNING: Decompyle incomplete

    get_largest_metadata_class = None(get_largest_metadata_class)
    
    def reserve_padding_for_metadata_and_signing_assets(self, authority, current_operation = None, number_of_certificates = None, number_of_root_certificates = None, signature_algorithm = ('authority', str, 'current_operation', str, 'number_of_certificates', int, 'number_of_root_certificates', int, 'signature_algorithm', SignatureDescription | None, 'return', None)):
        pass
    # WARNING: Decompyle incomplete

    
    def reserve_padding_for_size_alignment(self = None, alignment = None):
        current_size = HashTableSegmentCommon.get_size(self)
        added_padding_size = ceil_to_multiple(current_size, alignment) - current_size
        log_debug(f'''Adding {added_padding_size} bytes of padding for Hash Table Segment size alignment of {alignment}.''')
        self.padding = memoryview(bytearray(self.padding) + PAD_BYTE_1 * added_padding_size)

    
    def reserve_padding_for_encryption_parameters(self = None, consider_other_authority = None):
        pass

    
    def recompute_padding_size(self = None, authority = None, existing_signing_assets_size = None):
        pass

    
    def set_hash_table_algorithm(self = None, segment_hash_algorithm = None):
        pass

    
    def validate_existing_hash_table_algorithm(self = None, segment_hash_algorithm = None):
        pass

    
    def recompute_hash_table(self = None, segment_hash_algorithm = None, authority = None):
        pass

    
    def recompute_hash_table_size(self = None, segment_hash_algorithm = None):
        pass

    
    def update_hash_table_segment_phdr(self = None):
        pass

    
    def add_phdr_for_elf_header_and_program_header_table(self = None):
        pass

    
    def update_phdr_table_offset(self = None, authority = None):
        pass

    
    def remove_hash_table_segment(self = None):
        pass

    
    def add_hash_table_segment(self = None):
        pass

    
    def remove_sections(self = None):
        pass

    
    def remove_one_shot_hash_segment(self = None):
        pass

    
    def prep_for_encrypt(self, authority, current_operation = None, operations = None, device_restrictions = None, preexisting_hash_table_segment = (False,), second_authority_operating = ('authority', str, 'current_operation', str, 'operations', list[str], 'device_restrictions', BaseDeviceRestrictions, 'preexisting_hash_table_segment', bool, 'second_authority_operating', bool, 'return', None)):
        pass

    
    def get_max_encryption_parameters_size(self = None, _ = None):
        return 0

    
    def is_qbec_2_0_encrypted(self = None):
        return False

    
    def is_unsigned(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def is_oem_exclusive_signed(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def is_qti_exclusive_signed(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def is_qti_signed_double_signable(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def is_oem_signed_double_signable(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def is_double_signed(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def is_oem_signed(self = None):
        if not self.is_oem_exclusive_signed() and self.is_oem_signed_double_signable():
            pass
        return self.is_double_signed()

    
    def is_qti_signed(self = None):
        if not self.is_qti_exclusive_signed() and self.is_qti_signed_double_signable():
            pass
        return self.is_double_signed()

    
    def is_signed(self = None, authority = None):
        if authority == AUTHORITY_OEM:
            return self.is_oem_signed()
        return None.is_qti_signed()

    
    def is_signed_by_other_authority(self = None, authority = None):
        if authority == AUTHORITY_QTI:
            return self.is_oem_signed()
        return None.is_qti_signed()

    
    def set_metadata_values(metadata = None, device_restrictions = None):
        pass
    # WARNING: Decompyle incomplete

    set_metadata_values = None(set_metadata_values)
    
    def get_metadata_given_size(metadata_size = None, authority = None):
        '''Returns the highest metadata version class that fits the reserved metadata_size.'''
        metadata = None
    # WARNING: Decompyle incomplete

    get_metadata_given_size = None(get_metadata_given_size)
    
    def set_authority_specific_metadata(self, authority = None, current_operation = None, device_restrictions = None, preexisting_hash_table_segment = (None,), existing_metadata = ('authority', str, 'current_operation', str, 'device_restrictions', BaseDeviceRestrictions, 'preexisting_hash_table_segment', bool, 'existing_metadata', Metadata | None, 'return', None)):
        pass
    # WARNING: Decompyle incomplete

    
    def set_hash_table_segment_header_values(self, authority, current_operation, device_restrictions, number_of_certificates, number_of_root_certificates, signature_algorithm = None, preexisting_hash_table_segment = None, existing_signing_assets_size = None, is_second_authority = (0, False, None), segment_hash_algorithm = ('authority', str, 'current_operation', str, 'device_restrictions', BaseDeviceRestrictions, 'number_of_certificates', int, 'number_of_root_certificates', int, 'signature_algorithm', SignatureDescription | None, 'preexisting_hash_table_segment', bool, 'existing_signing_assets_size', int, 'is_second_authority', bool, 'segment_hash_algorithm', str | None, 'return', None)):
        if authority == AUTHORITY_OEM and self.oem_signature:
            self.oem_signature = memoryview(bytearray())
            self.oem_certificate_chain = memoryview(bytearray())
            self.oem_certificate_chain_list = []
        if authority == AUTHORITY_QTI and self.qti_signature:
            self.qti_signature = memoryview(bytearray())
            self.qti_certificate_chain = memoryview(bytearray())
            self.qti_certificate_chain_list = []
        (signature_size, certificate_chain_size) = get_max_signature_and_certificate_chain_size(current_operation, number_of_certificates, number_of_root_certificates, signature_algorithm)
        if is_second_authority and isinstance(self.header, MBNHeader) and len(self.padding) + existing_signing_assets_size < signature_size + certificate_chain_size:
            certificate_chain_size = max(len(self.padding) + existing_signing_assets_size - signature_size, 0)
    # WARNING: Decompyle incomplete

    
    def prep_for_first_authority_operation(self, authority, current_operation, operations, device_restrictions, number_of_certificates = None, number_of_root_certificates = None, signature_algorithm = None, preexisting_hash_table_segment = ('authority', str, 'current_operation', str, 'operations', list[str], 'device_restrictions', BaseDeviceRestrictions, 'number_of_certificates', int, 'number_of_root_certificates', int, 'signature_algorithm', SignatureDescription | None, 'preexisting_hash_table_segment', bool, 'return', None)):
        pass
    # WARNING: Decompyle incomplete

    
    def prep_for_second_authority_operation(self, authority, current_operation, operations, signature_size, certificate_chain_size, device_restrictions, number_of_certificates = None, number_of_root_certificates = None, signature_algorithm = None, preexisting_hash_table_segment = ('authority', str, 'current_operation', str, 'operations', list[str], 'signature_size', int, 'certificate_chain_size', int, 'device_restrictions', BaseDeviceRestrictions, 'number_of_certificates', int, 'number_of_root_certificates', int, 'signature_algorithm', SignatureDescription | None, 'preexisting_hash_table_segment', bool, 'return', None)):
        self.validate_existing_hash_table_algorithm(device_restrictions.segment_hash_algorithm)
        if current_operation in (HASH, SIGN):
            self.set_hash_table_segment_header_values(authority, current_operation, device_restrictions, number_of_certificates, number_of_root_certificates, signature_algorithm, preexisting_hash_table_segment, signature_size + certificate_chain_size, True)
            self.recompute_padding_size(authority, signature_size + certificate_chain_size)
        if not ENCRYPT in operations or self.image_prepped_for_encryption:
            self.prep_for_encrypt(authority, current_operation, operations, device_restrictions, preexisting_hash_table_segment, True, **('second_authority_operating',))
            self.image_prepped_for_encryption = True
            return None
        return None

    
    def prep_for_operation(self, authority, current_operation, operations, device_restrictions = None, preexisting_hash_table_segment = None, number_of_certificates = None, signature_algorithm = (0, None, 0), number_of_root_certificates = ('authority', str, 'current_operation', str, 'operations', list[str], 'device_restrictions', BaseDeviceRestrictions, 'preexisting_hash_table_segment', bool, 'number_of_certificates', int, 'signature_algorithm', SignatureDescription | None, 'number_of_root_certificates', int, 'return', None)):
        pass
    # WARNING: Decompyle incomplete

    
    def get_metadata_version(self = None, authority = None):
        metadata_version_str = None
        common_metadata_version_str = None
    # WARNING: Decompyle incomplete

    
    def validate_number_of_root_certificates(self = None, number_of_root_certificates = None, authority = None, mrc_index = ('number_of_root_certificates', int, 'authority', str, 'mrc_index', int | None, 'return', None)):
        pass
    # WARNING: Decompyle incomplete

    
    def _get_errors_table(self = None, security_profile = None, path = None):
        errors_table = []
        log_debug(f'''Validating SoC HW Version bindings of {path}.''')
    # WARNING: Decompyle incomplete

    
    def get_security_profile_mismatch_str(self = None, security_profile = None, path = None):
        errors_table = self._get_errors_table(security_profile, path)
        if errors_table:
            return 'The following values mismatch in validation against Security Profile.\n' + make_value_comparison_table(errors_table)

    
    def prep_for_zi_segment_hash(self = None):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None

