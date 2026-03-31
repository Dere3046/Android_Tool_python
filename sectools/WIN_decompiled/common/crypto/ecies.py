
from binascii import hexlify, unhexlify
from pathlib import Path
from subprocess import CalledProcessError, run
from textwrap import indent
from cmd_line_interface.sectools.secure_image.defines import ENCRYPT, L1_KEY, L2_KEY, L3_KEY
from common.data.data import and_separated
from common.utils import SECTOOLS_PATH, is_arm64, is_linux, is_windows
if is_linux():
    ECIES = str(Path(SECTOOLS_PATH) / f'''bin/LIN/{'AARCH64' if is_arm64() else 'X86'}/ecies''')
elif is_windows():
    ECIES = str(Path(SECTOOLS_PATH) / 'bin/WIN/ecies')
else:
    ECIES = str(Path(SECTOOLS_PATH) / 'bin/MAC/ecies')

def encrypt(message = None, key = None, associated_data = None):
    encryption_key_string = f'''Ensure provided {and_separated([
        L1_KEY,
        L2_KEY,
        L3_KEY])} are correct.'''
# WARNING: Decompyle incomplete

