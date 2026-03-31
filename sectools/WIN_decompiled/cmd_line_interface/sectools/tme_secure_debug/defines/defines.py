
from contextlib import suppress
from typing import Any
from cmd_line_interface.auto_close_security_profile_type import auto_close_security_profile_type
from cmd_line_interface.base_defines import COMPATIBLE, HELP_GROUP, KWARGS_ACTION, KWARGS_CHOICES, KWARGS_DEFAULT, KWARGS_HELP, KWARGS_NARGS, KWARGS_STORE_TRUE, KWARGS_TYPE, OPTIONAL
from cmd_line_interface.basecmdline import CMDLineArgs, CMDLineGroup
from cmd_line_interface.sectools.cmd_line_common.base_defines import PLUGIN_SIGNER
from cmd_line_interface.sectools.cmd_line_common.defines import AUTHORITY, GENERATE, HASH, IMAGE_FORMAT_GROUP, IMAGE_INPUTS_GROUP, IMAGE_OPERATIONS_GROUP, IMAGE_OUTPUTS_GROUP, INFILE, OUTFILE, PLUGIN_SIGNER_ARGS, QTI, QTI_DPR, ROOT_KEY, SECURITY_PROFILE, SECURITY_PROFILE_GROUP, SECURITY_PROFILE_HELP, SEGMENT_HASH_ALGORITHM, SEGMENT_HASH_ALGORITHMS, SEGMENT_HASH_ALGORITHM_HELP, SIGN, SIGNING_MODE, VERIFY_ROOT
from cmd_line_interface.sectools.metadata import CONSUMES, DEPENDS_NOT_FORCED, DEPENDS_ON_ANY_OF, INCOMPATIBLE_WITH
from cmd_line_interface.sectools.tme_secure_debug.defines.debug_options import DEBUG_OPTIONS_GROUP, DEBUG_OPTIONS_GROUP_HELP, TME_DEBUG_OPTIONS_GROUP
from cmd_line_interface.sectools.tme_secure_debug.defines.device_restrictions import OEM_ELF_ONLY_DEVICE_RESTRICTIONS_GLOBAL_CLUSTER_ARGS, TME_DEVICE_RESTRICTIONS
from cmd_line_interface.sectools.tme_secure_debug.defines.help import TME_HELP_GROUP
from cmd_line_interface.sectools.tme_secure_debug.defines.image_inputs import SLC, TME_IMAGE_INPUTS_GROUP, TME_IMAGE_OUTPUTS_GROUP
from cmd_line_interface.sectools.tme_secure_debug.defines.image_operations import TME_IMAGE_OPERATIONS_GROUP
from cmd_line_interface.sectools.tme_secure_debug.defines.oem_test_signing import OEM_TEST_SIGNED_IMAGES_GROUP, TME_OEM_TEST_SIGNING_GROUP
from cmd_line_interface.sectools.tme_secure_debug.defines.signing import OEM_ELF_ONLY_SIGNING_GLOBAL_CLUSTER_ARGS, OEM_ELF_USE_CASE_NOTE, TME_SECURE_DEBUG_SIGNING
from cmd_line_interface.sectools.tme_secure_debug.defines.test_signing import QTI_TEST_SIGNED_IMAGES_GROUP, QTI_TEST_SIGNED_IMAGES_GROUP_HELP, TME_QTI_TEST_SIGNING_GROUP
from common.parser.tme.tme_parser.defines import DEBUG_OPTIONS_PATH
NONPUBLIC_GLOBAL_CLUSTER_ARGS: dict[(str, Any)] = { }
with suppress(ModuleNotFoundError):
    from cmd_line_interface.sectools.tme_secure_debug.nonpublic.nonpublic_defines import NONPUBLIC_GLOBAL_CLUSTER_ARGS
    None(None, None, None)
# WARNING: Decompyle incomplete
