
from functools import reduce
from pathlib import Path
from typing import Any, Callable, Type
import profile
from cmd_line_interface.base_defines import get_cmd_arg
from cmd_line_interface.basecmdline import NamespaceWithGet
from cmd_line_interface.sectools.cmd_line_common.base_defines import LOCAL, PLUGIN, PLUGIN_SIGNER, SECURITY_PROFILE
from cmd_line_interface.sectools.cmd_line_common.defines import DUMP, GENERATE, HASH, INFILE, INSPECT, OUTFILE, PLATFORM_BINDING, PLUGIN_SIGNER_ARGS, QTI, ROOT_KEY, SIGN, SIGNATURE_FORMAT, SIGNING_MODE, VARIANT, VERIFY_ROOT
from cmd_line_interface.sectools.tme_secure_debug.defines import TME_SECURE_DEBUG_NAME, defines
from cmd_line_interface.sectools.tme_secure_debug.defines.device_restrictions import OEM_ELF_ONLY_DEVICE_RESTRICTIONS_GLOBAL_CLUSTER_ARGS
from cmd_line_interface.sectools.tme_secure_debug.defines.image_inputs import DEC
from cmd_line_interface.sectools.tme_secure_debug.dynamic_arguments import set_security_profile_data_for_inspect
from common.data.base_parser import BaseParser
from common.logging.logger import log_debug, log_info
from common.parser.hash_segment.defines import AUTHORITY_OEM, AUTHORITY_QTI
from common.parser.tme.base_tme import BaseTME
from common.parser.tme.dpr.dpr import DPR, FORMAT_TME
from common.parser.tme.dpr.validations import DPRValidationOptions, validate_and_apply_tme_limits
from common.parser.tme.tme_parser.defines import DEBUG_POLICY_DATA_PATH
from common.parser.tme.tme_parser.tme import TME
from common.parser.tme_elf.tme_elf import TMEELF
from common.utils import write_cmdline_file
from core.base_device_restrictions import BaseDeviceRestrictions
from core.core_interfaces.core_security_profile_validator_interface import CoreSecurityProfileValidatorInterface
from core.core_interfaces.core_specific_profile_consumer_interface import CoreSpecificProfileConsumerInterface
from core.hash_sign_core import HashSignCore, log_info_wrap
from core.platform_binding_utilities import get_security_profile_platform_binding_values
from core.tme_secure_debug.augmented_inspect import DESCRIBE_DP, DESCRIBE_DPR, DESCRIBE_OEM_DPR, DESCRIBE_QTI_DPR, TME_DEBUG_POLICY_IMAGE, describe
from core.tme_secure_debug.generate_dp import generate_dp
from core.tme_secure_debug.generate_dpr import generate_dpr
from core.tme_secure_debug.generate_elf import generate_elf
from core.tme_secure_debug.signer.chip_constraints_converter import apply_chip_constraints_to_device_restrictions
from core.tme_secure_debug.signer.local.tme_local_signer import local_sign
from core.tme_secure_debug.signer.plugin.tme_plugin_signer import plugin_sign
from profile.defines import SCHEMA_STRUCTURE
from profile.profile_core import SecurityProfile
from profile.schema.scale_profile import Profile

nonpublic_check_tme_secure_debug_args: Callable[([
    Any], bool)] = lambda _: False
sign: Callable[([
    Any,
    Any], Any)] | None = None
# WARNING: Decompyle incomplete
