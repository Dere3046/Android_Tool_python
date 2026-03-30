
from binascii import hexlify
from contextlib import suppress
from pathlib import Path
from cmd_line_interface.sectools.cmd_line_common.base_defines import LOCAL, PLUGIN, PLUGIN_SIGNER, QTI, SECURITY_PROFILE, SIGN, TEST, UIE_ENCRYPTION_DESCRIPTION
from cmd_line_interface.sectools.cmd_line_common.defines import HASH, IMAGE_ID, INFILE, MANDATE_SECURITY_PROFILE_STRING, OEM_ROOT_CERTIFICATE_HASH_HELP, OUTFILE, SEGMENT_HASH_ALGORITHM, SEGMENT_HASH_ALGORITHM_HELP_TEMPLATE, VALIDATE
from common.parser.multi_image.defines import MULTI_IMAGE
from common.utils import SECTOOLS_PATH
NONPUBLIC_ENCRYPTION_MODES: list[str] = []
NONPUBLIC_ENCRYPTION_MODE_HELP: str = ''
with suppress(ModuleNotFoundError):
    from cmd_line_interface.nonpublic.nonpublic_defines import NONPUBLIC_ENCRYPTION_MODE_HELP
    from cmd_line_interface.sectools.nonpublic.nonpublic_defines import NONPUBLIC_ENCRYPTION_MODES
    None(None, None, None)
# WARNING: Decompyle incomplete
