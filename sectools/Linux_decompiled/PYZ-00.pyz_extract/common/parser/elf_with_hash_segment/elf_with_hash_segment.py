
from contextlib import suppress
from math import ceil
from typing import Any, Type
import profile
from cmd_line_interface.sectools.cmd_line_common.defines import HASH, INFILE, SEGMENT_HASH_ALGORITHM, SIGN
from cmd_line_interface.sectools.secure_image.defines import ENCRYPT
from common.crypto.openssl.defines import ALGORITHM_ECDSA_USER_FACING, ALGORITHM_RSA_USER_FACING, SHA_DESCRIPTION_TO_CERTIFICATE_HASH_SIZE, SIGNATURE_DESCRIPTION_TO_SIZE, SignatureDescription
from common.crypto.openssl.openssl import get_curve_name_without_rs_48_49
from common.data.base_parser import BaseParserGenerator, BaseParserTransformer
from common.data.data import ceil_to_multiple, get_lsb, version_string_to_tuple
from common.data.defines import ONE_SHOT_DESCRIPTION_FROM_COMMON_METADATA_DESCRIPTION, ONE_SHOT_HASH_ALGORITHMS, PAD_BYTE_0, PAD_BYTE_1, SHA_DESCRIPTION_TO_FUNCTION, SHA_DESCRIPTION_TO_SIZE, ZI_HASH_ALGORITHMS
from common.logging.logger import log_debug
from common.parser.elf.bit32.program_header import ProgramHeader32
from common.parser.elf.bit64.program_header import ProgramHeader64
from common.parser.elf.defines import ELFCLASS32, ELF_BLOCK_SIZE, PT_NULL, PT_ONE_SHOT_HASH, P_FLAGS_OS_PAGED_SEGMENT, P_FLAGS_OS_SEGMENT_TYPE_MASK
from common.parser.elf.elf import ClusterLimits, ELF, PILSplitImage
from common.parser.elf.positional_data import AbstractPositionalData, PositionalData
from common.parser.elf.program_header import PROGRAM_HEADER_CLASSES
from common.parser.elf_with_hash_segment.defines import P_FLAGS_OS_SEGMENT_PHDR
from common.parser.elf_with_hash_segment.hash_table_segment_header import HashTableSegmentHeaderCommon
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.defines import AES_128_XTS, ENCRYPTED_THEN_SIGNED, ENCRYPTING_ENTITY_DESCRIPTION, XTS_BLOCK_SIZE
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec import QBECEncryptionParametersCommon
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec_block_encryption_parameters import QBECBlockEncryptionParameters
from common.parser.elf_with_hash_segment.qbec_encryption_parameters.qbec_segment_encryption_parameters import QBECSegmentEncryptionParameters
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.defines import EPS_MINOR_VERSION_0
from common.parser.elf_with_hash_segment.uie_encryption_parameters.section_header.v1_0.defines import KEY_PAYLOAD_SIZE
from common.parser.elf_with_hash_segment.uie_encryption_parameters.uie_encryption_parameters import UIEEncryptionParameters
from common.parser.elf_with_hash_segment.v3.hash_table_segment_header import HashTableSegmentHeaderV3
from common.parser.elf_with_hash_segment.v6.hash_table_segment_header import HashTableSegmentHeaderV6
from common.parser.elf_with_hash_segment.v7.defines import SHA_DESCRIPTION_TO_ALGO
from common.parser.elf_with_hash_segment.v7.hash_table_segment_header import HashTableSegmentHeaderV7
from common.parser.hash_segment.defines import AUTHORITY_OEM, AUTHORITY_QTI, HASH_SEGMENT_V3, HASH_SEGMENT_V6, HASH_SEGMENT_V7, MRC_1_0, MRC_2_0, MRC_3_0
from common.parser.hash_segment.hash_segment_common import HashTableSegmentCommon
from common.parser.hash_segment.hash_segment_utils import get_max_signature_and_certificate_chain_size
from common.parser.mdt_with_hash_segment.mdt_with_hash_segment import MDTWithHashTableSegment
from common.parser.parser_image_info_interface import HASH_TABLE_SEGMENT_PROPERTIES, ImageProperties
from core.base_device_restrictions import BaseDeviceRestrictions
from core.profile_validator.defines import QBEC, UIE
from profile.defines import END, START, UNKNOWN
from profile.schema import EncryptionFeatures, HashTableSegmentProperties, SigningFeatures

