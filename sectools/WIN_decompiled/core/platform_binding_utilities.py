
from typing import Collection, Dict, List, Optional, Set
from cmd_line_interface.sectools.cmd_line_common.base_defines import SECURITY_PROFILE
from cmd_line_interface.sectools.cmd_line_common.defines import AVAILABLE_VARIANTS, INDEPENDENT, JTAG_ID, PLATFORM_BINDING, PRODUCT_SEGMENT_ID, SOC_FEATURE_ID, SOC_HW_VER, VARIANT
from common.data.data import comma_separated_string, numbered_string, plural_s
from profile.defines import JTAG_IDS, PRODUCT_SEGMENT_IDS, SOC_FEATURE_IDS, SOC_HW_VERSIONS
from profile.profile_core import SecurityProfile
PLATFORM_BINDINGS_MAPPING = {
    PRODUCT_SEGMENT_ID: PRODUCT_SEGMENT_IDS,
    SOC_FEATURE_ID: SOC_FEATURE_IDS,
    JTAG_ID: JTAG_IDS,
    SOC_HW_VER: SOC_HW_VERSIONS }

def get_security_profile_platform_binding_values(platform_bindings = None, variant = None, security_profile = None, validate_platform_bindings = (True, 12), max_soc_hw_ver = ('platform_bindings', Collection[str], 'variant', Optional[str], 'validate_platform_bindings', bool, 'max_soc_hw_ver', int, 'return', Dict[(str, List[int])])):
    default_platform_bindings = set(security_profile.signing_features.platform_bindings.default_platform_bindings.value) if security_profile.signing_features else set()
    enabled_platform_bindings = set(platform_bindings) if platform_bindings else default_platform_bindings
    if validate_platform_bindings:
        error_string = f'''{PLATFORM_BINDING}''' if platform_bindings else 'default_platform_bindings value'
        validate_platform_binding_values(security_profile, enabled_platform_bindings, variant, error_string)
    ret = { }
    if not security_profile.signing_features and security_profile.signing_features.platform_bindings.supports_multiple_soc_ver:
        max_soc_hw_ver = 1
    possible_platform_bindings = [
        (JTAG_ID, JTAG_IDS, 'JTAG ID', 1),
        (SOC_FEATURE_ID, SOC_FEATURE_IDS, 'SOC Feature ID', 1),
        (SOC_HW_VER, SOC_HW_VERSIONS, 'SOC Hardware Version', max_soc_hw_ver),
        (PRODUCT_SEGMENT_ID, PRODUCT_SEGMENT_IDS, 'Product Segment ID', 1)]
    for platform_binding, profile_member, error_string, limit in possible_platform_bindings:
        if platform_binding in enabled_platform_bindings:
            profile_values = getattr(security_profile.platform_bindings, profile_member)
            if variant:
                filtered_profile_values = None((lambda .0 = None: pass# WARNING: Decompyle incomplete
)(profile_values.value))
            else:
                filtered_profile_values = list((lambda .0: pass# WARNING: Decompyle incomplete
)(profile_values.value))
            ret[profile_member] = filtered_profile_values
            if ret[profile_member] and variant:
                raise RuntimeError(f'''No {error_string} exists for variant {variant}.''')
            if None(set(ret[profile_member])) > limit:
                error = f'''Cannot bind image to more than {limit} {error_string}{plural_s(limit)}.'''
                if not any((lambda .0: for profile_value in .0:
profile_value.variant)(profile_values.value)) and variant:
                    raise RuntimeError(f'''{error} A Variant must be provided via {VARIANT} in order to bind to a single {error_string}. Use option {AVAILABLE_VARIANTS} to show available variants.''')
                raise None(error)
            return ret


def validate_platform_binding_values(security_profile = None, platform_bindings = None, variant = None, error_string = ('security_profile', SecurityProfile, 'platform_bindings', Set[str], 'variant', Optional[str], 'error_string', str, 'return', None)):
    allowed_variants = security_profile.get_variants()
    if variant and variant not in allowed_variants:
        if allowed_variants:
            raise RuntimeError(f'''{variant} is not a supported {VARIANT}.\nSupported Variants are:\n{numbered_string(allowed_variants)}''')
        raise None(f'''{VARIANT} is not supported by {SECURITY_PROFILE}.''')
    authenticator_supported_platform_bindings = set(security_profile.signing_features.platform_bindings.supported_platform_bindings.value) if None.signing_features else set()
    chipset_supported_platform_bindings = (lambda .0 = None: pass# WARNING: Decompyle incomplete
)(PLATFORM_BINDINGS_MAPPING.items())
    supported_platform_bindings = authenticator_supported_platform_bindings.intersection(chipset_supported_platform_bindings)
    if not platform_bindings and platform_bindings != {
        INDEPENDENT} and platform_bindings.issubset(supported_platform_bindings):
        disallowed_values = comma_separated_string(list(platform_bindings - supported_platform_bindings), 'and', **('final_separator',))
        raise RuntimeError(f'''{SECURITY_PROFILE} does not support binding to {disallowed_values}.''')
    if None in platform_bindings or variant:
        raise RuntimeError(f'''{VARIANT} cannot be provided when {error_string} is {INDEPENDENT}.''')
    return None

