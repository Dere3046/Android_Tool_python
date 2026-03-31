
from typing import Iterable
from lxml import etree
from lxml.etree import XMLSyntaxError
from cmd_line_interface.sectools.cmd_line_common.defines import IMAGE_ID, INFILE, SECURITY_PROFILE, SEGMENT_HASH_ALGORITHM
from cmd_line_interface.sectools.fuseblower.defines import FUSE_BLOWER_NAME
from cmd_line_interface.sectools.secure_debug.defines import SECURE_DEBUG_NAME
from cmd_line_interface.sectools.secure_image.defines import COMPRESS, VOUCH_FOR
from common.crypto.openssl.defines import ALGORITHM_ECDSA_USER_FACING, RS_48_49
from common.data.data import and_separated, numbered_string
from common.logging.logger import log_debug
from common.parser.hash_segment.defines import AUTHORITY_OEM, AUTHORITY_QTI
from common.parser.parser_image_info_interface import ImageFormatType
from core.profile_validator.validate import validate_security_profile
from profile.defines import ANY, JTAG_IDS, PRODUCT_SEGMENT_IDS, SCHEMA_STRUCTURE, SCHEMA_VERSIONS, SOC_FEATURE_IDS, SOC_HW_VERSIONS
from profile.profile_flatten import flatten_security_profile
from profile.profile_resolve import resolve_authenticator, resolve_image_entries_from_image_list, resolve_image_format, resolve_image_formats_from_image_list, resolve_platform_bindings, resolve_tme_elf_properties
from profile.schema import Authenticator, EncryptionFeatures, EncryptionFormat, FuseBlowing, HashTableSegmentMetadataVersions, HashTableSegmentPlacements, HashTableSegmentProperties, Image, ImageFormat, LegacyDebugging, LicenseManagerSegmentProperties, MBNMetadataVersions, MBNProperties, MRCSpecs, ProcessedProfile, Profile, SecDatProperties, SecELFProperties, SegmentHashAlgorithms, SignatureFormat, SigningFeatures, TMEDebugging, VouchSegmentPlacements, VouchSegmentProperties, licenseManagerSegmentPlacements
from profile.schema.scale_profile import upscale_security_profile
from profile.utils import compare_authentication_image_format, compare_fuse_blowing_format, compare_legacy_debugging_format, filter_elements, get_ids_for_format, verify_profile_elements

