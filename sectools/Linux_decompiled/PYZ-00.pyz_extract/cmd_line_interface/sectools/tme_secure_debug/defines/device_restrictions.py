
from operator import methodcaller
from typing import NamedTuple
from cmd_line_interface.base_defines import KWARGS_ACTION, KWARGS_CHOICES, KWARGS_DEFAULT, KWARGS_HELP, KWARGS_NARGS, KWARGS_STORE_TRUE, KWARGS_TYPE, LimitedRangeInt
from cmd_line_interface.basecmdline import CMDLineArgs
from cmd_line_interface.sectools.cmd_line_common.defines import ANTI_ROLLBACK_VERSION, ANTI_ROLLBACK_VERSION_HELP, DEVICE_RESTRICTIONS_GROUP, INDEPENDENT, MEASUREMENT_REGISTER_TARGET, MEASUREMENT_REGISTER_TARGETS, MEASUREMENT_REGISTER_TARGET_HELP, OEM_ID, OEM_ID_HELP, OEM_LIFECYCLE_STATE, OEM_LIFECYCLE_STATE_HELP, OEM_PRODUCT_ID, OEM_PRODUCT_ID_HELP, OEM_ROOT_CERTIFICATE_HASH_HELP, OUTFILE, PLATFORM_BINDING, PLATFORM_BINDINGS, PRODUCT_SEGMENT_ID, QTI, ROOT_CERTIFICATE_INDEX, ROOT_CERTIFICATE_INDEX_HELP, SECURITY_PROFILE, SEGMENT_HASH_ALGORITHM, SERIAL_NUMBER, SERIAL_NUMBER_HELP, SIGN, SOC_FEATURE_ID, SOC_LIFECYCLE_STATE, SOC_LIFECYCLE_STATE_HELP, TRANSFER_ROOT, TRANSFER_ROOT_HELP, VARIANT, VARIANT_HELP, eight_byte_hex, four_byte_hex, sha256_sha384_hash, sha256_sha384_sha512_hash, two_byte_hex
from cmd_line_interface.sectools.metadata import CONSUMES, DEPENDS_ON, INCOMPATIBLE_WITH, VALUE_DEPENDS_ON
from cmd_line_interface.sectools.secure_image.defines import OEM_ROOT_CERTIFICATE_HASH
from cmd_line_interface.sectools.tme_secure_debug.defines.signing import OEM_ELF_USE_CASE_NOTE
from common.parser.tme.tme_parser.defines import CHIP_UNIQUE_IDENTIFIER_PATH, DP_CHIP_CONSTRAINTS_PATH, OEM_BATCH_KEY_HASH_PATH, OEM_RC_HASH_PATH
from common.parser.tme.tme_parser.tme import get_selections_for_tag
OEM_BATCH_KEY_HASH = '--oem-batch-key-hash'
TME_PLATFORM_BINDING_HELP = f'''Chipset identifiers in Security Profile for which {OUTFILE} is authorized. {SOC_FEATURE_ID} must be used with {QTI}.'''
OEM_BATCH_KEY_HASH_HELP = 'Hash of the OEM Batch Secret that the OEM provisions to the SoC using Secure OTP Provisioning.'
_soc_lifecycle_state_choices = get_selections_for_tag('SocLifeCycleState') - {
    'RECOVERY',
    'BLANK',
    'TERMINATED',
    'PERSONALIZED'}
# WARNING: Decompyle incomplete
