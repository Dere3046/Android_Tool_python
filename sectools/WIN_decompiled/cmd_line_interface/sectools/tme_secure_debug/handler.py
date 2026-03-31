
from argparse import SUPPRESS
from contextlib import suppress
from typing import Any, Callable
from cmd_line_interface.base_defines import get_cmd_arg, get_cmd_member
from cmd_line_interface.basecmdline import BaseCMDLine, NamespaceWithGet
from cmd_line_interface.sectools.argument_clustering_interface import ArgumentClusteringInterface
from cmd_line_interface.sectools.cmd_line_common.base_defines import SECURITY_PROFILE
from cmd_line_interface.sectools.cmd_line_common.defines import DUMP, GENERATE, HASH, INSPECT, QTI, QTI_DPR, ROOT_KEY, SIGN, VERIFY_ROOT
from cmd_line_interface.sectools.cmd_line_common.handler import CommonCMDLineHandler
from cmd_line_interface.sectools.dynamic_arguments_interface import DynamicArgumentsInterface
from cmd_line_interface.sectools.secure_debug.handler import SecureDebugCMDLineHandler
from cmd_line_interface.sectools.tme_secure_debug.defines import TME_SECURE_DEBUG_NAME, defines
from cmd_line_interface.sectools.tme_secure_debug.defines.defines import GLOBAL_CLUSTER_ARGS, OEM_ELF_USE_CASE_ONLY_ARGS
from cmd_line_interface.sectools.tme_secure_debug.defines.device_restrictions import TME_DEVICE_RESTRICTIONS
from cmd_line_interface.sectools.tme_secure_debug.defines.image_inputs import DEC, SLC
from cmd_line_interface.sectools.tme_secure_debug.defines.image_operations import NEW_DPR
from cmd_line_interface.sectools.tme_secure_debug.defines.signing import TME_SECURE_DEBUG_SIGNING
from cmd_line_interface.sectools.tme_secure_debug.dynamic_arguments import update_tme_security_profile_arguments
from common.data.data import comma_separated_string
from common.parser.tme.dpr.dpr import FORMAT_TME
from common.parser.tme.dpr.validation_utils import get_cmd_arg_by_consumed_tme_tag_name
nonpublic_validate_complex_cluster_rules_check: Callable[([
    Any], Any)] | None = None
nonpublic_handler_tme_secure_debug: Callable[([
    Any], Any)] | None = None
with suppress(ModuleNotFoundError):
    from cmd_line_interface.sectools.nonpublic.nonpublic_sectools_handlers import nonpublic_handler_tme_secure_debug, nonpublic_validate_complex_cluster_rules_check
    None(None, None, None)
# WARNING: Decompyle incomplete