class SecurityProfile:
    
    def __init__(self = None, security_profiles = None):
        self.images = []
        self.authenticators = []
        self.image_format = None
        self.target_image_format = None
        self.signing_features = None
        self.other_authority_signing_features = None
        self.default_signature_format_id = ''
        self.signature_format = None
        self.other_authority_signature_format = None
        self.encryption_features = None
        self.other_authority_encryption_features = None
        self.encryption_format = None
        self.other_authority_encryption_format = None
        self.legacy_debugging_features = None
        self.tme_debugging_features = None
        self.fuse_blowing_features = None
        self.parsed_profiles = self.process_profiles(security_profiles)
        self.platform_bindings = resolve_platform_bindings(self.parsed_profiles, SCHEMA_STRUCTURE['profile']['platform_binding_values'])

    
    def process_profiles(security_profiles = None):
        parsed_profiles = []
        for parsed_profile in security_profiles:
            if parsed_profile.authentication:
                flatten_security_profile(parsed_profile)
            parsed_profile = upscale_security_profile(parsed_profile, max(SCHEMA_VERSIONS))
            validate_security_profile(parsed_profile)
            parsed_profiles.append(parsed_profile)
        return parsed_profiles

    process_profiles = None(process_profiles)
    
    def set_signing_features_and_signature_format(self = None, authority = None, signature_format_id = None):
        pass
    # WARNING: Decompyle incomplete

    
    def set_encryption_features_and_encryption_format(self = None, authority = None, encryption_format_id = None):
        pass
    # WARNING: Decompyle incomplete

    
    def set_debugging_features(self = None, image_ids = None, authority = None):
        schema_member = SCHEMA_STRUCTURE['profile']['debugging']
        self.legacy_debugging_features = self.parsed_profiles[0].debugging.legacy
        self.tme_debugging_features = self.parsed_profiles[0].debugging.tme
        if self.legacy_debugging_features:
            verify_profile_elements(filter_elements(vars(self.legacy_debugging_features)), schema_member['legacy'].keys(), 'debugging', 'set_debugging_features')
        if self.tme_debugging_features:
            verify_profile_elements(filter_elements(vars(self.tme_debugging_features)), schema_member['tme'].keys(), 'debugging', 'set_debugging_features')
        authenticator_id = None
        for image in self.parsed_profiles[0].authentication.image_list.image:
            if image.id == image_ids[0]:
                self.images.append(image)
                authenticator_id = image.authenticator_oem if authority == AUTHORITY_OEM else image.authenticator_qti
        if authenticator_id:
            self.set_authenticator_and_image_format(self.parsed_profiles[0], authenticator_id)
            return None

    
    def set_fuse_blowing_features(self = None, set_image_member = None):
        self.fuse_blowing_features = self.parsed_profiles[0].fuse_blowing
    # WARNING: Decompyle incomplete

    
    def set_authenticator_and_image_format(self = None, parsed_profile = None, authenticator_id = None):
        for authenticator in parsed_profile.authentication.authenticators.authenticator:
            if authenticator.id == authenticator_id:
                self.authenticators.append(authenticator)
    # WARNING: Decompyle incomplete

    
    def get_image_ids(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_supported_operations_for_image(image = None):
        supported_operations = []
        if image.compression_format:
            supported_operations.append(COMPRESS)
        return supported_operations

    get_supported_operations_for_image = None(get_supported_operations_for_image)
    
    def get_image_id_record(self = None, available_image_ids = None):
        if not available_image_ids:
            pass
        available_image_ids = self.get_image_ids()
        image_id_record_data = { }
        for parsed_profile in self.parsed_profiles:
            for image in parsed_profile.authentication.image_list.image:
                if image.id in available_image_ids:
                    supported_operations = self.get_supported_operations_for_image(image)
                    if image.id in image_id_record_data:
                        recorded_operations = image_id_record_data[image.id]['supported_operations']
                        supported_operations = list(set(recorded_operations).intersection(set(supported_operations)))
                    image_id_record_data[image.id] = {
                        'supported_operations': supported_operations }
        return dict(sorted(image_id_record_data.items()))

    
    def get_signature_format_ids(self = None):
        profile_ids = []
        for parsed_profile in self.parsed_profiles:
            parsed_profile_ids = []
            for authenticator in parsed_profile.authentication.authenticators.authenticator:
                for authority in (AUTHORITY_OEM, AUTHORITY_QTI):
                    signing_features = getattr(authenticator, f'''supported_{authority.lower()}_signing_features''')
                    if signing_features:
                        for signature_format in signing_features.signature_formats.signature_format:
                            signature_format_ids = get_ids_for_format(signature_format)
                            parsed_profile_ids.extend(signature_format_ids)
            profile_ids.append(parsed_profile_ids)
    # WARNING: Decompyle incomplete

    
    def get_segment_hash_algorithms(self = None):
        segment_hash_algorithms = []
        for parsed_profile in self.parsed_profiles:
            profile_algorithms = set()
            for authenticator in parsed_profile.authentication.authenticators.authenticator:
                for image_format in authenticator.supported_image_formats.image_format:
                    if image_format.hash_table_segment_properties is not None:
                        segment_hash_algs = image_format.hash_table_segment_properties.segment_hash_algorithms
                        profile_algorithms.update(segment_hash_algs.supported_segment_hash_algorithms.value)
            segment_hash_algorithms.append(profile_algorithms)
    # WARNING: Decompyle incomplete

    
    def get_encryption_format_ids(self = None):
        profile_ids = []
        for parsed_profile in self.parsed_profiles:
            parsed_profile_ids = []
            for authenticator in parsed_profile.authentication.authenticators.authenticator:
                for authority in (AUTHORITY_OEM, AUTHORITY_QTI):
                    encryption_features = getattr(authenticator, f'''supported_{authority.lower()}_encryption_features''')
                    if encryption_features:
                        for encryption_format in encryption_features.supported_encryption_formats.encryption_format:
                            parsed_profile_ids.append(encryption_format.id)
            profile_ids.append(parsed_profile_ids)
    # WARNING: Decompyle incomplete

    
    def get_variants(self = None):
        variants = set()
        for parsed_profile in self.parsed_profiles:
            profile_variants = []
            platform_bindings = parsed_profile.platform_binding_values
            for platform_binding in (SOC_HW_VERSIONS, JTAG_IDS, SOC_FEATURE_IDS, PRODUCT_SEGMENT_IDS):
                if getattr(platform_bindings, platform_binding, None):
                    profile_variants.extend((lambda .0: for value in .0:
if value.variant:
value.variantcontinueNone)(getattr(platform_bindings, platform_binding).value))
            variants = variants & set(profile_variants) if variants else set(profile_variants)
        return variants

    
    def supported_image_format_found(parsed_image_formats = None, profile_image_format = None, tool_specific_profile_format = staticmethod):
        match = False
        for idx, parsed_image_format in enumerate(parsed_image_formats):
            if isinstance(parsed_image_format, ImageFormat):
                if idx:
                    pass
                elif True:
                    pass
                match = compare_authentication_image_format(parsed_image_format, profile_image_format)
                continue
            if isinstance(parsed_image_format, LegacyDebugging) and tool_specific_profile_format:
                if idx:
                    pass
                elif True:
                    pass
                match = compare_legacy_debugging_format(parsed_image_format, tool_specific_profile_format)
                continue
            if isinstance(parsed_image_format, FuseBlowing) and tool_specific_profile_format:
                if idx:
                    pass
                elif True:
                    pass
                match = compare_fuse_blowing_format(parsed_image_format, tool_specific_profile_format)
        return match

    supported_image_format_found = None(supported_image_format_found)
    
    def get_target_image_format(self = None, image_format_string = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_elf_image_formats(self = None):
        pass
    # WARNING: Decompyle incomplete

    
    def set_image_format(self = None, current_image_format = None):
        """
        Sets the image format to that indicated by the image entry, if it exists. Otherwise, sets the image format to
        the first supported image format in the image's authenticator which matches the existing format of infile,
        with preference given to the authenticator's default image format.
        """
        supported_image_format = None
        error_message = None
        if tool_specific_profile_format = self.legacy_debugging_features:
            error_message = f'''by {SECURE_DEBUG_NAME} with the Security Profiles provided via {SECURITY_PROFILE}.'''
        elif tool_specific_profile_format = self.fuse_blowing_features:
            error_message = f'''by {FUSE_BLOWER_NAME} with the Security Profiles provided via {SECURITY_PROFILE}.'''
        if self.image and image_format_string = self.image.image_format:
            target_image_format = self.get_target_image_format(image_format_string)
            if not SecurityProfile.supported_image_format_found(current_image_format, target_image_format, tool_specific_profile_format):
                if not error_message:
                    pass
                raise RuntimeError(f'''The format of {INFILE} is not supported {f'''for {IMAGE_ID} {self.image.id}.'''}''')
            supported_image_format = self.image.image_format
    # WARNING: Decompyle incomplete

    
    def get_image_format_given_user_inputs(self = None, user_provided_segment_hash_algorithm = None):
        '''
        Other image format related functions consider only the existing image format and profile supported image
        formats. This function is used to find a supported image format which meets requirements specified by the user
        via the command line.
        '''
        log_debug(f'''Checking to see if any supported image formats are compatible with {user_provided_segment_hash_algorithm}.''')
    # WARNING: Decompyle incomplete

    
    def get_authenticator_id(authority = None, image = None):
        error = f'''Security Profiles provided via {SECURITY_PROFILE} does not allow for operations to be performed by {authority} for {image.id}.'''
        if not (authority == AUTHORITY_OEM or image.authenticator_oem or authority == AUTHORITY_QTI) and image.authenticator_qti:
            raise RuntimeError(error)
        if None == AUTHORITY_OEM:
            return image.authenticator_oem
        return None.authenticator_qti

    get_authenticator_id = None(get_authenticator_id)
    
    def resolve_authentication(self, image_ids = None, authority = None, encrypt = None, schema_member = ('image_ids', Iterable[str], 'authority', str, 'encrypt', bool, 'schema_member', dict[(str, dict)], 'return', None)):
        for image_id in image_ids:
            image_entries = []
            authenticator_entries = []
            for parsed_profile in self.parsed_profiles:
                verify_profile_elements(filter_elements(vars(parsed_profile.authentication)), schema_member.keys(), 'authentication', 'resolve_authentication')
                for image in parsed_profile.authentication.image_list.image:
                    if image.id == image_id:
                        image_entries.append(image)
                        authority_authenticator_id = SecurityProfile.get_authenticator_id(authority, image)
                        for authenticator in parsed_profile.authentication.authenticators.authenticator:
                            if authenticator.id == authority_authenticator_id:
                                authenticator_entries.append(authenticator)
            if len(self.parsed_profiles) > 1:
                resolve_image_entries_from_image_list(image_entries, schema_member['image_list'], False, **('resolving_multi_image',))
                self.target_image_format = resolve_image_formats_from_image_list(image_entries, authenticator_entries, schema_member['image_list'])
            self.images.append(image_entries[0])
            self.authenticators.append(resolve_authenticator(authenticator_entries, encrypt, schema_member['authenticators']['authenticator']) if len(self.parsed_profiles) > 1 else authenticator_entries[0])

    
    def resolve_tme(self = None, schema_member = None):
        elf_properties = []
        for parsed_profile in self.parsed_profiles:
            if parsed_profile.debugging.tme.tme_elf_properties:
                elf_properties.append(parsed_profile.debugging.tme.tme_elf_properties)
        self.tme_debugging_features = self.parsed_profiles[0].debugging.tme
        self.tme_debugging_features.tme_elf_properties = resolve_tme_elf_properties(elf_properties, schema_member['tme_elf_properties'])

    
    def validate_vouch_for_image_format(vouch_for_image_format = None, authenticator = None):
        vouch_for_meets_security_profile_constraints = False
        for profile_image_format in authenticator.supported_image_formats.image_format:
            if SecurityProfile.supported_image_format_found(vouch_for_image_format, profile_image_format):
                vouch_for_meets_security_profile_constraints = True
                return vouch_for_meets_security_profile_constraints
            return vouch_for_meets_security_profile_constraints

    validate_vouch_for_image_format = None(validate_vouch_for_image_format)
    
    def _get_multi_image_formats(self = None, authority = None):
        multi_image_formats = []
        image_entries = []
        authenticator_entries = []
        for parsed_profile in self.parsed_profiles:
            for image in parsed_profile.authentication.image_list.image:
                current_authenticator = image.authenticator_qti if authority == AUTHORITY_QTI else image.authenticator_oem
                if not current_authenticator:
                    continue
                for authenticator in parsed_profile.authentication.authenticators.authenticator:
                    if authenticator.id == current_authenticator:
                        temp_image_format = image.image_format if image.image_format else authenticator.default_image_format
                        for authenticator_image in authenticator.supported_image_formats.image_format:
                            if authenticator_image.id == temp_image_format and authenticator_image.vouch_segment_properties:
                                multi_image_formats.append(authenticator_image)
                                image_entries.append(image)
                                authenticator_entries.append(authenticator)
                            
                            return (multi_image_formats, image_entries, authenticator_entries)

    
    def get_multi_image_format(self = None, authority = None, signature_format_id = None):
        self.images = []
        self.authenticators = []
        (multi_image_formats, image_entries, authenticator_entries) = self._get_multi_image_formats(authority)
        if not multi_image_formats or len(multi_image_formats) == len(self.parsed_profiles):
            raise RuntimeError(f'''No supporting image format found for {INFILE} for the {VOUCH_FOR} operation as {authority}.''')
        schema_authenticator = None['profile']['authentication']['authenticators']['authenticator']
        resolved_multi_image_format = multi_image_formats[0]
        schema_image_format = schema_authenticator['supported_image_formats']['image_format']
        for multi_image_format in multi_image_formats:
            resolved_multi_image_format = resolve_image_format(resolved_multi_image_format, multi_image_format, schema_image_format)
        self.image_format = resolved_multi_image_format
        schema_member = SCHEMA_STRUCTURE['profile']['authentication']
        if len(self.parsed_profiles) > 1:
            resolve_image_entries_from_image_list(image_entries, schema_member['image_list'], True, **('resolving_multi_image',))
        self.images.append(image_entries[0])
        authenticator = resolve_authenticator(authenticator_entries, False, schema_member['authenticators']['authenticator']) if len(self.parsed_profiles) > 1 else authenticator_entries[0]
        self.authenticators.append(authenticator)
        self.set_signing_features_and_signature_format(authority, signature_format_id)
        return resolved_multi_image_format

    
    def get_multi_image_image_ids(self = None, authority = None):
        (_, image_entries, _) = self._get_multi_image_formats(authority)
        return list(set((lambda .0: for image_entry in .0:
image_entry.id)(image_entries)))

    
    def authority_signing_features(self = None, authority = None):
        pass
    # WARNING: Decompyle incomplete

    
    def get_metadata_versions(self = None):
        if self.hash_table_segment_properties:
            metadata_versions = self.hash_table_segment_metadata_versions
            default_metadata_version = metadata_versions.default_hash_table_segment_metadata_version
            supported_metadata_versions = metadata_versions.supported_hash_table_segment_metadata_versions.value
            return (default_metadata_version, supported_metadata_versions)
        metadata_versions = None.mbn_metadata_versions
        default_metadata_version = metadata_versions.default_mbn_metadata_version
        supported_metadata_versions = metadata_versions.supported_mbn_metadata_versions.value
        return (default_metadata_version, supported_metadata_versions)

    
    def requires_rs_48_49(self = None):
        if self.signature_algorithm == ALGORITHM_ECDSA_USER_FACING:
            pass
        return RS_48_49 in self.default_ecdsa_curve

    
    def hash_table_segment_properties(self = None):
        return self.image_format.hash_table_segment_properties

    hash_table_segment_properties = None(hash_table_segment_properties)
    
    def hash_table_segment_alignment(self = None):
        return self.hash_table_segment_properties.hash_table_segment_alignment

    hash_table_segment_alignment = None(hash_table_segment_alignment)
    
    def hash_table_segment_placements(self = None):
        return self.hash_table_segment_properties.hash_table_segment_placements

    hash_table_segment_placements = None(hash_table_segment_placements)
    
    def default_hash_table_segment_placement(self = None):
        return self.hash_table_segment_placements.default_hash_table_segment_placement

    default_hash_table_segment_placement = None(default_hash_table_segment_placement)
    
    def supported_hash_table_segment_placements(self = None):
        return self.hash_table_segment_placements.supported_hash_table_segment_placements.value

    supported_hash_table_segment_placements = None(supported_hash_table_segment_placements)
    
    def segment_hash_algorithms(self = None):
        if self.hash_table_segment_properties:
            return self.hash_table_segment_properties.segment_hash_algorithms

    segment_hash_algorithms = None(segment_hash_algorithms)
    
    def default_segment_hash_algorithm(self = None):
        if self.segment_hash_algorithms:
            return self.segment_hash_algorithms.default_segment_hash_algorithm

    default_segment_hash_algorithm = None(default_segment_hash_algorithm)
    
    def supported_segment_hash_algorithms(self = None):
        if self.segment_hash_algorithms:
            return self.segment_hash_algorithms.supported_segment_hash_algorithms

    supported_segment_hash_algorithms = None(supported_segment_hash_algorithms)
    
    def hash_table_segment_metadata_versions(self = None):
        return self.hash_table_segment_properties.hash_table_segment_metadata_versions

    hash_table_segment_metadata_versions = None(hash_table_segment_metadata_versions)
    
    def hash_pages(self = None):
        return self.hash_table_segment_properties.hash_pages

    hash_pages = None(hash_pages)
    
    def mbn_properties(self = None):
        return self.image_format.mbn_properties

    mbn_properties = None(mbn_properties)
    
    def mbn_metadata_versions(self = None):
        return self.mbn_properties.mbn_metadata_versions

    mbn_metadata_versions = None(mbn_metadata_versions)
    
    def signature_algorithm(self = None):
        return self.signature_format.signature_algorithm

    signature_algorithm = None(signature_algorithm)
    
    def default_signature_hash_algorithm(self = None):
        return self.signature_format.signature_hash_algorithms.default_signature_hash_algorithm

    default_signature_hash_algorithm = None(default_signature_hash_algorithm)
    
    def default_key_size(self = None):
        if self.signature_format.key_sizes:
            return self.signature_format.key_sizes.default_key_size

    default_key_size = None(default_key_size)
    
    def default_exponent(self = None):
        if self.signature_format.exponents:
            return self.signature_format.exponents.default_exponent

    default_exponent = None(default_exponent)
    
    def default_rsa_padding(self = None):
        if self.signature_format.rsa_paddings:
            return self.signature_format.rsa_paddings.default_rsa_padding

    default_rsa_padding = None(default_rsa_padding)
    
    def default_ecdsa_curve(self = None):
        if self.signature_format.ecdsa_curves:
            return self.signature_format.ecdsa_curves.default_ecdsa_curve

    default_ecdsa_curve = None(default_ecdsa_curve)
    
    def mrc_specs(self = None):
        return self.signing_features.mrc_specs

    mrc_specs = None(mrc_specs)
    
    def default_mrc_spec(self = None):
        if self.mrc_specs:
            return self.mrc_specs.default_mrc_spec

    default_mrc_spec = None(default_mrc_spec)
    
    def default_certificate_chain_depth(self = None):
        if self.signature_format.certificate_chain_depths_override:
            return self.signature_format.certificate_chain_depths_override.default_certificate_chain_depth
        return None.signing_features.certificate_chain_depths.default_certificate_chain_depth

    default_certificate_chain_depth = None(default_certificate_chain_depth)
    
    def supported_certificate_chain_depths(self = None):
        if self.signature_format.certificate_chain_depths_override:
            return self.signature_format.certificate_chain_depths_override.supported_certificate_chain_depths.value
        return None.signing_features.certificate_chain_depths.supported_certificate_chain_depths.value

    supported_certificate_chain_depths = None(supported_certificate_chain_depths)
    
    def license_manager_segment_properties(self = None):
        return self.image_format.license_manager_segment_properties

    license_manager_segment_properties = None(license_manager_segment_properties)
    
    def license_manager_segment_alignment(self = None):
        return self.license_manager_segment_properties.license_manager_segment_alignment

    license_manager_segment_alignment = None(license_manager_segment_alignment)
    
    def license_manager_segment_placements(self = None):
        return self.license_manager_segment_properties.license_manager_segment_placements

    license_manager_segment_placements = None(license_manager_segment_placements)
    
    def default_license_manager_segment_placement(self = None):
        return self.license_manager_segment_placements.default_license_manager_segment_placement

    default_license_manager_segment_placement = None(default_license_manager_segment_placement)
    
    def vouch_segment_properties(self = None):
        return self.image_format.vouch_segment_properties

    vouch_segment_properties = None(vouch_segment_properties)
    
    def vouch_segment_alignment(self = None):
        return self.vouch_segment_properties.vouch_segment_alignment

    vouch_segment_alignment = None(vouch_segment_alignment)
    
    def vouch_segment_placements(self = None):
        return self.vouch_segment_properties.vouch_segment_placements

    vouch_segment_placements = None(vouch_segment_placements)
    
    def default_vouch_segment_placement(self = None):
        return self.vouch_segment_placements.default_vouch_segment_placement

    default_vouch_segment_placement = None(default_vouch_segment_placement)
    
    def debug_policy_segment_alignment(self = None):
        return self.legacy_debugging_features.debug_policy_segment_alignment

    debug_policy_segment_alignment = None(debug_policy_segment_alignment)
    
    def default_debug_policy_segment_placement(self = None):
        return self.legacy_debugging_features.debug_policy_segment_placements.default_debug_policy_segment_placement

    default_debug_policy_segment_placement = None(default_debug_policy_segment_placement)
    
    def image(self = None):
        if self.images:
            return self.images[0]

    image = None(image)
    
    def authenticator(self = None):
        if self.authenticators:
            return self._authenticators[0]

    authenticator = None(authenticator)
    
    def authenticators(self = None):
        return self._authenticators

    authenticators = None(authenticators)
    
    def authenticators(self, value):
        self._authenticators = value

    authenticators = authenticators.setter(authenticators)
    
    def sec_elf_properties(self = None):
        return self.fuse_blowing_features.sec_elf_properties

    sec_elf_properties = None(sec_elf_properties)
    
    def sec_dat_properties(self = None):
        return self.fuse_blowing_features.sec_dat_properties

    sec_dat_properties = None(sec_dat_properties)
    
    def sec_dat_segment_alignment(self = None):
        return self.sec_elf_properties.sec_dat_segment_alignment

    sec_dat_segment_alignment = None(sec_dat_segment_alignment)
    
    def default_sec_dat_segment_placement(self = None):
        return self.sec_elf_properties.sec_dat_segment_placements.default_sec_dat_segment_placement

    default_sec_dat_segment_placement = None(default_sec_dat_segment_placement)
    
    def default_root_certificate_hash_algorithm(self = None):
        return self.signing_features.root_certificate_hash_algorithms.default_root_certificate_hash_algorithm

    default_root_certificate_hash_algorithm = None(default_root_certificate_hash_algorithm)
    
    def hash_table_segment_filesz_multiple(self = None):
        if self.image_format.hash_table_segment_properties and self.image_format.hash_table_segment_properties.hash_table_segment_filesz_multiple and self.image_format.hash_table_segment_properties.hash_table_segment_filesz_multiple != ANY:
            return int(self.image_format.hash_table_segment_properties.hash_table_segment_filesz_multiple, 16)

    hash_table_segment_filesz_multiple = None(hash_table_segment_filesz_multiple)

