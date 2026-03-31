
from binascii import hexlify
from errno import ENOEXEC
from os.path import join
from pathlib import Path
from subprocess import CalledProcessError, run
from cmd_line_interface.sectools.secure_image.defines import ENCRYPT
from common.crypto.defines import ENCRYPT_OPERATION_UNSUPPORTED_ON_ARCHITECTURE
from common.utils import SECTOOLS_PATH, is_linux, is_windows, temp_file_path
if is_linux():
    CRYPTO_CBC = join(SECTOOLS_PATH, 'bin', 'LIN', 'X86', 'crypto_cbc')
elif is_windows():
    CRYPTO_CBC = join(SECTOOLS_PATH, 'bin', 'WIN', 'crypto_cbc')
else:
    CRYPTO_CBC = join(SECTOOLS_PATH, 'bin', 'MAC', 'crypto_cbc')

def encrypt(message = None, key = None, iv = None):
    pass
# WARNING: Decompyle incomplete