class ELFWithHashTableSegment(ELF, MDTWithHashTableSegment, BaseParserTransformer):
    
    def create_default(self = None, *, elf_class, hash_table_segment_version, hash_table_segment_address, common_metadata_version, **_):
        ELF.create_default(self, elf_class, **('elf_class',))
        self.create_default_hash_table_segment(hash_table_segment_version, hash_table_segment_address, common_metadata_version)

    
    def complete_default_hash_table(self = None, *_):
        pass
    # WARNING: Decompyle incomplete

    
    def transform(self = None, persist_sections = None, hash_table_segment_version = None, hash_table_segment_address = (True, HASH_SEGMENT_V3, 0, None), common_metadata_version = ('persist_sections', bool, 'hash_table_segment_version', int, 'hash_table_segment_address', int, 'common_metadata_version', tuple[(int, int)] | None, 'return', None), **_):
        if not persist_sections:
            self.remove_sections()
        self.remove_elf_hdr_phdr_table_overlaps()
        self.create_default_hash_table_segment(hash_table_segment_version, hash_table_segment_address, common_metadata_version)

    
    def transformable_parsers(cls = None):
        return [
            ELF]

    transformable_parsers = None(transformable_parsers)
    
    def get_hash_table_segment_data(self = None, _ = None):
        if not self.phdrs:
            raise self.ExceptionNeedsTransform('ELF does not contain any segments')
        if not None.hash_table_segment_phdr:
            raise self.ExceptionNeedsTransform(f'''ELF does not contain a {self.hash_segment_type()}.''')
        return None.segments[self.hash_table_segment_phdr]

    
    def get_greatest_offset(self = None):
        return ELF.get_greatest_offset(self)

    
    def get_segment_hash_algorithm(self = None):
        hash_algorithm = super().get_segment_hash_algorithm()
        if hash_algorithm and self.contains_one_shot_hash():
            return ONE_SHOT_DESCRIPTION_FROM_COMMON_METADATA_DESCRIPTION[hash_algorithm]

    
    def contains_one_shot_hash(self = None):
        return self.one_shot_hash_phdr is not None

    
    def remove_one_shot_hash_segment(self = None):
        if self.one_shot_hash_phdr:
            self.remove_segment(self.one_shot_hash_phdr)
        self.one_shot_hash_phdr = None

    
    def validate_before_operation(self = None, validate_sections = None, is_second_authority = None, **_):
        super().validate_before_operation(validate_sections, is_second_authority, **('validate_sections', 'is_second_authority'))
        HashTableSegmentCommon.validate_before_operation(self)
        if self.padding and self.padding != len(self.padding) * PAD_BYTE_1:
            raise RuntimeError(f'''Padding at end of {self.hash_segment_type()} contains invalid data.''')
        os_segment_hash = None
        os_segment_phdr = None
        one_shot_phdr = None
        for phdr in self.phdrs:
            if phdr.is_os_segment_hash():
                if os_segment_hash:
                    raise RuntimeError(f'''An ELF image must contain only one {self.hash_segment_type()}.''')
                os_segment_hash = None
            if phdr.is_os_segment_phdr():
                if os_segment_phdr:
                    raise RuntimeError('An ELF image must contain only one Segment encapsulating the ELF Header and Program Header Table.')
                os_segment_phdr = None
            if phdr.p_type == PT_ONE_SHOT_HASH:
                if one_shot_phdr:
                    raise RuntimeError('An ELF image must contain only one One-Shot Hash Entry.')
                one_shot_phdr = None

    
    def overlapping_data_mismatches(self = None, phdr = None, other_phdr = None):
        pass
    # WARNING: Decompyle incomplete

    
    def data_overlaps_and_mismatches(self = None, phdr = None, other_phdr = None):
        data_mismatches = False
        if phdr.end_address <= phdr.end_address or phdr.end_address <= other_phdr.end_address:
            pass
        else:
            other_phdr.address
        data_mismatches = self.overlapping_data_mismatches(other_phdr, phdr)
        return data_mismatches
        if other_phdr.end_address <= other_phdr.end_address or other_phdr.end_address <= phdr.end_address:
            pass
        else:
            phdr.address
            return data_mismatches
        data_mismatches = phdr.address.overlapping_data_mismatches(phdr, other_phdr)
        return data_mismatches

    
    def is_type(cls = None, data = None):
        ''' Detect whether the data is of an ELF With Hash Segment image. '''
        match = False
    # WARNING: Decompyle incomplete

    is_type = None(is_type)
    
    def update_hash_table_segment(self = None):
        hash_table_segment_data = HashTableSegmentCommon.pack(self)
    # WARNING: Decompyle incomplete

    
    def pack(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def supports_multi_image(self = None):
        return True

    
    def get_signing_assets_size_for_authority(signing_features = None):
        max_total_size = 0
        for signature_format in signing_features.signature_formats.signature_format:
            format_certificate_size = 0
            format_signature_size = 0
            if signature_format.signature_algorithm == ALGORITHM_RSA_USER_FACING:
                key_sizes_or_curves = signature_format.key_sizes.supported_key_sizes.value
            elif signature_format.signature_algorithm == ALGORITHM_ECDSA_USER_FACING:
                key_sizes_or_curves = (lambda .0: [ get_curve_name_without_rs_48_49(curve) for curve in .0 ])(signature_format.ecdsa_curves.supported_ecdsa_curves.value)
            else:
                key_sizes_or_curves = [
                    None]
            for key_size_or_curve in key_sizes_or_curves:
                (signing_features_signature_size, signing_features_certificate_size, _) = SIGNATURE_DESCRIPTION_TO_SIZE[SignatureDescription(signature_format.signature_algorithm, key_size_or_curve)]
                format_signature_size = max(format_signature_size, signing_features_signature_size)
                format_certificate_size = max(format_certificate_size, signing_features_certificate_size)
            format_root_certificates_size = format_certificate_size
            if signing_features.mrc_specs:
                number_of_roots = signing_features.mrc_specs.max_root_certificate_count
                mrc_spec = signing_features.mrc_specs.default_mrc_spec
                if mrc_spec == MRC_3_0:
                    max_hash_size = max((lambda .0: for hash_algorithm in .0:
SHA_DESCRIPTION_TO_CERTIFICATE_HASH_SIZE[hash_algorithm])(signing_features.root_certificate_hash_algorithms.supported_root_certificate_hash_algorithms.value))
                    roots_size = format_certificate_size + (number_of_roots - 1) * max_hash_size
                elif mrc_spec in (MRC_1_0, MRC_2_0):
                    roots_size = number_of_roots * format_certificate_size
                else:
                    raise RuntimeError(f'''Unrecognized MRC version: {mrc_spec}, could not determine the size of signing assets.''')
                format_root_certificates_size = None(format_root_certificates_size, roots_size)
            format_number_of_non_root_certificates = 1
            if signature_format.certificate_chain_depths_override:
                depths = signature_format.certificate_chain_depths_override.supported_certificate_chain_depths.value
            else:
                depths = signing_features.certificate_chain_depths.supported_certificate_chain_depths.value
            for depth in depths:
                format_number_of_non_root_certificates = max(format_number_of_non_root_certificates, depth - 1)
            max_format_size = format_signature_size + format_root_certificates_size + format_number_of_non_root_certificates * format_certificate_size
            max_total_size = max(max_format_size, max_total_size)
        return max_total_size

    get_signing_assets_size_for_authority = None(get_signing_assets_size_for_authority)
    
    def reserve_padding_for_metadata_and_signing_assets(self = None, authority = None, current_operation = None, number_of_certificates = None, number_of_root_certificates = None, signature_algorithm = None):
        super().reserve_padding_for_metadata_and_signing_assets(authority, current_operation, number_of_certificates, number_of_root_certificates, signature_algorithm)
    # WARNING: Decompyle incomplete

    
    def reserve_padding_for_encryption_parameters(self = None, consider_other_authority = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_max_encryption_parameters_size(self = None, encryption_features = None):
        max_encryption_spec_size = 0
        if encryption_features:
            for encryption_format in encryption_features.supported_encryption_formats.encryption_format:
                if encryption_format.encryption_type == UIE:
                    for encryption_spec in encryption_format.encryption_specs.supported_encryption_specs.value:
                        (eps_major_version, l2_ad_major_version, l2_ad_minor_version) = extract_encryption_spec_versions(encryption_spec)
                        max_encryption_spec_size = max(max_encryption_spec_size, UIEEncryptionParameters.get_encryption_spec_size(eps_major_version, EPS_MINOR_VERSION_0, l2_ad_major_version, l2_ad_minor_version))
                    continue
                key_management_scheme = encryption_format.key_management_scheme.valueOf_
                data_encryption_scheme = encryption_format.data_encryption_scheme
                if encryption_format.public_keys:
                    pass
                elif not encryption_format.max_num_public_keys:
                    pass
                num_public_keys = 0
                max_encryption_spec_size = max(max_encryption_spec_size, QBECEncryptionParametersCommon.get_encryption_spec_size(encryption_format.version, key_management_scheme, data_encryption_scheme, num_public_keys, self.phdrs))
        return max_encryption_spec_size

    
    def recompute_padding_size(self = None, authority = None, existing_signing_assets_size = None):
        pass
    # WARNING: Decompyle incomplete

    
    def include_padding_in_cluster(self = None, positional_entry = None):
        if isinstance(self.encryption_parameters, QBECBlockEncryptionParameters):
            pass
        return positional_entry in self.get_qbec_block_encryptable_entries()

    
    def entry_should_go_into_existing_cluster(self = None, cluster_limit = None, cluster = None, positional_entry = None):
        add_entry = super().entry_should_go_into_existing_cluster(cluster_limit, cluster, positional_entry)
        if isinstance(self.encryption_parameters, QBECBlockEncryptionParameters):
            encrypted_entries = self.get_qbec_block_encryptable_entries()
            if add_entry and positional_entry.offset == cluster_limit.end + 1 and positional_entry in encrypted_entries:
                pass
            add_entry = cluster[-1] in encrypted_entries
        return add_entry

    
    def wipe_paddings(self):
        if isinstance(self.encryption_parameters, QBECBlockEncryptionParameters):
            entries_to_encrypt = self.get_qbec_block_encryptable_entries()
            for padding_positional_entry in list(self.paddings.keys()):
                if padding_positional_entry not in entries_to_encrypt:
                    del self.paddings[padding_positional_entry]
            return None
        self.paddings = None

    
    def set_hash_table_algorithm(self = None, segment_hash_algorithm = None):
        pass
    # WARNING: Decompyle incomplete

    
    def validate_existing_hash_table_algorithm(self = None, segment_hash_algorithm = None):
        if segment_hash_algorithm or image_algorithm = self.get_segment_hash_algorithm() != segment_hash_algorithm:
            raise RuntimeError(f'''Cannot use {SEGMENT_HASH_ALGORITHM} {segment_hash_algorithm} because {INFILE} was previously operated on with {image_algorithm}.''')
        return self.get_segment_hash_algorithm()

    
    def recompute_hash_table(self = None, segment_hash_algorithm = None, authority = None, include_encrypted_data = (False,)):
        security_profile = profile.SECURITY_PROFILE
    # WARNING: Decompyle incomplete

    
    def recompute_hash_table_size(self = None, segment_hash_algorithm = None):
        pass
    # WARNING: Decompyle incomplete

    
    def update_hash_table_segment_phdr(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def add_phdr_for_elf_header_and_program_header_table(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def shift_phdr_table(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def update_phdr_table_offset(self = None, authority = None):
        if not self.is_signed_by_other_authority(authority):
            self.shift_phdr_table()
            return None

    
    def remove_hash_table_segment(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def add_hash_table_segment(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_segment_placement(self = None, phdr = None):
        placement = []
        if self.phdrs[0] == phdr or all((lambda .0: for preceding_phdr in .0:
if not preceding_phdr.is_os_segment_phdr():
passpreceding_phdr.is_os_segment_hash())(self.phdrs[:self.phdrs.index(phdr)])):
            placement.append(START)
        if (self.phdrs[-1] == phdr or len(self.phdrs) > 1) and self.phdrs[-2] == phdr and self.phdrs[-1].is_os_segment_hash():
            placement.append(END)
        if not placement:
            placement.append(UNKNOWN)
        return placement

    
    def get_image_properties(self = None, authority = None):
        if bool(self.hash_table_hashes):
            pass
        hash_pages = len(self.phdrs) != len(self.hash_table_hashes)
        (metadata_version, common_metadata_version) = self.get_metadata_version(authority)
    # WARNING: Decompyle incomplete

    
    def get_phdrs_of_segments_to_encrypt(self = None, encryptable_indices = None):
        return (lambda .0 = None: [ self.phdrs[idx] for idx in .0 ])(encryptable_indices)

    
    def prep_for_encrypt(self, authority, current_operation = None, operations = None, device_restrictions = None, preexisting_hash_table_segment = (False,), second_authority_operating = ('authority', str, 'current_operation', str, 'operations', list[str], 'device_restrictions', BaseDeviceRestrictions, 'preexisting_hash_table_segment', bool, 'second_authority_operating', bool, 'return', None)):
        pass
    # WARNING: Decompyle incomplete

    
    def prep_for_uie_encryption(self = None, authority = None, operations = None, second_authority_operating = ('authority', str, 'operations', list[str], 'second_authority_operating', bool, 'return', None)):
        for idx, phdr in enumerate(self.phdrs):
            if phdr.is_uie_encryptable and len(self.segments[phdr]) < KEY_PAYLOAD_SIZE:
                if not (second_authority_operating or self.is_unsigned()) and SIGN in operations:
                    raise RuntimeError(f'''Cannot {authority} encrypt a signed image with segments shorter than {KEY_PAYLOAD_SIZE} bytes. Problematic segment\'s Program Header is at index {idx}.''')
                for positional_entry in None.get_positional_entries():
                    if phdr != positional_entry and phdr.overlaps_with(positional_entry):
                        raise RuntimeError(f'''Cannot encrypt an image with LOAD segments shorter than {KEY_PAYLOAD_SIZE} bytes that also overlap with other regions of the image. {phdr} overlaps with {positional_entry}.''')
                    log_debug(f'''Padding {phdr} so that it is {KEY_PAYLOAD_SIZE} bytes.''')
                    self.pad_segment(phdr, KEY_PAYLOAD_SIZE)
                    return None

    
    def prep_for_xts_encryption(self = None):
        entries_to_encrypt = self.get_qbec_block_encryptable_entries()
        data_length = len(self.get_data_from_entries(entries_to_encrypt))
        last_phdr = self.get_last_entry(entries_to_encrypt)
    # WARNING: Decompyle incomplete

    
    def pad_segment(self = None, phdr = None, size = None):
        original_filesz = phdr.size
        phdr.size = size
        padding_data = bytearray()
        if phdr.p_memsz < size:
            phdr.p_memsz = size
            for other_phdr in self.phdrs:
                if phdr != other_phdr and other_phdr.size and phdr.overlaps_in_memory_with(other_phdr):
                    overlap_size = (phdr.end_address - other_phdr.address) + 1
                    void_size = size - original_filesz + overlap_size
                    padding_data = PAD_BYTE_0 * void_size + self.segments[other_phdr][:overlap_size]
                    if overlap_size > other_phdr.size:
                        raise RuntimeError(f'''Cannot encrypt {INFILE} as data is shorter than expected.''')
                    if padding_data:
                        self.segments[phdr] = memoryview(bytearray(self.segments[phdr]) + bytearray(padding_data))
                    else:
                        self.segments[phdr] = memoryview(bytearray(self.segments[phdr]).ljust(size, PAD_BYTE_0))
        self.flatten_segment(phdr)

    
    def set_encryption_parameters(self = None, encryption_parameters = None):
        self.encryption_parameters = encryption_parameters
    # WARNING: Decompyle incomplete

    
    def pil_split(self = None):
        pil_image = super().pil_split()
        log_debug(f'''Adding {self.hash_segment_type()} data to mdt data.''')
        self.update_hash_table_segment()
    # WARNING: Decompyle incomplete

    
    def add_one_shot_hash_phdr(self = None):
        pass
    # WARNING: Decompyle incomplete

    __classcell__ = None


def extract_encryption_spec_versions(encryption_spec = None):
    (_, eps_version, _, l2_version) = encryption_spec.split('-')
    (eps_major_version, _) = version_string_to_tuple(eps_version)
    (l2_ad_major_version, l2_ad_minor_version) = version_string_to_tuple(l2_version)
    return (eps_major_version, l2_ad_major_version, l2_ad_minor_version)


def performing_sign_or_hash(operations = None):
    if not SIGN in operations:
        pass
    return HASH in operations

