
from pathlib import Path
from subprocess import CalledProcessError, run
from common.utils import SECTOOLS_PATH, is_arm64, is_linux, is_windows, temp_file_path
if is_linux():
    XZ_UTILS = str(Path(SECTOOLS_PATH) / f'''bin/LIN/{'AARCH64' if is_arm64() else 'X86'}/xz''')
elif is_windows():
    XZ_UTILS = str(Path(SECTOOLS_PATH) / 'bin/WIN/xz')
else:
    XZ_UTILS = str(Path(SECTOOLS_PATH) / 'bin/MAC/xz')

def compress(data = None):
    pass
# WARNING: Decompyle incomplete

