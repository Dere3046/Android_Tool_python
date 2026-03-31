
from binascii import hexlify
from errno import ENOEXEC
from os import environ
from os.path import join
from pathlib import Path
from subprocess import CalledProcessError, run
from cmd_line_interface.sectools.secure_image.defines import ENCRYPT
from common.crypto.defines import ENCRYPT_OPERATION_UNSUPPORTED_ON_ARCHITECTURE
from common.utils import SECTOOLS_PATH, is_linux, is_windows, temp_file_path
if is_linux():
    CRYPTO_CCM = join(SECTOOLS_PATH, 'bin', 'LIN', 'X86', 'crypto_ccm')
elif is_windows():
    CRYPTO_CCM = join(SECTOOLS_PATH, 'bin', 'WIN', 'crypto_ccm')
else:
    macos_dir = join(SECTOOLS_PATH, 'bin', 'MAC')
    CRYPTO_CCM = join(macos_dir, 'crypto_ccm')
    environ['DYLD_LIBRARY_PATH'] = macos_dir

def encrypt(message = None, key = None, iv = None, associated_data = ('message', bytes, 'key', bytes, 'iv', bytes, 'associated_data', bytes, 'return', bytes)):
    pass
# WARNING: Decompyle incomplete

