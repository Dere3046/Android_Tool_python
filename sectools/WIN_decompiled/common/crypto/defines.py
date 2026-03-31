
from platform import machine
from cmd_line_interface.sectools.secure_image.defines import ENCRYPT
ENCRYPT_OPERATION_UNSUPPORTED_ON_ARCHITECTURE = f'''{ENCRYPT} operation is not supported on {machine()}.'''
