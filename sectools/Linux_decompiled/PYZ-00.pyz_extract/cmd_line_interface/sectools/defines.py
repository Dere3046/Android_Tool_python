
from common.data.data import tuple_to_version_string
from common.utils import is_public_distro
SECTOOLS_VERSION = (1, 43)
SECTOOLS_DESCRIPTION = f'''{'Public ' if is_public_distro() else ''}Qualcomm Security Tools v{tuple_to_version_string(SECTOOLS_VERSION)}'''
